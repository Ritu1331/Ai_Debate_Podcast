def detect_emotion(text):

    text = text.lower()

    excited_words = [

        "amazing",
        "excited",
        "incredible",
        "fantastic",
        "wonderful",
        "great"
    ]

    angry_words = [

        "wrong",
        "ridiculous",
        "terrible",
        "hate",
        "awful"
    ]

    sad_words = [

        "sad",
        "depressed",
        "upset",
        "unfortunate"
    ]

    happy_words = [

        "happy",
        "love",
        "enjoy",
        "beautiful"
    ]

    if any(word in text for word in excited_words):

        return "excited"

    if any(word in text for word in angry_words):

        return "angry"

    if any(word in text for word in sad_words):

        return "sad"

    if any(word in text for word in happy_words):

        return "happy"

    return "neutral"