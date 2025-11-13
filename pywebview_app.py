"""PyWebView-based Espanso Companion Pro application."""

from __future__ import annotations

import atexit
import json
import threading
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

import webview

import platform
import shutil
import subprocess
import tempfile
import urllib.request

from espanso_companion.cli_integration import EspansoCLI
from espanso_companion.config_loader import ConfigLoader
from espanso_companion.feature_catalog import FeatureCatalog, CatalogSection
from espanso_companion.file_watcher import FileWatcher, WatchEvent
from espanso_companion.variable_engine import VariableEngine
from espanso_companion.yaml_processor import YamlProcessor


def _section_to_dict(section: CatalogSection) -> Dict[str, Any]:
    return {
        "title": section.title,
        "description": section.description,
        "items": list(section.items),
    }


class EspansoAPI:
    """Exposes the backend surface to the JavaScript dashboard."""

    def __init__(self) -> None:
        loader = ConfigLoader()
        self._paths = loader.discover_paths()
        for path in self._paths.__dict__.values():
            path.mkdir(parents=True, exist_ok=True)
        self.yaml_processor = YamlProcessor()
        self.variable_engine = VariableEngine()
        self.cli = EspansoCLI()
        self._events: deque[Dict[str, Any]] = deque(maxlen=60)
        self._event_lock = threading.Lock()
        self._match_cache: List[Dict[str, Any]] = []
        self._yaml_errors: List[Dict[str, Any]] = []
        self._connection_steps: List[Dict[str, Any]] = []
        self._watcher = FileWatcher([self._paths.match, self._paths.config])
        self._watcher.register_callback(self._capture_event)
        self._watcher.start()
        self.refresh_files()
        atexit.register(self.shutdown)

    def shutdown(self) -> None:
        """Shutdown resources with proper error logging."""
        try:
            self._watcher.stop()
        except Exception as exc:
            # Log the error but don't fail shutdown
            # In production, this could be logged to a file
            print(f"Warning: Error stopping file watcher: {exc}", flush=True)

    def _capture_event(self, event: WatchEvent) -> None:
        """Capture filesystem events with error handling."""
        try:
            entry = {
                "type": event.event_type,
                "file": Path(event.src_path).name if event.src_path else "unknown",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            with self._event_lock:
                self._events.appendleft(entry)
        except Exception:
            # Silently ignore errors to prevent watcher thread crash
            # This protects against invalid paths, race conditions, etc.
            pass

    def _populate_matches(self) -> None:
        """Load and parse all match files with error tracking."""
        matches: List[Dict[str, Any]] = []
        match_dir = self._paths.match
        if not match_dir.exists():
            self._match_cache = matches
            return

        yaml_errors = []
        for file in match_dir.glob("*.yml"):
            try:
                data = self.yaml_processor.load(file)
            except Exception as exc:
                # Track YAML errors for diagnostics but continue processing
                yaml_errors.append({"file": file.name, "error": str(exc)})
                continue

            try:
                flattened = self.yaml_processor.flatten_matches(data)
                for match in flattened:
                    matches.append(
                        {
                            "name": match.name,
                            "trigger": match.trigger,
                            "replace": match.replace,
                            "variables": match.variables,
                            "enabled": match.enabled,
                            "file": file.name,
                            "hasForm": bool(match.variables) or bool(match.meta.get("form") if match.meta else False),
                            "hasVars": bool(match.variables),
                        }
                    )
            except Exception as exc:
                # Track processing errors
                yaml_errors.append({"file": file.name, "error": f"Processing error: {exc}"})

        self._match_cache = matches
        # Store errors for diagnostics (could be exposed to UI later)
        self._yaml_errors = yaml_errors

    def _get_event_snapshot(self) -> List[Dict[str, Any]]:
        with self._event_lock:
            return list(self._events)

    def _run_connection_sequence(self) -> None:
        self._connection_steps = []
        steps: List[Tuple[str, Callable[[], Tuple[str, str]]]] = [
            ("Ensure Espanso CLI", self._ensure_espanso_installed),
            ("Espanso service running", self._start_espanso_service),
            ("Check Espanso version", self._check_cli_available),
            ("Detect configuration paths", self._verify_paths),
            ("Validate YAML structure", self._validate_yaml),
            ("Ensure watcher ping", self._check_watcher),
        ]
        for label, action in steps:
            self._record_step(label, action)

    def _record_step(self, label: str, action: Callable[[], Tuple[str, str]]) -> None:
        try:
            status, detail = action()
        except Exception as exc:
            status = "error"
            detail = str(exc)
        self._connection_steps.append(
            {
                "label": label,
                "status": status,
                "detail": detail,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    def _check_cli_available(self) -> Tuple[str, str]:
        result = self.cli.run(["--version"])
        if result.returncode == 0:
            message = result.stdout.strip() or "Espanso CLI ready"
            return "success", message
        return "error", result.stderr.strip() or result.stdout.strip() or "Espanso CLI missing"

    def _ensure_espanso_installed(self) -> Tuple[str, str]:
        if shutil.which("espanso"):
            return "success", "Espanso CLI already present"
        try:
            installer = self._install_espanso()
            return "success", f"Downloaded installer {installer.name}"
        except Exception as exc:
            return "error", f"Failed to install: {exc}"

    def _install_espanso(self) -> Path:
        """Download and install Espanso with proper error reporting."""
        if platform.system() != "Windows":
            raise RuntimeError("Auto-install supported only on Windows")

        installer_url = "https://github.com/federico-terzi/espanso/releases/latest/download/espanso-setup.exe"
        target = Path(tempfile.gettempdir()) / "espanso-setup.exe"

        try:
            # Download installer with error handling
            urllib.request.urlretrieve(installer_url, target)
        except Exception as exc:
            raise RuntimeError(f"Failed to download Espanso installer: {exc}")

        # Run installer and capture output for diagnostics
        result = subprocess.run(
            [str(target), "/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART"],
            check=False,  # Don't raise on error - we want to check returncode
            capture_output=True,  # Capture output instead of suppressing
            text=True,
        )

        if result.returncode != 0:
            error_msg = result.stderr.strip() or result.stdout.strip() or f"Exit code {result.returncode}"
            raise RuntimeError(f"Espanso installer failed: {error_msg}")

        return target

    def _start_espanso_service(self) -> Tuple[str, str]:
        result = self.cli.run(["start"])
        if result.returncode == 0:
            return "success", "Espanso daemon started"
        detail = result.stdout.strip() or result.stderr.strip()
        status = "warning" if "already running" in detail.lower() else "error"
        return status, detail or "start command failed"

    def _verify_paths(self) -> Tuple[str, str]:
        details = ", ".join(
            f"{name}: {path}"
            for name, path in self._paths.__dict__.items()
        )
        return "success", details

    def _validate_yaml(self) -> Tuple[str, str]:
        match_files = list(self._paths.match.glob("*.yml"))
        if not match_files:
            return "warning", "No match files yet; waiting for snippets."
        try:
            self.yaml_processor.load(match_files[0])
            return "success", f"Parsed {match_files[0].name}"
        except Exception as exc:
            return "error", f"YAML parse failed: {exc}"

    def _check_watcher(self) -> Tuple[str, str]:
        observer = getattr(self._watcher, "_observer", None)
        if observer is not None and observer.is_alive():
            return "success", "Filesystem watcher active"
        return "warning", "Watcher not running yet"

    def _autostart_status(self) -> Dict[str, str]:
        """Check if espanso is registered as a system service (autostart)."""
        # In Espanso 2.x, the command is 'service check' not 'autostart status'
        result = self.cli.run(["service", "check"])
        detail = result.stdout.strip() or result.stderr.strip()

        # Exit code 2 means "not registered" which is a valid state
        if result.returncode == 0:
            # Successfully registered
            return {"status": "success", "detail": detail or "Auto-start enabled"}
        elif result.returncode == 2:
            # Not registered (expected when autostart is disabled)
            return {"status": "warning", "detail": detail or "Auto-start disabled"}
        else:
            # Other error
            return {"status": "error", "detail": detail or "Unable to check autostart status"}

    def _run_package_command(self, args: List[str]) -> Dict[str, str]:
        result = self.cli.run(args)
        detail = result.stdout.strip() or result.stderr.strip()
        status = "success" if result.returncode == 0 else "error"
        return {"status": status, "detail": detail or f"Command {' '.join(args)} completed"}

    def get_dashboard(self) -> Dict[str, Any]:
        self._populate_matches()
        status = self.cli.status()
        self._run_connection_sequence()
        matches = self._match_cache
        form_snippets = sum(1 for snippet in matches if snippet["hasForm"])
        var_snippets = sum(1 for snippet in matches if snippet["hasVars"])
        recent_events = self._get_event_snapshot()
        return {
            "configPath": str(self._paths.config),
            "statusMessage": "Connected" if status["returncode"] == 0 else "CLI unavailable",
            "cliStatus": status["stdout"] or status["stderr"] or "Ready",
            "snippetCount": len(matches),
            "matchFileCount": len(list(self._paths.match.glob("*.yml"))),
            "formSnippets": form_snippets,
            "variableSnippets": var_snippets,
            "eventCount": len(recent_events),
            "recentEvents": recent_events[:10],
            "connectionSteps": self._connection_steps,
        }

    def get_settings(self) -> Dict[str, Any]:
        status = self.cli.status()
        autostart = self._autostart_status()
        return {
            "serviceStatus": status["stdout"].strip() or status["stderr"].strip() or "Unknown",
            "autostart": autostart,
            "packages": self.cli.packages(),
        }

    def toggle_autostart(self, enable: bool) -> Dict[str, str]:
        """Enable or disable espanso autostart (system service registration)."""
        # In Espanso 2.x, the commands are 'service register' / 'service unregister'
        cmd = "register" if enable else "unregister"
        result = self.cli.run(["service", cmd])
        detail = result.stdout.strip() or result.stderr.strip()
        status = "success" if result.returncode == 0 else "error"
        return {"status": status, "detail": detail or f"Autostart {cmd} completed"}

    def install_package(self, name: str) -> Dict[str, str]:
        return self._run_package_command(["package", "install", name])

    def uninstall_package(self, name: str) -> Dict[str, str]:
        return self._run_package_command(["package", "uninstall", name])

    def start_service(self) -> Dict[str, str]:
        result = self.cli.run(["start"])
        detail = result.stdout.strip() or result.stderr.strip()
        status = "success" if result.returncode == 0 else "warning"
        return {"status": status, "detail": detail or "Espanso start requested"}

    def stop_service(self) -> Dict[str, str]:
        result = self.cli.run(["stop"])
        detail = result.stdout.strip() or result.stderr.strip()
        status = "success" if result.returncode == 0 else "warning"
        return {"status": status, "detail": detail or "Espanso stop requested"}

    def restart_service(self) -> Dict[str, str]:
        result = self.cli.reload()
        detail = result.stdout.strip() or result.stderr.strip()
        status = "success" if result.returncode == 0 else "warning"
        return {"status": status, "detail": detail or "Espanso restart issued"}

    def list_snippets(self) -> List[Dict[str, Any]]:
        self._populate_matches()
        return self._match_cache

    def refresh_files(self) -> Dict[str, Any]:
        self._populate_matches()
        return self.get_dashboard()

    def get_base_yaml(self) -> Dict[str, Any]:
        """Read the base.yaml file for editing."""
        base_file = self._paths.match / "base.yml"
        try:
            if base_file.exists():
                content = base_file.read_text(encoding="utf-8")
                return {"status": "success", "content": content, "path": str(base_file)}
            else:
                return {"status": "error", "content": "", "detail": "base.yml not found"}
        except Exception as exc:
            return {"status": "error", "content": "", "detail": f"Failed to read base.yml: {exc}"}

    def save_base_yaml(self, content: str) -> Dict[str, str]:
        """Save the base.yaml file after editing."""
        base_file = self._paths.match / "base.yml"
        try:
            # Validate YAML syntax before saving
            self.yaml_processor.load_str(content)

            # Create backup before saving
            if base_file.exists():
                backup_dir = Path.home() / ".espanso_companion" / "editor_backups"
                backup_dir.mkdir(parents=True, exist_ok=True)
                backup_file = backup_dir / f"base.yml.{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.bak"
                backup_file.write_text(base_file.read_text(encoding="utf-8"), encoding="utf-8")

            # Save new content
            base_file.write_text(content, encoding="utf-8")

            # Refresh snippets cache
            self.refresh_files()

            # Reload espanso to apply changes
            self.cli.run(["restart"])

            return {"status": "success", "detail": f"Saved and reloaded Espanso"}
        except Exception as exc:
            return {"status": "error", "detail": f"Failed to save: {exc}"}

    # ========================================
    # SNIPPET CRUD OPERATIONS
    # ========================================

    def create_snippet(self, snippet_data: Dict[str, Any]) -> Dict[str, str]:
        """Create a new snippet in base.yml."""
        try:
            base_file = self._paths.match / "base.yml"

            # Load existing content
            if base_file.exists():
                data = self.yaml_processor.load(base_file)
            else:
                data = {"matches": []}

            # Build new match object
            new_match = {"trigger": snippet_data["trigger"], "replace": snippet_data["replace"]}

            # Add optional properties
            if snippet_data.get("word"):
                new_match["word"] = True
            if snippet_data.get("propagate_case"):
                new_match["propagate_case"] = True
            if snippet_data.get("vars"):
                new_match["vars"] = snippet_data["vars"]
            if snippet_data.get("form"):
                new_match["form"] = snippet_data["form"]

            # Add to matches
            if "matches" not in data:
                data["matches"] = []
            data["matches"].append(new_match)

            # Save back to file
            import yaml
            backup_dir = Path.home() / ".espanso_companion" / "editor_backups"
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_file = backup_dir / f"base.yml.{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}.bak"
            if base_file.exists():
                backup_file.write_text(base_file.read_text(encoding="utf-8"), encoding="utf-8")

            base_file.write_text(yaml.dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")

            # Refresh and reload
            self.refresh_files()
            self.cli.run(["restart"])

            return {"status": "success", "detail": f"Created snippet '{snippet_data['trigger']}'"}
        except Exception as exc:
            return {"status": "error", "detail": f"Failed to create snippet: {exc}"}

    def update_snippet(self, original_trigger: str, snippet_data: Dict[str, Any]) -> Dict[str, str]:
        """Update an existing snippet in base.yml."""
        try:
            base_file = self._paths.match / "base.yml"

            if not base_file.exists():
                return {"status": "error", "detail": "base.yml not found"}

            data = self.yaml_processor.load(base_file)

            # Find the match to update
            found = False
            for match in data.get("matches", []):
                if match.get("trigger") == original_trigger:
                    # Update fields
                    match["trigger"] = snippet_data["trigger"]
                    match["replace"] = snippet_data["replace"]

                    # Update optional properties
                    match.pop("word", None)
                    match.pop("propagate_case", None)
                    match.pop("vars", None)
                    match.pop("form", None)

                    if snippet_data.get("word"):
                        match["word"] = True
                    if snippet_data.get("propagate_case"):
                        match["propagate_case"] = True
                    if snippet_data.get("vars"):
                        match["vars"] = snippet_data["vars"]
                    if snippet_data.get("form"):
                        match["form"] = snippet_data["form"]

                    found = True
                    break

            if not found:
                return {"status": "error", "detail": f"Snippet '{original_trigger}' not found"}

            # Save back to file
            import yaml
            backup_dir = Path.home() / ".espanso_companion" / "editor_backups"
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_file = backup_dir / f"base.yml.{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}.bak"
            backup_file.write_text(base_file.read_text(encoding="utf-8"), encoding="utf-8")

            base_file.write_text(yaml.dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")

            # Refresh and reload
            self.refresh_files()
            self.cli.run(["restart"])

            return {"status": "success", "detail": f"Updated snippet '{snippet_data['trigger']}'"}
        except Exception as exc:
            return {"status": "error", "detail": f"Failed to update snippet: {exc}"}

    def delete_snippet(self, trigger: str) -> Dict[str, str]:
        """Delete a snippet from base.yml."""
        try:
            base_file = self._paths.match / "base.yml"

            if not base_file.exists():
                return {"status": "error", "detail": "base.yml not found"}

            data = self.yaml_processor.load(base_file)

            # Filter out the match
            original_count = len(data.get("matches", []))
            data["matches"] = [m for m in data.get("matches", []) if m.get("trigger") != trigger]

            if len(data["matches"]) == original_count:
                return {"status": "error", "detail": f"Snippet '{trigger}' not found"}

            # Save back to file
            import yaml
            backup_dir = Path.home() / ".espanso_companion" / "editor_backups"
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_file = backup_dir / f"base.yml.{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}.bak"
            backup_file.write_text(base_file.read_text(encoding="utf-8"), encoding="utf-8")

            base_file.write_text(yaml.dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")

            # Refresh and reload
            self.refresh_files()
            self.cli.run(["restart"])

            return {"status": "success", "detail": f"Deleted snippet '{trigger}'"}
        except Exception as exc:
            return {"status": "error", "detail": f"Failed to delete snippet: {exc}"}

    def get_snippet(self, trigger: str) -> Dict[str, Any]:
        """Get a single snippet by trigger for editing."""
        try:
            base_file = self._paths.match / "base.yml"

            if not base_file.exists():
                return {"status": "error", "detail": "base.yml not found"}

            data = self.yaml_processor.load(base_file)

            for match in data.get("matches", []):
                if match.get("trigger") == trigger:
                    return {
                        "status": "success",
                        "snippet": {
                            "trigger": match.get("trigger", ""),
                            "replace": match.get("replace", ""),
                            "word": match.get("word", False),
                            "propagate_case": match.get("propagate_case", False),
                            "vars": match.get("vars", []),
                            "form": match.get("form", "")
                        }
                    }

            return {"status": "error", "detail": f"Snippet '{trigger}' not found"}
        except Exception as exc:
            return {"status": "error", "detail": f"Failed to get snippet: {exc}"}

    def get_variable_types(self) -> List[Dict[str, Any]]:
        """Get all supported variable types with their metadata."""
        return [
            {"type": "date", "label": "Date/Time", "icon": "DATE", "params": ["format", "offset"]},
            {"type": "clipboard", "label": "Clipboard", "icon": "CLIP", "params": ["fallback"]},
            {"type": "random", "label": "Random Choice", "icon": "RAND", "params": ["choices"]},
            {"type": "shell", "label": "Shell Command", "icon": "SHELL", "params": ["cmd", "shell"]},
            {"type": "script", "label": "Script", "icon": "SCRIPT", "params": ["args"]},
            {"type": "echo", "label": "Echo Prompt", "icon": "ECHO", "params": ["prompt"]},
            {"type": "choice", "label": "User Choice", "icon": "CHOICE", "params": ["values"]},
            {"type": "form", "label": "Form Input", "icon": "FORM", "params": ["fields"]},
            {"type": "match", "label": "Match Reference", "icon": "MATCH", "params": ["trigger"]},
        ]

    def get_global_variables(self) -> List[Dict[str, Any]]:
        """Get all global variables from all snippets for reuse."""
        self._populate_matches()
        global_vars = []
        seen = set()

        for match in self._match_cache:
            if match.get("vars"):
                for var in match["vars"]:
                    var_key = f"{var['name']}:{var['type']}"
                    if var_key not in seen:
                        seen.add(var_key)
                        global_vars.append({
                            "name": var["name"],
                            "type": var["type"],
                            "params": var.get("params", {}),
                            "source_snippet": match.get("trigger", "unknown")
                        })

        return global_vars

    def create_backup(self) -> Dict[str, Any]:
        backup_dir = Path.home() / ".espanso_companion" / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": "1.0",
            "timestamp": datetime.utcnow().isoformat(),
            "matchFiles": [],
            "configFiles": [],
        }
        for file in self._paths.match.glob("*.yml"):
            payload["matchFiles"].append({"name": file.name, "content": file.read_text(encoding="utf-8")})
        if self._paths.config.exists():
            for child in self._paths.config.rglob("*.yml"):
                payload["configFiles"].append({"name": str(child.relative_to(self._paths.config)), "content": child.read_text(encoding="utf-8")})
        backup_file = backup_dir / f"espanso-backup-{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.json"
        backup_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return {"path": str(backup_file), "count": len(payload["matchFiles"]) + len(payload["configFiles"])}

    def restart_espanso(self) -> Dict[str, Any]:
        result = self.cli.reload()
        return {"message": result.stdout.strip() or result.stderr.strip() or "Restart issued"}

    def get_feature_catalog(self) -> Dict[str, Any]:
        architecture = FeatureCatalog.describe_architecture()
        workflow = FeatureCatalog.describe_workflow()
        return {
            "architecture": [f"{section}: {', '.join(entries)}" for section, entries in architecture.items()],
            "requirements": _section_to_dict(FeatureCatalog.requirements),
            "workflow": {
                "title": "Workflow guidance",
                "items": self._build_workflow_items(workflow),
            },
            "integration": _section_to_dict(FeatureCatalog.integration_requirements),
            "ui": _section_to_dict(FeatureCatalog.ui_components),
            "variables": {
                "title": "Variable matrix",
                "types": [
                    f"{item['type']} ({item['editor']})"
                    for item in self.variable_engine.list_types()
                ],
                "methods": self.variable_engine.insertion_methods(),
                "insertionTitle": "Insertion methods",
            },
            "success": FeatureCatalog.success_criteria,
        }

    @staticmethod
    def _build_workflow_items(workflow: Dict[str, CatalogSection]) -> List[str]:
        items: List[str] = []
        for section in workflow.values():
            items.append(f"{section.title} — {section.description}")
            items.extend(section.items)
        return items


def main() -> None:
    api = EspansoAPI()
    html_path = Path(__file__).with_name("webview_ui") / "espanso_companion.html"
    window = webview.create_window(
        "Espanso Companion Pro",
        html=html_path.read_text(encoding="utf-8"),
        js_api=api,
        width=1360,
        height=900,
        min_size=(1000, 700),
    )
    webview.start(gui="edgechromium", debug=False, http_server=False)


if __name__ == "__main__":
    main()
