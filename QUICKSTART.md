# Fabric GUI - Quick Start Guide

## 🚀 Launch the App

### Method 1: Desktop Icon (macOS)
1. Double-click **Fabric GUI.app** on Desktop
2. Browser opens automatically to http://127.0.0.1:8000
3. Start using immediately!

### Method 2: Terminal
```bash
cd fabric-gui
./start.sh
# Then open: http://127.0.0.1:8000
```

## 📝 Basic Usage (3 Steps)

### Step 1: Choose a Pattern
Click the **Pattern** dropdown or search box
- Type to search (e.g., "summarize", "extract", "analyze")
- Click to select from 233+ patterns

### Step 2: Add Your Input
Choose an input method (tabs):
- **Text**: Paste or type content
- **URL**: Enter a web page URL
- **YouTube**: Paste a YouTube video link
- **Raw CLI**: Advanced command-line arguments

### Step 3: Run
Click **"Run Pattern"** button
- Watch the loading indicator
- Results appear in the Output section below
- Copy or download as needed

## 💡 Pro Tips

### Quick Patterns to Try
```
extract_wisdom       - Pull key insights from text
summarize           - Create concise summaries  
analyze_paper       - Analyze academic papers
create_summary      - Generate executive summaries
improve_writing     - Enhance your text
explain_code        - Understand code snippets
```

### Use Command Preview
- See exactly what command will run
- Located below input area
- Updates in real-time as you change options

### Try Dry Run Mode
1. Expand **"Advanced Options"**
2. Check **"Dry run"**
3. Run to preview without executing
4. See the full prompt that would be sent

### Model Selection
- Choose specific AI models (Claude, GPT-4, etc.)
- Select vendor if needed
- Leave blank for default model

### Temperature Control
- 0.0 = Very focused, deterministic
- 0.7 = Balanced (default)
- 1.0-2.0 = More creative, varied

## 🎯 Common Workflows

### Workflow 1: Summarize a YouTube Video
```
1. Select pattern: "summarize"
2. Click YouTube tab
3. Paste: https://youtube.com/watch?v=VIDEO_ID
4. Click "Run Pattern"
5. Copy output when done
```

### Workflow 2: Extract Wisdom from Article
```
1. Select pattern: "extract_wisdom"
2. Stay on Text tab
3. Paste article text
4. Click "Run Pattern"
5. Download result as text file
```

### Workflow 3: Analyze with Specific Model
```
1. Select pattern: "analyze_paper"
2. Choose model: "claude-sonnet-4-5"
3. Paste paper content
4. Expand Advanced Options
5. Set temperature: 0.3 (for focused analysis)
6. Enable "Web search" if needed
7. Click "Run Pattern"
```

### Workflow 4: Test Command First
```
1. Configure your pattern and options
2. Check "Command Preview" box
3. Expand "Advanced Options"
4. Check "Dry run"
5. Click "Run Pattern"
6. Review what would be sent
7. Uncheck "Dry run" to run for real
```

## ⚙️ Advanced Options Explained

### Temperature (0.0 - 2.0)
Controls creativity/randomness of output

### Stream
Show output as it's generated (real-time)

### Copy to Clipboard
Automatically copy result to clipboard

### Web Search
Enable web search for supported models (Anthropic, OpenAI, Gemini)

### Dry Run
Preview the full prompt without sending to AI

## 🔧 Troubleshooting

### Pattern List Empty?
- Check if fabric is installed: `fabric --listpatterns`
- Restart the server
- Check browser console for errors

### "fabric not found" Error?
- Install fabric: `go install github.com/danielmiessler/fabric@latest`
- Add to PATH or place in `~/go/bin/`
- Restart the app

### Output Not Showing?
- Check the "Errors" tab for error messages
- Verify pattern name is correct
- Try dry run to see what would be sent

## 📚 Learning Resources

- **Fabric GitHub**: https://github.com/danielmiessler/Fabric
- **Pattern Explanations**: Check fabric's documentation
- **Pattern List**: Run `fabric --listpatterns` in terminal

## 🎨 Interface Tour

```
┌─────────────────────────────────────────────────┐
│  FABRIC GUI HEADER                              │
│  Enhanced interface for 233+ patterns           │
└─────────────────────────────────────────────────┘

┌──────────────────────┬──────────────────────────┐
│ PATTERN & CONFIG     │ INPUT                    │
│                      │                          │
│ • Pattern search     │ [Text][URL][YT][Raw CLI]│
│ • Pattern dropdown   │                          │
│ • Model selection    │ Input area here...       │
│ • Vendor selection   │                          │
│ • Context/Session    │ Command Preview:         │
│ • Advanced Options   │ fabric -p pattern...     │
│   - Temperature      │                          │
│   - Stream          │ [Run Pattern] [Clear]    │
│   - Copy            │                          │
│   - Search          │ Status: Ready            │
│   - Dry run         │                          │
└──────────────────────┴──────────────────────────┘

┌─────────────────────────────────────────────────┐
│ OUTPUT                                          │
│                                                 │
│ [Copy Output] [Download]                        │
│ [Result][Errors][Both]                          │
│                                                 │
│ Output displays here...                         │
│                                                 │
└─────────────────────────────────────────────────┘
```

## ⌨️ Keyboard Tips

- **Tab**: Navigate between fields
- **Enter** in search: Filter patterns
- **Ctrl/Cmd + C**: Copy from output
- **Escape**: Clear search

## 🔄 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Port 8000 in use | Kill old server: `pkill -f uvicorn` |
| Patterns not loading | Check fabric installation |
| Slow response | Pattern is running, wait for completion |
| Empty output | Check Errors tab |
| Can't copy output | Use Download button instead |

## 📱 Access from Other Devices

The server binds to 127.0.0.1 (localhost only). To access from other devices:

```bash
# Start with 0.0.0.0 to allow network access
uvicorn main:app --host 0.0.0.0 --port 8000

# Then access from other devices:
# http://YOUR_IP:8000
```

⚠️ **Security Note**: Only do this on trusted networks!

## 🎉 You're Ready!

Now you have a powerful GUI for Fabric. Explore the 233+ patterns and discover what works best for your workflow!

**Happy pattern running! 🚀**
