import edge_tts


async def generate_voice(

    text,
    voice,
    output_file,
    emotion="neutral"
):

    # =====================================
    # DEFAULT SETTINGS
    # =====================================

    rate = "+0%"
    pitch = "+0Hz"

    # =====================================
    # EMOTION SETTINGS
    # =====================================

    if emotion == "excited":

        rate = "+15%"
        pitch = "+10Hz"

    elif emotion == "happy":

        rate = "+10%"
        pitch = "+8Hz"

    elif emotion == "sad":

        rate = "-12%"
        pitch = "-10Hz"

    elif emotion == "angry":

        rate = "+8%"
        pitch = "-8Hz"

    # =====================================
    # EDGE TTS
    # =====================================

    communicate = edge_tts.Communicate(

        text=text,

        voice=voice,

        rate=rate,

        pitch=pitch
    )

    await communicate.save(output_file)