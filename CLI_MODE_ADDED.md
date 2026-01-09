# CLI Mode Added to Fabric GUI

## What's New

A new **CLI tab** has been added to the Fabric GUI, giving you direct command-line access while still using the web interface.

## Features

### CLI Tab
- Located between "Image Gen" and "Advanced" tabs
- Text area for entering raw fabric commands
- Built-in examples and usage hints
- Uses the same `/api/run` endpoint that was already available in the backend
- Same output display as other tabs (stdout/stderr/both)

### Usage

1. Click the **CLI** tab
2. Enter raw fabric command arguments (without "fabric" prefix)
3. Click **Run Pattern** button
4. View results in the output section

### Examples

You can enter commands like:
```
-p summarize
-p extract_wisdom -m claude-3-5-sonnet
-p analyze_claims --stream
-u https://example.com -p summarize
-y https://youtube.com/watch?v=xyz -p summarize_video
```

### Command Preview

The command preview box automatically updates to show:
```
fabric [your command]
```

## Technical Details

### Frontend Changes (static/index.html)
1. **Added CLI tab button** in the tabs section
2. **Added CLI tab content** with textarea for command input and usage examples
3. **Modified `runFabric()` function** to detect CLI mode and call `/api/run` endpoint
4. **Modified `updateCommandPreview()` function** to show CLI commands in preview
5. **Modified `clearAll()` function** to clear CLI command field

### Backend (No Changes Required)
The `/api/run` endpoint was already implemented at [main.py:467-509](main.py#L467-L509), accepting raw command arguments.

## How It Works

```
User enters: -p summarize -m gpt-4
↓
Frontend calls: POST /api/run with { "args": "-p summarize -m gpt-4" }
↓
Backend runs: fabric -p summarize -m gpt-4
↓
Returns: { stdout, stderr, returncode, command }
```

## Benefits

- **Flexibility**: Use any fabric CLI argument without waiting for GUI controls
- **Quick Testing**: Test commands before adding them to scripts
- **Full Coverage**: Access 100% of CLI features even if not in structured GUI
- **Same Interface**: Stay in the browser, use same output display

## Access

Simply refresh your browser at http://127.0.0.1:8000 to see the new CLI tab!

---

**Status**: ✅ Complete and ready to use
**Date**: January 8, 2026
