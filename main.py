from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import shutil
import os
import uuid

from mood_model import detect_mood
from chakra_raga import chakra_raga_map
from speech_to_text import speech_to_text
from storyteller import generate_story_with_voice

# ── Config ──────────────────────────────────────────────
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


# ── App ──────────────────────────────────────────────────
app = FastAPI(
    title="SoulSync API",
    description="Mood-based chakra & raga healing — powered by AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/audio",   StaticFiles(directory="audio"),   name="audio")
app.mount("/stories", StaticFiles(directory="stories"), name="stories")

# ── Pydantic Models ──────────────────────────────────────
class TextInput(BaseModel):
    text: str

class MoodInput(BaseModel):
    mood: str = "stressed"

# ── Helper ───────────────────────────────────────────────
def build_mood_response(text: str, mood: str) -> dict:
    """Build the standard mood response dict."""
    if mood not in chakra_raga_map:
        mood = "stressed"   # safe fallback
    info = chakra_raga_map[mood]
    return {
        "text": text,
        "mood": mood,
        "chakra": info["chakra"],
        "raga":   info["raga"],
        "audio":  BASE_URL + info["audio"],
    }

# ── Routes ───────────────────────────────────────────────
@app.get("/")
def home():
    return {"status": "SoulSync API running", "version": "1.0.0"}

@app.get("/health")
def health():
    """Quick health-check endpoint."""
    return {"ok": True}


@app.post("/analyze-text")
def analyze_text(data: TextInput):
    """Detect mood from text and return chakra + raga info."""
    text = data.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    mood = detect_mood(text)
    return build_mood_response(text, mood)

@app.post("/speech-mood")
async def speech_mood(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename or "audio")[-1] or ".webm"
    temp_dir = "/tmp"
    temp_path = os.path.join(temp_dir, f"{uuid.uuid4().hex}{ext}")

    try:
        with open(temp_path, "wb") as buf:
            shutil.copyfileobj(file.file, buf)

        text = speech_to_text(temp_path)
        mood = detect_mood(text)
        return build_mood_response(text, mood)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech processing failed: {str(e)}")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/story")
def story(data: MoodInput):
    """Generate a Panchatantra-style healing story for the given mood."""
    mood = data.mood.lower().strip()
    if mood not in chakra_raga_map:
        raise HTTPException(status_code=400, detail=f"Unknown mood '{mood}'. Valid: {list(chakra_raga_map.keys())}")

    story_text = generate_story_with_voice(mood)
    return {
        "mood":  mood,
        "story": story_text,
        "audio": BASE_URL + "/stories/story.mp3",
    }