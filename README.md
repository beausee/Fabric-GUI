# Fabric GUI - Enhanced Interface

A modern, feature-rich web GUI for the [Fabric AI Framework](https://github.com/danielmiessler/Fabric) by Daniel Miessler.

## Features

### 🎨 Modern Interface
- Clean, dark-themed UI with gradient accents
- Responsive layout optimized for productivity
- Real-time command preview
- Collapsible advanced options

### 🧩 Pattern Management
- Browse all 233+ Fabric patterns
- Searchable pattern list
- Quick pattern selection with visual feedback
- Pattern descriptions on selection

### 📊 Model & Provider Support
- Select from available AI models
- Choose AI vendor/provider
- Configure temperature and other parameters
- Context and session management

### 📥 Multiple Input Methods
- **Text Input**: Direct text entry
- **URL Scraping**: Process web content via Jina AI
- **YouTube**: Extract transcripts from videos
- **Raw CLI**: Advanced mode for direct CLI arguments

### ⚙️ Advanced Options
- Temperature control (0.0 - 2.0)
- Stream output in real-time
- Copy to clipboard automatically
- Enable web search for supported models
- Dry run mode (preview what will be sent)
- Context and session management

### 📤 Output Features
- Copy output with one click
- Download results as text file
- Separate tabs for stdout/stderr/both
- Syntax-friendly monospace display
- Scrollable output with max height

## Installation

### Prerequisites
- Python 3.12+
- [Fabric CLI](https://github.com/danielmiessler/Fabric) installed and configured
- Fabric should be accessible via PATH or installed in `~/go/bin/fabric`

### Setup

1. Clone or download this repository:
```bash
cd fabric-gui
```

2. Create a virtual environment:
```bash
python3 -m venv venv
```

3. Activate and install dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

4. Run the server:
```bash
./start.sh
# Or manually:
uvicorn main:app --host 127.0.0.1 --port 8000
```

5. Open your browser to:
```
http://127.0.0.1:8000
```

## macOS App

Double-click the **Fabric GUI.app** on your Desktop to:
- Automatically start the server
- Open the GUI in your default browser
- Keep running until you quit

## Usage

### Quick Start

1. **Select a Pattern**: Use the search box or dropdown to find a pattern (e.g., "extract_wisdom", "summarize")
2. **Choose Input Method**: Switch between Text, URL, YouTube, or Raw CLI tabs
3. **Enter Your Input**: Type or paste content
4. **Configure Options** (optional): Select model, adjust temperature, enable features
5. **Run Pattern**: Click "Run Pattern" button
6. **View Results**: Output appears in the bottom panel

### Example Workflows

**Summarize a YouTube video:**
1. Select pattern: `summarize`
2. Switch to YouTube tab
3. Paste video URL
4. Click Run Pattern

**Extract wisdom from text:**
1. Select pattern: `extract_wisdom`
2. Stay on Text tab
3. Paste article or notes
4. Click Run Pattern

**Analyze with specific model:**
1. Select pattern: `analyze_paper`
2. Choose model: `claude-sonnet-4-5`
3. Enter text
4. Enable web search if needed
5. Click Run Pattern

## API Endpoints

The backend provides these endpoints:

- `GET /` - Serve the GUI
- `GET /api/patterns` - List all patterns
- `GET /api/models` - List all models
- `GET /api/vendors` - List all vendors
- `GET /api/contexts` - List all contexts
- `GET /api/sessions` - List all sessions
- `POST /api/pattern/run` - Run pattern with structured request
- `POST /api/run` - Run with raw CLI arguments
- `GET /api/help` - Get fabric help output

## Architecture

```
fabric-gui/
├── main.py              # FastAPI backend
├── static/
│   └── index.html       # Enhanced single-page app
├── venv/                # Python virtual environment
├── start.sh             # Startup script
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Technologies

- **Backend**: FastAPI (Python)
- **Frontend**: Vanilla JavaScript (no frameworks)
- **Styling**: Custom CSS with dark theme
- **AI Framework**: Fabric CLI

## Features Implemented

✅ Pattern browser with search
✅ Model and vendor selection  
✅ Context and session management
✅ Temperature control
✅ Multiple input methods (Text, URL, YouTube, Raw CLI)
✅ Advanced options (stream, copy, search, dry-run)
✅ Real-time command preview
✅ Output copy/download
✅ Separate output tabs
✅ Collapsible sections
✅ Loading indicators
✅ Error handling
✅ Auto-detection of fabric binary

## Troubleshooting

**"fabric not found" error:**
- Ensure Fabric is installed: `go install github.com/danielmiessler/fabric@latest`
- Check if fabric is in PATH: `which fabric`
- The app checks common locations: `~/go/bin/fabric`, `/usr/local/bin/fabric`

**Port already in use:**
```bash
# Kill existing server
pkill -f "uvicorn main:app"
# Or use a different port
uvicorn main:app --host 127.0.0.1 --port 8001
```

**Patterns not loading:**
- Verify fabric works: `fabric --listpatterns`
- Check server logs for errors
- Ensure fabric is configured: `fabric --setup`

## Credits

- **Fabric Framework**: [Daniel Miessler](https://github.com/danielmiessler/Fabric)
- **GUI Development**: Enhanced interface with modern features
- **Original GUI**: Simple CLI wrapper concept

## License

This GUI is a wrapper around the Fabric CLI. Fabric itself is licensed under MIT.

## Contributing

Suggestions and improvements welcome! This is a local development tool.

## Roadmap

Future enhancements:
- [ ] Pattern variable auto-detection and input fields
- [ ] Pattern descriptions from fabric metadata
- [ ] History of recent runs
- [ ] Favorites/bookmarks for patterns
- [ ] Multi-tab support for parallel runs
- [ ] Batch processing queue
- [ ] Export as markdown/PDF
- [ ] Settings page for fabric configuration
- [ ] File upload support
- [ ] Syntax highlighting for code outputs
