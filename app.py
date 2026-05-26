import asyncio

from debate.generator import generate_debate
from debate.parser import parse_debate
from voice_generator import generate_voice
from mixer import merge_audio
from utils import clean_text

topic = input("Enter topic: ")

# STEP 1
print("\nGenerating debate...\n")

debate = generate_debate(topic)

print("\nDEBATE OUTPUT:\n")
print(debate)

# STEP 2
dialogues = parse_debate(debate)

print("\nPARSED DIALOGUES:\n")
print(dialogues)

# STEP 3
voice_map = {
    "Alex": "en-US-GuyNeural",
    "Ben": "en-US-JennyNeural"
}

audio_files = []

# STEP 4
for i, (speaker, text) in enumerate(dialogues):

    print(f"\nGenerating audio for {speaker}")
    print(text)

    text = clean_text(text)
    voice = voice_map.get(speaker, "en-US-GuyNeural")

    output_file = f"audio_{i}.mp3"

    asyncio.run(
        generate_voice(
            text=text,
            voice=voice,
            output_file=output_file
        )
    )

    audio_files.append(output_file)

    print(f"Generated: {output_file}")

# STEP 5
print("\nAudio files:\n")
print(audio_files)

# STEP 6
if len(audio_files) > 0:

    merge_audio(audio_files, "final_podcast.mp3")

else:
    print("No audio files generated.")