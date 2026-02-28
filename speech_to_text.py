import os
import speech_recognition as sr
from pydub import AudioSegment

def speech_to_text(file_path: str) -> str:
    """
    Transcribe audio file to text using Google Speech Recognition.
    Handles .webm, .mp3, .ogg, .m4a → converts to .wav first.
    Returns empty string if transcription fails.
    """
    recognizer = sr.Recognizer()
    wav_path = None

    try:
        # Convert any format → WAV (SpeechRecognition only reads WAV)
        if not file_path.lower().endswith(".wav"):
            wav_path = file_path + ".wav"
            sound = AudioSegment.from_file(file_path)  # pydub auto-detects format
            sound = sound.set_channels(1).set_frame_rate(16000)  # mono 16kHz = best for SR
            sound.export(wav_path, format="wav")
            target = wav_path
        else:
            target = file_path

        with sr.AudioFile(target) as source:
            # Adjust for ambient noise for better accuracy
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        print(f"[speech_to_text] Transcribed: {text}")
        return text

    except sr.UnknownValueError:
        print("[speech_to_text] Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"[speech_to_text] Google SR request failed: {e}")
        return ""
    except Exception as e:
        print(f"[speech_to_text] Unexpected error: {e}")
        return ""
    finally:
        # Clean up the converted WAV file
        if wav_path and os.path.exists(wav_path):
            os.remove(wav_path)