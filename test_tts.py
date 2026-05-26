import asyncio
from voice_generator import generate_voice

text = "Hello everyone, welcome to AI podcast."

asyncio.run(
    generate_voice(
        text=text,
        voice="en-US-GuyNeural",
        output_file="test.mp3"
    )
)

print("Voice generated!")