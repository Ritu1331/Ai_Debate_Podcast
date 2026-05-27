import re
import random


def humanize_text(text):

    # =====================================
    # REMOVE MARKDOWN
    # =====================================

    text = text.replace("**", "")

    # =====================================
    # REMOVE BRACKET ACTIONS
    # =====================================

    text = re.sub(r"\(.*?\)", "", text)
    text = re.sub(r"\[.*?\]", "", text)

    # =====================================
    # REMOVE EXTRA SPACES
    # =====================================

    text = re.sub(r"\s+", " ", text).strip()

    # =====================================
    # NATURAL SPEECH PAUSES
    # =====================================

    text = text.replace(".", "... ")
    text = text.replace("?", "? ")
    text = text.replace("!", "! ")

    # =====================================
    # HUMAN FILLERS
    # =====================================

    fillers = [

        "Well, ",
        "Honestly, ",
        "You know, ",
        "I mean, ",
        "Actually, "
    ]

    if random.random() > 0.75:

        text = random.choice(fillers) + text

    # =====================================
    # EMPHASIS WORDS
    # =====================================

    replacements = {

        "very": "really",
        "important": "super important",
        "good": "great",
        "bad": "terrible",
        "interesting": "pretty interesting"
    }

    for old, new in replacements.items():

        text = re.sub(
            rf"\b{old}\b",
            new,
            text,
            flags=re.IGNORECASE
        )

    # =====================================
    # REMOVE MULTIPLE DOTS
    # =====================================

    text = re.sub(r"\.\.\.+", "...", text)

    return text