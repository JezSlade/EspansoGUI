"""Config discovery helpers for Espanso Companion Pro."""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, Optional


@dataclass
class ConfigPaths:
    config: Path
    match: Path
    packages: Path
    runtime: Path


class ConfigLoader:
    """Auto-detects Espanso directories with CLI and env fallbacks."""

    def __init__(self, runner: Callable = subprocess.run):
        self._runner = runner

    def discover_paths(self) -> ConfigPaths:
        """Return official workspace paths across platforms."""
        sys_name = platform.system()
        detected = self._probe_cli_paths()
        config = detected.get("config") or self._default_config_path(sys_name)
        match = detected.get("match") or config / "match"
        packages = detected.get("packages") or config.parent / "packages"
        runtime = detected.get("runtime") or config.parent / "run"

        return ConfigPaths(
            config=config,
            match=match,
            packages=packages,
            runtime=runtime,
        )

    def _probe_cli_paths(self) -> Dict[str, Path]:
        """Probe espanso CLI for paths with Windows .cmd -> .exe resolution."""
        result: Dict[str, Path] = {}
        try:
            # Find the actual executable (handles Windows .cmd wrapper issue)
            espanso_exe = self._find_espanso_executable()

            completed = self._runner(
                [espanso_exe, "path"],
                capture_output=True,
                text=True,
                check=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as exc:
            # Log the error but continue with fallback paths
            # This is intentional - we don't want to fail initialization
            return result

        for line in completed.stdout.splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip().lower().replace(" ", "_")
            result[key] = Path(value.strip())
        return result

    def _find_espanso_executable(self) -> str:
        """
        Find the actual espanso executable.

        On Windows, shutil.which() returns espanso.cmd, but subprocess.run()
        needs the actual .exe file for reliable output capture.
        """
        # First try to find espanso (will find .cmd on Windows)
        espanso_path = shutil.which("espanso")

        if not espanso_path:
            raise FileNotFoundError("espanso not found in PATH")

        # On Windows, if we found a .cmd file, look for the .exe in the same directory
        if platform.system() == "Windows" and espanso_path.lower().endswith('.cmd'):
            exe_path = Path(espanso_path).parent / "espansod.exe"
            if exe_path.exists():
                return str(exe_path)

        # For other platforms or if .exe not found, use what we found
        return espanso_path

    def _default_config_path(self, sys_name: str) -> Path:
        """Fallback for each OS plus environment overrides."""
        env_override = self._env_paths(
            "ESPANSO_CONFIG_DIR",
            "ESPANSO_RUNTIME_DIR",
            "ESPANSO_PACKAGE_DIR",
        )
        if env_override.get("config"):
            return env_override["config"]
        if sys_name == "Linux":
            return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "espanso"
        if sys_name == "Darwin":
            return Path.home() / "Library" / "Application Support" / "espanso"
        if sys_name == "Windows":
            return Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "espanso"
        raise RuntimeError("Unsupported platform")

    @staticmethod
    def _env_paths(*keys: str) -> Dict[str, Path]:
        result: Dict[str, Path] = {}
        for key in keys:
            value = os.environ.get(key)
            if value:
                result[key.lower()] = Path(value)
        return result

    @staticmethod
    def resolve_env_paths(paths: Iterable[Path]) -> Dict[str, Path]:
        """Ensure each path exists; create directories lazily."""
        resolved = {}
        for path in paths:
            resolved[str(path)] = path
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
        return resolved
