import re


# =====================================================
# HUMANIZE / CLEAN TEXT
# =====================================================

def humanize_text(text):

    # Remove markdown bold
    text = re.sub(r"\*\*", "", text)

    # Remove unwanted symbols
    text = re.sub(r"[#*_>`]", "", text)

    # Better pauses for TTS
    text = text.replace(":", ". ")

    # Remove multiple newlines
    text = re.sub(r"\n+", "\n", text)

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()