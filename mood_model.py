from textblob import TextBlob

def detect_mood(text):
    if not text:
        return "stressed"

    text = text.lower()

    # Keyword rules
    if any(w in text for w in ["stress", "anxious", "worried", "panic", "tension"]):
        return "stressed"
    if any(w in text for w in ["sad", "depressed", "lonely", "cry", "hopeless"]):
        return "sad"
    if any(w in text for w in ["happy", "great", "good", "excited", "joy"]):
        return "happy"

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.3:
        return "happy"
    elif polarity < -0.2:
        return "sad"
    else:
        return "stressed"
