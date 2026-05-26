from groq import Groq
import os
from dotenv import load_dotenv

from rag.retrieve import retrieve_context

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# =====================================================
# GENERATE DEBATE
# =====================================================

def generate_debate(topic):

    # =========================================
    # RETRIEVE CONTEXT FROM CHROMADB
    # =========================================

    context = retrieve_context(topic)

    # =========================================
    # IF CONTEXT FOUND → USE RAG
    # =========================================

    if context.strip():

        prompt = f"""
Generate a podcast-style debate.

Use ONLY the provided context.

Topic:
{topic}

Context:
{context}

IMPORTANT RULES:
- Use ONLY these speaker labels:
Speaker 1:
Speaker 2:

- NEVER use names like Alex, Jack, Moderator, Rachel, etc.
- No markdown
- No bold text
- Plain text only
- Alternate speakers clearly
- Keep responses conversational
- Stay grounded in context

Example:

Speaker 1: AI improves personalized learning.

Speaker 2: But students still need human interaction.
"""

    # =========================================
    # IF NO CONTEXT FOUND → GENERAL KNOWLEDGE
    # =========================================

    else:

        prompt = f"""
Topic: {topic}

Create a realistic AI podcast debate.

There are 3 people:

1. Host (moderator)
2. Alex (supports the topic)
3. Jamie (opposes or challenges the topic)

Structure:

1. Host introduces the podcast
2. Host introduces topic
3. Host introduces Alex and Jamie
4. Alex and Jamie debate naturally
5. Speakers occasionally address each other by name
6. Debate should feel emotional and realistic
7. Include small agreements/disagreements
8. End with Host concluding the episode

IMPORTANT:
- Make it sound like a real Spotify podcast
- Keep dialogue natural
- Avoid robotic wording
- Do NOT use stage directions
- Do NOT use brackets
- Format EXACTLY like this:

Host: text

Alex: text

Jamie: text
"""
    # =========================================
    # GROQ RESPONSE
    # =========================================

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content