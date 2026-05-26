import edge_tts
import asyncio


async def generate_voice(
    text,
    voice,
    output_file,
    rate="+0%",
    pitch="+0Hz",
    volume="+0%"
):

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch,
        volume=volume
    )

    await communicate.save(output_file)