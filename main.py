import subprocess
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow browser JS to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for local use, this is fine
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Helper function to find the fabric binary
def get_fabric_path():
    """
    Find the fabric binary. First checks PATH, then checks common locations.
    Returns the path to fabric or None if not found.
    """
    # First try to find it in PATH
    fabric_path = subprocess.run(
        ["which", "fabric"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if fabric_path.returncode == 0:
        return fabric_path.stdout.strip()

    # Check common installation locations
    common_paths = [
        os.path.expanduser("~/go/bin/fabric"),
        "/usr/local/bin/fabric",
        "/usr/bin/fabric",
        os.path.expanduser("~/.local/bin/fabric"),
    ]

    for path in common_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    return None


FABRIC_PATH = get_fabric_path()


class FabricRunRequest(BaseModel):
    # Raw arguments string the user types, e.g.:
    #   "-p 'summarize this' input.txt"
    args: str


class FabricPatternRequest(BaseModel):
    # Structured pattern execution request with ALL fabric CLI parameters

    # Pattern & Model
    pattern: str | None = None
    model: str | None = None
    vendor: str | None = None

    # Input Methods
    input_text: str | None = None
    input_url: str | None = None
    youtube_url: str | None = None
    attachment: str | None = None  # -a for vision models

    # Model Parameters
    temperature: float | None = None  # -t
    top_p: float | None = None  # -T
    presence_penalty: float | None = None  # -P
    frequency_penalty: float | None = None  # -F
    seed: int | None = None  # -e
    raw_mode: bool = False  # -r

    # Context & Sessions
    context: str | None = None  # -C
    session: str | None = None  # --session

    # Variables
    variables: dict[str, str] | None = None  # -v
    input_has_vars: bool = False  # --input-has-vars
    no_variable_replacement: bool = False  # --no-variable-replacement

    # YouTube Advanced
    youtube_playlist: bool = False  # --playlist
    youtube_transcript_timestamps: bool = False  # --transcript-with-timestamps
    youtube_comments: bool = False  # --comments
    youtube_metadata: bool = False  # --metadata
    yt_dlp_args: str | None = None  # --yt-dlp-args

    # Web Scraping
    scrape_question: str | None = None  # -q
    readability: bool = False  # --readability
    search_location: str | None = None  # --search-location

    # Media Processing
    transcribe_file: str | None = None  # --transcribe-file
    transcribe_model: str | None = None  # --transcribe-model
    split_media: bool = False  # --split-media-file

    # Output Options
    output_file: str | None = None  # -o
    output_session: bool = False  # --output-session
    copy: bool = False  # -c
    stream: bool = False  # -s

    # Image Generation
    image_file: str | None = None  # --image-file
    image_size: str | None = None  # --image-size
    image_quality: str | None = None  # --image-quality
    image_compression: int | None = None  # --image-compression
    image_background: str | None = None  # --image-background

    # TTS
    voice: str | None = None  # --voice

    # Thinking/Reasoning
    thinking: str | None = None  # --thinking
    suppress_think: bool = False  # --suppress-think
    think_start_tag: str | None = None  # --think-start-tag
    think_end_tag: str | None = None  # --think-end-tag

    # Advanced Options
    language: str | None = None  # -g
    search: bool = False  # --search
    dry_run: bool = False  # --dry-run
    notification: bool = False  # --notification
    notification_command: str | None = None  # --notification-command
    debug: int | None = None  # --debug

    # Strategy & Extensions
    strategy: str | None = None  # --strategy

    # API Options
    disable_responses_api: bool = False  # --disable-responses-api
    model_context_length: int | None = None  # --modelContextLength


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serve the main HTML page."""
    index_path = Path("static/index.html")
    if not index_path.exists():
        raise HTTPException(status_code=500, detail="index.html not found")
    return index_path.read_text(encoding="utf-8")


@app.get("/api/help", response_class=HTMLResponse)
async def fabric_help():
    """Return `fabric --help` output as HTML."""
    if not FABRIC_PATH:
        raise HTTPException(
            status_code=500,
            detail="fabric not found. Please ensure fabric is installed and accessible.",
        )

    try:
        result = subprocess.run(
            [FABRIC_PATH, "--help"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail=f"fabric not found at {FABRIC_PATH}. Is it installed?",
        )

    # Simple HTML-preformatted block
    return f"<pre>{result.stdout}</pre>"


@app.get("/api/patterns")
async def list_patterns():
    """List all available fabric patterns."""
    if not FABRIC_PATH:
        raise HTTPException(status_code=500, detail="fabric not found.")

    try:
        result = subprocess.run(
            [FABRIC_PATH, "--listpatterns"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return {"patterns": [], "error": result.stderr}

        # Parse patterns (one per line)
        patterns = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        return {"patterns": patterns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/models")
async def list_models():
    """List all available models."""
    if not FABRIC_PATH:
        raise HTTPException(status_code=500, detail="fabric not found.")

    try:
        result = subprocess.run(
            [FABRIC_PATH, "--listmodels"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return {"models": [], "error": result.stderr}

        # Parse models (one per line)
        models = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/vendors")
async def list_vendors():
    """List all available AI vendors."""
    if not FABRIC_PATH:
        raise HTTPException(status_code=500, detail="fabric not found.")

    try:
        result = subprocess.run(
            [FABRIC_PATH, "--listvendors"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return {"vendors": [], "error": result.stderr}

        # Parse vendors (one per line)
        vendors = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        return {"vendors": vendors}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/contexts")
async def list_contexts():
    """List all available contexts."""
    if not FABRIC_PATH:
        raise HTTPException(status_code=500, detail="fabric not found.")

    try:
        result = subprocess.run(
            [FABRIC_PATH, "--listcontexts"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return {"contexts": [], "error": result.stderr}

        contexts = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        return {"contexts": contexts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sessions")
async def list_sessions():
    """List all available sessions."""
    if not FABRIC_PATH:
        raise HTTPException(status_code=500, detail="fabric not found.")

    try:
        result = subprocess.run(
            [FABRIC_PATH, "--listsessions"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return {"sessions": [], "error": result.stderr}

        sessions = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        return {"sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/pattern/run")
async def run_pattern(req: FabricPatternRequest):
    """Run fabric with structured pattern request - supports ALL CLI parameters."""
    if not FABRIC_PATH:
        raise HTTPException(status_code=500, detail="fabric not found.")

    # Build command arguments
    cmd = [FABRIC_PATH]

    # Pattern & Model
    if req.pattern:
        cmd.extend(["-p", req.pattern])
    if req.model:
        cmd.extend(["-m", req.model])
    if req.vendor:
        cmd.extend(["-V", req.vendor])

    # Model Parameters
    if req.temperature is not None:
        cmd.extend(["-t", str(req.temperature)])
    if req.top_p is not None:
        cmd.extend(["-T", str(req.top_p)])
    if req.presence_penalty is not None:
        cmd.extend(["-P", str(req.presence_penalty)])
    if req.frequency_penalty is not None:
        cmd.extend(["-F", str(req.frequency_penalty)])
    if req.seed is not None:
        cmd.extend(["-e", str(req.seed)])
    if req.raw_mode:
        cmd.append("-r")
    if req.model_context_length is not None:
        cmd.extend(["--modelContextLength", str(req.model_context_length)])

    # Context & Sessions
    if req.context:
        cmd.extend(["-C", req.context])
    if req.session:
        cmd.extend(["--session", req.session])

    # Variables
    if req.variables:
        for key, value in req.variables.items():
            cmd.extend(["-v", f"{key}:{value}"])
    if req.input_has_vars:
        cmd.append("--input-has-vars")
    if req.no_variable_replacement:
        cmd.append("--no-variable-replacement")

    # Input Methods
    if req.youtube_url:
        cmd.extend(["-y", req.youtube_url])
    if req.input_url:
        cmd.extend(["-u", req.input_url])
    if req.attachment:
        cmd.extend(["-a", req.attachment])

    # YouTube Advanced
    if req.youtube_playlist:
        cmd.append("--playlist")
    if req.youtube_transcript_timestamps:
        cmd.append("--transcript-with-timestamps")
    if req.youtube_comments:
        cmd.append("--comments")
    if req.youtube_metadata:
        cmd.append("--metadata")
    if req.yt_dlp_args:
        cmd.extend(["--yt-dlp-args", req.yt_dlp_args])

    # Web Scraping
    if req.scrape_question:
        cmd.extend(["-q", req.scrape_question])
    if req.readability:
        cmd.append("--readability")
    if req.search_location:
        cmd.extend(["--search-location", req.search_location])

    # Media Processing
    if req.transcribe_file:
        cmd.extend(["--transcribe-file", req.transcribe_file])
    if req.transcribe_model:
        cmd.extend(["--transcribe-model", req.transcribe_model])
    if req.split_media:
        cmd.append("--split-media-file")

    # Output Options
    if req.output_file:
        cmd.extend(["-o", req.output_file])
    if req.output_session:
        cmd.append("--output-session")
    if req.copy:
        cmd.append("-c")
    if req.stream:
        cmd.append("-s")

    # Image Generation
    if req.image_file:
        cmd.extend(["--image-file", req.image_file])
    if req.image_size:
        cmd.extend(["--image-size", req.image_size])
    if req.image_quality:
        cmd.extend(["--image-quality", req.image_quality])
    if req.image_compression is not None:
        cmd.extend(["--image-compression", str(req.image_compression)])
    if req.image_background:
        cmd.extend(["--image-background", req.image_background])

    # TTS
    if req.voice:
        cmd.extend(["--voice", req.voice])

    # Thinking/Reasoning
    if req.thinking:
        cmd.extend(["--thinking", req.thinking])
    if req.suppress_think:
        cmd.append("--suppress-think")
    if req.think_start_tag:
        cmd.extend(["--think-start-tag", req.think_start_tag])
    if req.think_end_tag:
        cmd.extend(["--think-end-tag", req.think_end_tag])

    # Advanced Options
    if req.language:
        cmd.extend(["-g", req.language])
    if req.search:
        cmd.append("--search")
    if req.dry_run:
        cmd.append("--dry-run")
    if req.notification:
        cmd.append("--notification")
    if req.notification_command:
        cmd.extend(["--notification-command", req.notification_command])
    if req.debug is not None:
        cmd.extend(["--debug", str(req.debug)])

    # Strategy & Extensions
    if req.strategy:
        cmd.extend(["--strategy", req.strategy])

    # API Options
    if req.disable_responses_api:
        cmd.append("--disable-responses-api")

    # Prepare stdin if text input provided
    stdin_input = req.input_text if req.input_text else None

    try:
        result = subprocess.run(
            cmd,
            input=stdin_input,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "command": " ".join(cmd),
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


@app.post("/api/run")
async def run_fabric(req: FabricRunRequest):
    """
    Run the fabric CLI with whatever args the user typed.
    Example: args = "-p 'my prompt' file.txt"
    """
    if not FABRIC_PATH:
        raise HTTPException(
            status_code=500,
            detail="fabric not found. Please ensure fabric is installed and accessible.",
        )

    # VERY simple splitting; for a first version this is OK.
    # Later we can build structured forms instead of raw args.
    import shlex

    try:
        arg_list = shlex.split(req.args)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Could not parse args: {e}")

    cmd = [FABRIC_PATH, *arg_list]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail=f"fabric not found at {FABRIC_PATH}. Is it installed?",
        )

    return {
        "command": " ".join(cmd),
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


# Context/Session Management
@app.post("/api/context/wipe")
async def wipe_context(context_name: str):
    """Wipe a specific context."""
    if not FABRIC_PATH:
        raise HTTPException(status_code=500, detail="fabric not found.")

    try:
        result = subprocess.run(
            [FABRIC_PATH, "-w", context_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return {
            "success": result.returncode == 0,
            "message": result.stdout or result.stderr
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/session/wipe")
async def wipe_session(session_name: str):
    """Wipe a specific session."""
    if not FABRIC_PATH:
        raise HTTPException(status_code=500, detail="fabric not found.")

    try:
        result = subprocess.run(
            [FABRIC_PATH, "-W", session_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return {
            "success": result.returncode == 0,
            "message": result.stdout or result.stderr
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/context/print")
async def print_context(context_name: str):
    """Print context content."""
    if not FABRIC_PATH:
        raise HTTPException(status_code=500, detail="fabric not found.")

    try:
        result = subprocess.run(
            [FABRIC_PATH, "--printcontext", context_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return {
            "content": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/session/print")
async def print_session(session_name: str):
    """Print session content."""
    if not FABRIC_PATH:
        raise HTTPException(status_code=500, detail="fabric not found.")

    try:
        result = subprocess.run(
            [FABRIC_PATH, "--printsession", session_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return {
            "content": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Pattern Management
@app.post("/api/patterns/update")
async def update_patterns():
    """Update patterns from repository."""
    if not FABRIC_PATH:
        raise HTTPException(status_code=500, detail="fabric not found.")

    try:
        result = subprocess.run(
            [FABRIC_PATH, "-U"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return {
            "success": result.returncode == 0,
            "message": result.stdout or result.stderr
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Additional List Endpoints
@app.get("/api/strategies")
async def list_strategies():
    """List all available strategies."""
    if not FABRIC_PATH:
        raise HTTPException(status_code=500, detail="fabric not found.")

    try:
        result = subprocess.run(
            [FABRIC_PATH, "--liststrategies"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return {"strategies": [], "error": result.stderr}

        strategies = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        return {"strategies": strategies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/extensions")
async def list_extensions():
    """List all registered extensions."""
    if not FABRIC_PATH:
        raise HTTPException(status_code=500, detail="fabric not found.")

    try:
        result = subprocess.run(
            [FABRIC_PATH, "--listextensions"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return {"extensions": [], "error": result.stderr}

        extensions = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        return {"extensions": extensions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/voices")
async def list_voices():
    """List all available Gemini TTS voices."""
    if not FABRIC_PATH:
        raise HTTPException(status_code=500, detail="fabric not found.")

    try:
        result = subprocess.run(
            [FABRIC_PATH, "--list-gemini-voices"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return {"voices": [], "error": result.stderr}

        voices = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        return {"voices": voices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/transcription-models")
async def list_transcription_models():
    """List all available transcription models."""
    if not FABRIC_PATH:
        raise HTTPException(status_code=500, detail="fabric not found.")

    try:
        result = subprocess.run(
            [FABRIC_PATH, "--list-transcription-models"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return {"models": [], "error": result.stderr}

        models = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# For serving any extra static files if needed later
@app.get("/static/{filename}")
async def static_files(filename: str):
    path = Path("static") / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path)

