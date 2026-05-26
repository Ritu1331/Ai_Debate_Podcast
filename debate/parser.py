import re


def parse_debate(text):

    pattern = r"([A-Za-z]+):\s*(.*?)(?=\n[A-Za-z]+:|$)"

    matches = re.findall(
        pattern,
        text,
        re.DOTALL
    )

    dialogues = []

    for speaker, line in matches:

        line = line.strip()

        if line:

            dialogues.append({
                "speaker": speaker,
                "text": line
            })

    return dialogues