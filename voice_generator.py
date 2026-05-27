import edge_tts


async def generate_voice(

    text,
    voice,
    output_file,
    emotion="neutral"
):

    # =====================================
    # EMOTION SETTINGS
    # =====================================

    rate = "+0%"
    pitch = "+0Hz"

    if emotion == "excited":

        rate = "+15%"
        pitch = "+12Hz"

    elif emotion == "sad":

        rate = "-10%"
        pitch = "-10Hz"

    elif emotion == "angry":

        rate = "+8%"
        pitch = "-8Hz"

    elif emotion == "happy":

        rate = "+10%"
        pitch = "+8Hz"

    # =====================================
    # NORMAL TTS
    # =====================================

    communicate = edge_tts.Communicate(

        text=text,

        voice=voice,

        rate=rate,

        pitch=pitch
    )

    await communicate.save(output_file)