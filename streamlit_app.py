import streamlit as st
import asyncio
import time
import os

from debate.generator import generate_debate
from debate.parser import parse_debate

from voice_generator import generate_voice
from mixer import merge_audio

from utils.emotion import detect_emotion
from utils.text_cleaner import humanize_text


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Debate Podcast",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.stApp {

    background:
        radial-gradient(circle at top left,
        rgba(0,212,255,0.15),
        transparent 25%),

        radial-gradient(circle at bottom right,
        rgba(124,77,255,0.18),
        transparent 25%),

        linear-gradient(
        135deg,
        #020617,
        #050816,
        #0b1120
    );

    color: white;
}


/* SIDEBAR */

section[data-testid="stSidebar"] {

    background:
        rgba(255,255,255,0.05);

    backdrop-filter: blur(16px);

    border-right:
        1px solid rgba(255,255,255,0.08);
}


/* TITLE */

.main-title {

    font-size: 72px;

    font-weight: 900;

    text-align: center;

    margin-top: 10px;

    background: linear-gradient(
        90deg,
        #00d4ff,
        #7c4dff,
        #ff4d6d
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {

    text-align: center;

    font-size: 22px;

    color: #9ca3af;

    margin-top: -10px;

    margin-bottom: 40px;
}


/* GLASS CARD */

.glass-card {

    background:
        rgba(255,255,255,0.06);

    border:
        1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(18px);

    border-radius: 24px;

    padding: 28px;

    margin-bottom: 25px;
}


/* BUTTON */

.stButton > button {

    width: 100%;

    height: 62px;

    border-radius: 18px;

    border: none;

    font-size: 22px;

    font-weight: bold;

    color: white;

    background:
        linear-gradient(
            90deg,
            #00d4ff,
            #7c4dff
        );
}


/* INPUT */

.stTextInput > div > div > input {

    background:
        rgba(255,255,255,0.06);

    border:
        1px solid rgba(255,255,255,0.08);

    border-radius: 16px;

    height: 55px;

    color: white;

    font-size: 18px;
}


/* TEXT AREA */

textarea {

    background:
        rgba(255,255,255,0.04) !important;

    border-radius: 18px !important;

    color: white !important;

    font-size: 17px !important;
}


/* SECTION TITLES */

.section-title {

    font-size: 40px;

    font-weight: 800;

    margin-bottom: 20px;

    background: linear-gradient(
        90deg,
        #ffffff,
        #00d4ff
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}


/* AUDIO */

audio {

    width: 100%;
}


/* FOOTER */

.footer {

    text-align: center;

    margin-top: 60px;

    color: #94a3b8;

    opacity: 0.7;

    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="main-title">
🎙️ AI Debate Podcast
</div>

<div class="subtitle">
Realistic Multi-Speaker AI Podcast Generator
</div>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("⚙️ Podcast Settings")

speaker_style = st.sidebar.selectbox(
    "Debate Style",
    [
        "Professional",
        "Aggressive",
        "Friendly",
        "Humorous"
    ]
)

voice_energy = st.sidebar.slider(
    "Voice Energy",
    0,
    100,
    50
)

debate_length = st.sidebar.slider(
    "Debate Length",
    4,
    12,
    6
)


# =====================================================
# INPUT
# =====================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

topic = st.text_input(
    "🎯 Enter Debate Topic",
    placeholder="AI vs Humans, Climate Change, Social Media..."
)

generate = st.button(
    "🚀 Generate AI Debate Podcast"
)

st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# MAIN
# =====================================================

if generate and topic:

    # =========================================
    # DELETE OLD AUDIO FILES
    # =========================================

    for file in os.listdir():

        if file.endswith(".mp3"):

            try:
                os.remove(file)

            except:
                pass

    progress = st.progress(0)

    status = st.empty()

    # =========================================
    # GENERATE DEBATE
    # =========================================

    status.info("🧠 Generating debate...")

    progress.progress(20)

    debate = generate_debate(topic)

    time.sleep(1)

    # =========================================
    # SHOW TRANSCRIPT
    # =========================================

    st.markdown(
        '<div class="section-title">🧠 Debate Transcript</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.text_area(
        "Generated Debate",
        debate,
        height=450
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # =========================================
    # PARSE
    # =========================================

    status.info("🎙️ Parsing debate...")

    progress.progress(40)

    dialogues = parse_debate(debate)

    if not dialogues:

        st.error("Failed to parse debate.")

        st.stop()

    # =========================================
    # VOICES
    # =========================================

    voice_map = {

        "Host": "en-US-AriaNeural",

        "Alex": "en-US-GuyNeural",

        "Jamie": "en-US-JennyNeural"
    }

    audio_files = []

    # =========================================
    # GENERATE AUDIO
    # =========================================

    status.info("🎧 Generating AI voices...")

    progress.progress(70)

    for i, dialogue in enumerate(dialogues):

        try:

            speaker = dialogue["speaker"]

            text = dialogue["text"]

            text = humanize_text(text)

            if not text.strip():
                continue

            emotion = detect_emotion(text)

            rate = "+0%"
            pitch = "+0Hz"
            volume = "+0%"

            if emotion == "excited":

                rate = "+10%"
                pitch = "+8Hz"

            elif emotion == "angry":

                rate = "+5%"
                pitch = "-5Hz"

            elif emotion == "sad":

                rate = "-10%"
                pitch = "-10Hz"

            voice = voice_map.get(
                speaker,
                "en-US-GuyNeural"
            )

            output_file = f"audio_{i}.mp3"

            print(f"\nGenerating voice for {speaker}")
            print(text)

            asyncio.run(
                generate_voice(
                    text=text,
                    voice=voice,
                    output_file=output_file,
                    rate=rate,
                    pitch=pitch,
                    volume=volume
                )
            )

            if os.path.exists(output_file):

                audio_files.append(output_file)

        except Exception as e:

            st.error(f"Audio generation failed: {e}")

    # =========================================
    # MERGE AUDIO
    # =========================================

    status.info("🎵 Mixing podcast...")

    progress.progress(90)

    if len(audio_files) > 0:

        merge_audio(
            audio_files,
            "final_podcast.mp3"
        )

    progress.progress(100)

    status.success("✅ Podcast Generated Successfully!")

    # =========================================
    # AUDIO PLAYER
    # =========================================

    st.markdown(
        '<div class="section-title">🎧 Generated Podcast</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    if os.path.exists("final_podcast.mp3"):

        with open(
            "final_podcast.mp3",
            "rb"
        ) as audio_file:

            audio_bytes = audio_file.read()

        st.audio(audio_bytes)

        st.download_button(
            label="⬇ Download Podcast",
            data=audio_bytes,
            file_name="ai_debate_podcast.mp3",
            mime="audio/mp3"
        )

    else:

        st.error("Podcast generation failed.")

    st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">
Built with ❤️ using Streamlit · Groq · ChromaDB · Edge-TTS
</div>
""", unsafe_allow_html=True)