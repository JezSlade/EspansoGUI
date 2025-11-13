#!/usr/bin/env python3
"""Generate the comprehensive Espanso IDE HTML file."""

HTML_CONTENT = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Espanso IDE</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: #0d1117;
            color: #c9d1d9;
            height: 100vh;
            display: flex;
            overflow: hidden;
        }

        /* Sidebar */
        .sidebar {
            width: 200px;
            background: #161b22;
            border-right: 1px solid #30363d;
            display: flex;
            flex-direction: column;
            padding: 20px 10px;
        }
        .sidebar h1 {
            font-size: 18px;
            margin-bottom: 20px;
            padding: 0 10px;
        }
        .nav-btn {
            padding: 12px 15px;
            background: transparent;
            border: none;
            color: #c9d1d9;
            text-align: left;
            cursor: pointer;
            border-radius: 6px;
            margin-bottom: 5px;
            font-size: 14px;
        }
        .nav-btn:hover { background: #21262d; }
        .nav-btn.active { background: #1f6feb; color: #fff; }

        /* Main Content */
        .main {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        /* Views */
        .view {
            display: none;
            flex-direction: column;
            height: 100%;
            padding: 20px;
            overflow-y: auto;
        }
        .view.active { display: flex; }

        /* Status Bar */
        .status-bar {
            background: #161b22;
            border-bottom: 1px solid #30363d;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .status-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-indicator.connected { background: #3fb950; }
        .status-indicator.disconnected { background: #f85149; }

        /* Dashboard */
        .dash-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .dash-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 20px;
        }
        .dash-card h3 {
            font-size: 14px;
            color: #8b949e;
            margin-bottom: 10px;
        }
        .dash-card .value {
            font-size: 24px;
            font-weight: 600;
            color: #58a6ff;
        }
        .btn {
            background: #238636;
            color: #fff;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            margin-right: 8px;
            margin-bottom: 8px;
        }
        .btn:hover { background: #2ea043; }
        .btn.danger { background: #da3633; }
        .btn.danger:hover { background: #f85149; }
        .btn.secondary { background: #21262d; }
        .btn.secondary:hover { background: #30363d; }

        /* Snippet IDE */
        .snippet-ide {
            display: grid;
            grid-template-columns: 1fr 350px;
            gap: 20px;
            height: calc(100vh - 120px);
        }
        .editor-main {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .editor-toolbar {
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }
        .input-group {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        .input-group label {
            font-size: 12px;
            color: #8b949e;
            font-weight: 600;
        }
        .input-group input, .input-group select, .input-group textarea {
            padding: 8px 12px;
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            color: #c9d1d9;
            font-size: 14px;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        .input-group input:focus, .input-group select:focus, .input-group textarea:focus {
            outline: none;
            border-color: #58a6ff;
        }
        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 0;
        }
        .checkbox-group input[type="checkbox"] {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }
        .replacement-editor {
            flex: 1;
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 15px;
            color: #c9d1d9;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            line-height: 1.6;
            resize: none;
        }
        .replacement-editor:focus {
            outline: none;
            border-color: #58a6ff;
        }

        /* Snippet List */
        .snippet-list {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 15px;
            overflow-y: auto;
            max-height: calc(100vh - 120px);
        }
        .snippet-list h3 {
            margin-bottom: 15px;
            color: #58a6ff;
        }
        .snippet-item {
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .snippet-item:hover {
            border-color: #58a6ff;
            background: #161b22;
        }
        .snippet-item.active {
            border-color: #1f6feb;
            background: #1c2532;
        }
        .snippet-trigger {
            font-weight: 600;
            color: #58a6ff;
            margin-bottom: 4px;
            font-family: monospace;
        }
        .snippet-preview {
            color: #8b949e;
            font-size: 12px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        /* Variable Builder */
        .variable-builder {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 15px;
            margin-top: 15px;
        }
        .variable-builder h4 {
            margin-bottom: 15px;
            color: #58a6ff;
        }
        .variable-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 15px;
        }
        .variable-card {
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .variable-info {
            flex: 1;
        }
        .variable-name {
            font-weight: 600;
            color: #58a6ff;
            font-family: monospace;
        }
        .variable-type {
            font-size: 11px;
            color: #8b949e;
        }
        .variable-actions {
            display: flex;
            gap: 5px;
        }
        .btn-small {
            padding: 4px 8px;
            font-size: 12px;
            background: #21262d;
            border: none;
            color: #c9d1d9;
            border-radius: 4px;
            cursor: pointer;
        }
        .btn-small:hover { background: #30363d; }
        .btn-small.danger { background: #da3633; }
        .btn-small.danger:hover { background: #f85149; }

        /* Variable Type Selector */
        .type-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-bottom: 15px;
        }
        .type-btn {
            padding: 10px;
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            color: #c9d1d9;
            cursor: pointer;
            text-align: center;
            transition: all 0.2s;
            font-size: 12px;
        }
        .type-btn:hover {
            border-color: #58a6ff;
            background: #161b22;
        }
        .type-btn.active {
            border-color: #1f6feb;
            background: #1c2532;
        }

        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        .modal.active { display: flex; }
        .modal-content {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 20px;
            max-width: 500px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .modal-header h3 {
            color: #58a6ff;
        }
        .modal-close {
            background: transparent;
            border: none;
            color: #8b949e;
            font-size: 24px;
            cursor: pointer;
            padding: 0;
            width: 30px;
            height: 30px;
        }
        .modal-close:hover { color: #c9d1d9; }

        /* Toast */
        .toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #238636;
            color: #fff;
            padding: 12px 20px;
            border-radius: 6px;
            display: none;
            z-index: 1000;
        }
        .toast.show { display: block; }
        .toast.error { background: #da3633; }

        /* YAML Editor */
        #yaml-editor {
            flex: 1;
            width: 100%;
            background: #0d1117;
            color: #c9d1d9;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 15px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            line-height: 1.5;
            resize: none;
        }

        /* Search */
        .search-box {
            width: 100%;
            padding: 10px;
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            color: #c9d1d9;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
'''

# Write the HTML file
output_path = r"c:\Users\jez.slade\Desktop\Projects\Espanso Enhancifier\webview_ui\espanso_ide.html"

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(HTML_CONTENT)
    # Continue with body content...
    f.write('''
    <!-- Sidebar -->
    <div class="sidebar">
        <h1>Espanso IDE</h1>
        <button class="nav-btn active" data-view="dashboard">Dashboard</button>
        <button class="nav-btn" data-view="snippet-ide">Snippet IDE</button>
        <button class="nav-btn" data-view="yaml-editor">YAML Editor</button>
        <button class="nav-btn" data-view="snippets">All Snippets</button>
    </div>

    <!-- Main Content -->
    <div class="main">
        <!-- Status Bar -->
        <div class="status-bar">
            <div>
                <span class="status-indicator" id="connection-indicator"></span>
                <span id="status-text">Connecting...</span>
            </div>
            <div id="snippet-count">0 snippets</div>
        </div>

        <!-- Dashboard View -->
        <div class="view active" id="dashboard-view">
            <h2 style="margin-bottom: 20px;">Espanso Control Panel</h2>
            <div class="dash-grid">
                <div class="dash-card">
                    <h3>Service Status</h3>
                    <div class="value" id="service-status">Unknown</div>
                </div>
                <div class="dash-card">
                    <h3>Snippets</h3>
                    <div class="value" id="total-snippets">0</div>
                </div>
                <div class="dash-card">
                    <h3>Config Path</h3>
                    <div class="value" id="config-path" style="font-size: 12px; word-break: break-all;">-</div>
                </div>
            </div>
            <div style="margin-top: 20px;">
                <h3 style="margin-bottom: 10px;">Service Controls</h3>
                <button class="btn" id="btn-start">Start Espanso</button>
                <button class="btn" id="btn-stop">Stop Espanso</button>
                <button class="btn" id="btn-restart">Restart Espanso</button>
                <button class="btn" id="btn-refresh">Refresh Data</button>
            </div>
        </div>

        <!-- Snippet IDE View -->
        <div class="view" id="snippet-ide-view">
            <h2 style="margin-bottom: 15px;">Snippet IDE</h2>
            <div class="snippet-ide">
                <div class="editor-main">
                    <div class="editor-toolbar">
                        <div class="input-group" style="max-width: 300px;">
                            <label>Trigger</label>
                            <input type="text" id="snippet-trigger" placeholder=":example">
                        </div>
                        <div class="checkbox-group">
                            <input type="checkbox" id="snippet-word">
                            <label>Word boundary</label>
                        </div>
                        <div class="checkbox-group">
                            <input type="checkbox" id="snippet-propagate-case">
                            <label>Propagate case</label>
                        </div>
                    </div>
                    <div style="flex: 1; display: flex; flex-direction: column;">
                        <label style="font-size: 12px; color: #8b949e; font-weight: 600; margin-bottom: 5px;">Replacement</label>
                        <textarea class="replacement-editor" id="snippet-replace" placeholder="Type your replacement text here...

Use {{variable_name}} to insert variables
Use $|$ to mark cursor position"></textarea>
                    </div>
                    <div class="variable-builder">
                        <h4>Variables <button class="btn-small" id="btn-add-var">+ Add Variable</button></h4>
                        <div class="variable-list" id="variable-list"></div>
                    </div>
                    <div style="display: flex; gap: 10px;">
                        <button class="btn" id="btn-save-snippet">Save Snippet</button>
                        <button class="btn secondary" id="btn-new-snippet">New Snippet</button>
                        <button class="btn danger" id="btn-delete-snippet">Delete</button>
                        <span id="snippet-editor-status" style="margin-left: 15px; color: #8b949e; align-self: center;"></span>
                    </div>
                </div>
                <div class="snippet-list">
                    <h3>Your Snippets</h3>
                    <input type="text" id="snippet-search" class="search-box" placeholder="Search snippets...">
                    <div id="snippet-list-items"></div>
                </div>
            </div>
        </div>

        <!-- YAML Editor View -->
        <div class="view" id="yaml-editor-view">
            <h2 style="margin-bottom: 15px;">base.yaml Editor</h2>
            <div style="margin-bottom: 10px; display: flex; gap: 10px;">
                <button class="btn" id="btn-save-yaml">Save & Reload</button>
                <button class="btn secondary" id="btn-reload-yaml">Reload from Disk</button>
                <span id="editor-status" style="margin-left: 15px; color: #8b949e; align-self: center;"></span>
            </div>
            <textarea id="yaml-editor" placeholder="Loading base.yaml..."></textarea>
        </div>

        <!-- All Snippets View -->
        <div class="view" id="snippets-view">
            <h2 style="margin-bottom: 15px;">All Snippets</h2>
            <input type="text" id="search-snippets" class="search-box" placeholder="Search snippets...">
            <div id="snippets-list" style="display: grid; gap: 10px;"></div>
        </div>
    </div>
''')

print(f"Generated IDE HTML structure at: {output_path}")
print("File size check... continuing with JavaScript...")
