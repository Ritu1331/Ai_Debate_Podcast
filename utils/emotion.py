def detect_emotion(text):

    text = text.lower()

    if "!" in text:
        return "excited"

    elif any(word in text for word in [
        "terrible",
        "angry",
        "ridiculous",
        "hate",
        "awful"
    ]):
        return "angry"

    elif any(word in text for word in [
        "sad",
        "worried",
        "depressed",
        "lonely",
        "upset"
    ]):
        return "sad"

    return "neutral"