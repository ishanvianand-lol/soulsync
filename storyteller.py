import os
import google.generativeai as genai
from gtts import gTTS

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

os.makedirs("stories", exist_ok=True)

FALLBACKS = {
    "stressed": "A busy bee kept flying without rest until a wise owl said, 'Even rivers pause at bends.' The bee rested, and returned stronger. Moral: Stillness is not weakness — it is wisdom.",
    "sad":      "A lonely elephant wept by a dry river. A small sparrow sat beside her and sang softly. Slowly, the river filled with rain. Moral: Even the smallest kindness can restore a flood of hope.",
    "happy":    "A cheerful monkey shared his mangoes with every animal in the forest. That season, every tree bore double the fruit. Moral: Joy multiplied is joy that never runs out.",
}

def generate_story_with_voice(mood: str) -> str:
    """Generate a Panchatantra-style healing story and save it as MP3."""

    # 1. Generate story text via Gemini
    try:
        prompt = (
            f"Write a short Panchatantra-style healing story for someone feeling {mood}. "
            "Include two animal characters and end with a one-line moral. "
            "Keep it under 120 words. Do not use markdown or bullet points."
        )
        response = model.generate_content(prompt)
        story_text = response.text.strip()
        if not story_text:
            raise ValueError("Empty response from Gemini")
    except Exception as e:
        print(f"[storyteller] Gemini failed: {e}")
        story_text = FALLBACKS.get(mood, FALLBACKS["stressed"])

    # 2. Convert to speech
    audio_path = "stories/story.mp3"
    try:
        tts = gTTS(text=story_text, lang="en", slow=False)
        tts.save(audio_path)
    except Exception as e:
        print(f"[storyteller] gTTS failed: {e}")
        # Don't crash — frontend will just have no audio

    return story_text