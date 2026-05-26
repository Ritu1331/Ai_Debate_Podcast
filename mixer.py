import subprocess


def merge_audio(audio_files, output_file):

    with open("file_list.txt", "w", encoding="utf-8") as f:

        for audio in audio_files:

            f.write(f"file '{audio}'\n")

    command = [

        "ffmpeg",

        "-y",

        "-f",
        "concat",

        "-safe",
        "0",

        "-i",
        "file_list.txt",

        "-ar",
        "44100",

        "-ac",
        "2",

        "-b:a",
        "192k",

        output_file
    ]

    subprocess.run(command)

    print(f"Final podcast saved as {output_file}")