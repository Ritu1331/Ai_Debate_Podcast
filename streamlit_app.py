# =========================================================
# AI DEBATE PODCAST - STREAMLIT APP
# =========================================================

import streamlit as st
import asyncio
import os
import time
import re

from debate.generator import generate_debate
from debate.parser import parse_debate

from voice_generator import generate_voice
from mixer import merge_audio

from utils.text_cleaner import humanize_text
from utils.emotion import detect_emotion


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Debate Podcast",
    page_icon="🎙️",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       MAIN BACKGROUND
    ===================================================== */

    .stApp {

        background:
            linear-gradient(
                135deg,
                #020617,
                #050816,
                #0f172a
            );

        color: white;
    }


    /* =====================================================
       SIDEBAR
    ===================================================== */

    section[data-testid="stSidebar"] {

        background:
            rgba(255,255,255,0.04);

        backdrop-filter: blur(12px);

        border-right:
            1px solid rgba(255,255,255,0.08);
    }


    /* =====================================================
       TITLE
    ===================================================== */

    .main-title {

        text-align: center;

        font-size: 72px;

        font-weight: 900;

        margin-top: 20px;

        background:
            linear-gradient(
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

        color: #94a3b8;

        font-size: 24px;

        margin-bottom: 40px;
    }


    /* =====================================================
       GLASS CARD
    ===================================================== */

    .glass {

        background:
            rgba(255,255,255,0.05);

        border:
            1px solid rgba(255,255,255,0.08);

        border-radius: 24px;

        padding: 25px;

        backdrop-filter: blur(14px);

        margin-bottom: 25px;
    }


    /* =====================================================
       SECTION TITLES
    ===================================================== */

    .section-title {

        font-size: 38px;

        font-weight: 800;

        margin-bottom: 20px;

        color: white;
    }


    /* =====================================================
       BUTTON
    ===================================================== */

    .stButton > button {

        width: 100%;

        height: 60px;

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

        transition: 0.3s;
    }


    .stButton > button:hover {

        transform: scale(1.02);

        box-shadow:
            0px 0px 20px rgba(0,212,255,0.4);
    }


    /* =====================================================
       INPUT
    ===================================================== */

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


    /* =====================================================
       TEXTAREA
    ===================================================== */

    textarea {

        background:
            rgba(255,255,255,0.04) !important;

        color: white !important;

        border-radius: 18px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="main-title">
        🎙️ AI Debate Podcast
    </div>

    <div class="subtitle">
        Realistic Multi-Speaker AI Podcast Generator
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Podcast Settings")

debate_style = st.sidebar.selectbox(
    "Debate Style",
    [
        "Professional",
        "Friendly",
        "Aggressive",
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


# =========================================================
# INPUT
# =========================================================

st.markdown('<div class="glass">', unsafe_allow_html=True)

topic = st.text_input(
    "🎯 Enter Debate Topic",
    placeholder="AI vs Humans, Climate Change, Social Media..."
)

generate = st.button(
    "🚀 Generate AI Debate Podcast"
)

st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# MAIN GENERATION
# =========================================================

if generate and topic:

    # =====================================================
    # DELETE OLD AUDIO FILES
    # =====================================================

    for file in os.listdir():

        if file.endswith(".mp3"):

            try:

                os.remove(file)

            except:

                pass

    progress = st.progress(0)

    status = st.empty()

    # =====================================================
    # GENERATE DEBATE
    # =====================================================

    status.info("🧠 Generating AI Debate...")

    progress.progress(20)

    debate = generate_debate(topic)

    time.sleep(1)

    # =====================================================
    # SHOW TRANSCRIPT
    # =====================================================

    st.markdown(
        '<div class="section-title">🧠 Debate Transcript</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.text_area(
        "Generated Debate",
        debate,
        height=450
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # PARSE DEBATE
    # =====================================================

    status.info("🎙️ Parsing Speakers...")

    progress.progress(40)

    dialogues = parse_debate(debate)

    if not dialogues:

        st.error("Failed to parse debate.")

        st.stop()

    # =====================================================
    # VOICE MAP
    # =====================================================

    voice_map = {

        "Host": "en-US-AriaNeural",

        "Alex": "en-US-GuyNeural",

        "Jamie": "en-US-JennyNeural",

        "Alex Chen": "en-US-GuyNeural",

        "Jamie Patel": "en-US-JennyNeural",

        "Rachel": "en-US-AriaNeural",

        "Rachel Lee": "en-US-AriaNeural"
    }

    audio_files = []

    # =====================================================
    # GENERATE AUDIO
    # =====================================================

    status.info("🎧 Generating Emotional Voices...")

    progress.progress(70)

    for i, dialogue in enumerate(dialogues):

        try:

            speaker = dialogue["speaker"]

            text = dialogue["text"]

            # =====================================
            # REMOVE MARKDOWN
            # =====================================

            text = text.replace("**", "")

            # =====================================
            # REMOVE SPEAKER LABELS
            # =====================================

            text = re.sub(

                r"^[A-Za-z ,]+:\s*",

                "",

                text
            )

            # =====================================
            # REMOVE BRACKET ACTIONS
            # =====================================

            text = re.sub(

                r"\(.*?\)",

                "",

                text
            )

            # =====================================
            # REMOVE EXTRA SPACES
            # =====================================

            text = re.sub(

                r"\s+",

                " ",

                text
            ).strip()

            # =====================================
            # HUMANIZE
            # =====================================

            text = humanize_text(text)

            if not text.strip():

                continue

            # =====================================
            # DETECT EMOTION
            # =====================================

            emotion = detect_emotion(text)

            # =====================================
            # SELECT VOICE
            # =====================================

            voice = voice_map.get(

                speaker,

                "en-US-GuyNeural"
            )

            output_file = f"audio_{i}.mp3"

            # =====================================
            # GENERATE TTS
            # =====================================

            asyncio.run(

                generate_voice(

                    text=text,

                    voice=voice,

                    output_file=output_file,

                    emotion=emotion
                )
            )

            if os.path.exists(output_file):

                audio_files.append(output_file)

        except Exception as e:

            st.error(f"Voice generation failed: {e}")

    # =====================================================
    # MERGE AUDIO
    # =====================================================

    status.info("🎵 Mixing Podcast Audio...")

    progress.progress(90)

    if len(audio_files) > 0:

        merge_audio(
            audio_files,
            "final_podcast.mp3"
        )

    progress.progress(100)

    status.success("✅ Podcast Generated Successfully!")

    # =====================================================
    # AUDIO PLAYER
    # =====================================================

    st.markdown(
        '<div class="section-title">🎧 Generated Podcast</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="glass">', unsafe_allow_html=True)

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