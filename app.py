
import os
from pathlib import Path

import streamlit as st

# ============================================================
# MUHAMMAD ABDULLAH SCHOOL AI
# A Streamlit study assistant for Classes 1–10
# ============================================================

st.set_page_config(
    page_title="Muhammad Abdullah | School AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_DIR = Path(__file__).parent
PROFILE_IMAGE = APP_DIR / "muhammad_abdullah.png"

SUBJECTS = [
    "All Subjects", "Mathematics", "English", "Urdu",
    "General Science", "Physics", "Chemistry", "Biology",
    "Computer Science", "Islamiyat", "Pakistan Studies",
    "Social Studies", "History", "Geography",
]

LANGUAGES = ["Simple English", "Urdu", "Roman Urdu"]

STUDY_MODES = [
    "Explain a topic",
    "Solve homework step by step",
    "Make short revision notes",
    "Create a practice quiz",
    "Prepare for an exam",
    "Give examples",
    "Explain difficult words",
    "Check my understanding",
]

# ----------------------------- DESIGN -----------------------------

st.markdown(
    """
    <style>
    :root {
        --navy: #102A43;
        --teal: #0F8B8D;
        --ice: #EAF4F7;
    }

    .stApp {
        background: linear-gradient(
            180deg,
            #F5F8FC 0%,
            #EEF4F8 100%
        );
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #102A43 0%,
            #173F5F 100%
        );
    }

    [data-testid="stSidebar"] * {
        color: #F4F8FC !important;
    }

    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        color: #102A43 !important;
        background: #FFFFFF !important;
    }

    .hero {
        padding: 28px 30px;
        border-radius: 22px;
        color: white;
        background: linear-gradient(
            115deg,
            #102A43 0%,
            #176B87 58%,
            #0F8B8D 100%
        );
        box-shadow: 0 12px 28px rgba(16,42,67,.14);
        margin-bottom: 18px;
    }

    .hero h1 {
        color: white !important;
        font-size: 2.1rem;
        margin: 0;
    }

    .hero p {
        color: #E5F5FA !important;
        margin: 8px 0 0 0;
    }

    .mini-card {
        background: white;
        border: 1px solid #DCE7EF;
        border-radius: 16px;
        padding: 16px;
        min-height: 92px;
        box-shadow: 0 4px 14px rgba(16,42,67,.04);
    }

    .mini-card b {
        color: #102A43;
        font-size: 1.03rem;
    }

    .mini-card span {
        color: #587084;
        font-size: .88rem;
    }

    div[data-testid="stChatMessage"] {
        border: 1px solid #E0E9F0;
        border-radius: 16px;
        padding: 12px;
        background: rgba(255,255,255,.88);
    }

    .footer {
        text-align: center;
        color: #647B8D;
        font-size: .85rem;
        padding: 18px 0 8px;
    }

    .stButton button {
        border-radius: 12px;
        border: 0;
        font-weight: 600;
        background: linear-gradient(
            100deg,
            #176B87,
            #0F8B8D
        );
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------- SIDEBAR -----------------------------

with st.sidebar:

    if PROFILE_IMAGE.is_file():
        st.image(str(PROFILE_IMAGE), width=138)

    st.title("Muhammad Abdullah")
    st.caption("🎓 School AI • Classes 1–10")

    st.divider()

    student_name = st.text_input(
        "Student name (optional)",
        placeholder="Your name"
    )

    grade = st.selectbox(
        "Choose your class",
        [f"Class {n}" for n in range(1, 11)]
    )

    subject = st.selectbox(
        "Choose a subject",
        SUBJECTS
    )

    language = st.selectbox(
        "Answer language",
        LANGUAGES
    )

    study_mode = st.selectbox(
        "How can I help?",
        STUDY_MODES
    )

    st.divider()

    st.caption("Learn • Practise • Improve")
    st.caption("Created by Muhammad Abdullah")

# ----------------------------- HEADER -----------------------------

st.markdown(
    """
    <div class="hero">
        <h1>🎓 Muhammad Abdullah School AI</h1>
        <p>
            Your smart and friendly study companion —
            understand lessons, practise questions and
            prepare confidently for school.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)

for col, heading, detail in [
    (
        c1,
        "📚 Classes 1–10",
        "Learning support by class level"
    ),
    (
        c2,
        "🧠 All major subjects",
        "Maths, languages, sciences and more"
    ),
    (
        c3,
        "✍️ Study tools",
        "Notes, quizzes and homework guidance"
    ),
]:
    col.markdown(
        f"""
        <div class="mini-card">
            <b>{heading}</b><br>
            <span>{detail}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

with st.expander("📖 Subjects and features"):

    st.write(", ".join(SUBJECTS[1:]))

    st.write(
        "Ask for topic explanations, step-by-step homework guidance, "
        "examples, revision notes, practice quizzes and exam preparation."
    )

# ----------------------------- AI CONFIGURATION -----------------------------

def get_api_key():
    """Read the Gemini key from Streamlit Secrets or environment variables."""

    try:
        key = st.secrets.get("GEMINI_API_KEY", "")

        if key:
            return key

    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY", "")


def build_prompt(question: str) -> str:

    learner = student_name.strip() or "the student"

    return f"""
You are Muhammad Abdullah School AI, a patient,
accurate and encouraging school tutor.

Student: {learner}
Class: {grade}
Selected subject: {subject}
Answer language: {language}
Requested study mode: {study_mode}

Student's question:
{question}

Teaching requirements:

- Match explanations to the student's class.
- Use age-appropriate language.
- Answer in the selected language.
- For Urdu, use Urdu script.
- For Roman Urdu, use Roman Urdu.
- Explain concepts clearly in small steps.
- Include examples when useful.
- For mathematics, show the working and verify the answer.
- For science, explain the concept with a real-life example.
- For English and Urdu, help with grammar and vocabulary.
- For quizzes, create five suitable questions.
- Put the quiz answer key under a separate heading.
- For exam preparation, include key points and practice.
- Guide students to understand their homework.
- Never invent textbook page numbers or facts.
- If the question is unclear, ask one short question.
- Be respectful, supportive and concise.
"""


def offline_answer(question: str) -> str:
    """Small sample responses when the AI service is not connected."""

    q = question.lower()

    if any(
        word in q
        for word in ("hello", "hi", "salam", "assalam")
    ):
        return (
            "Hello! 👋 Welcome to **Muhammad Abdullah School AI**. "
            "Ask me a question from any school subject."
        )

    if "photosynthesis" in q:
        return (
            "**Photosynthesis** is the process by which green plants "
            "make food. Plants use sunlight, water and carbon dioxide. "
            "The process mainly happens in leaves, and oxygen is released."
        )

    if "fraction" in q:
        return (
            "A **fraction** represents part of a whole. "
            "In **1/2**, 1 is the numerator and 2 is the denominator. "
            "It means one of two equal parts."
        )

    if "noun" in q:
        return (
            "A **noun** names a person, place, animal or thing. "
            "Examples: teacher, school, cat and book."
        )

    if "verb" in q:
        return (
            "A **verb** tells an action or a state. "
            "Examples: read, write, run, is and are."
        )

    return (
        "The AI service is not connected yet. Add your Gemini API key "
        "under **Streamlit Cloud → App settings → Secrets** to enable "
        "answers across subjects.\n\n"
        "For now, try: photosynthesis, fraction, noun or verb."
    )

# ----------------------------- CHAT -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "Ask a question about your school subjects…"
)

if question:

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Preparing your study answer…"):

            api_key = get_api_key()

            if not api_key:

                answer = offline_answer(question)

            else:

                try:
                    from google import genai

                    client = genai.Client(
                        api_key=api_key
                    )

                    result = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=build_prompt(question),
                    )

                    answer = (
                        result.text
                        or "I couldn't prepare an answer. Please try again."
                    )

                except Exception:

                    answer = (
                        "I couldn't connect to the AI service. "
                        "Please check that your Gemini API key is correct "
                        "in Streamlit Secrets, then restart the app."
                    )

            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

if st.session_state.messages:

    if st.button("🗑️ Clear conversation"):

        st.session_state.messages = []
        st.rerun()

# ----------------------------- SETUP HELP -----------------------------

with st.expander("⚙️ AI Setup Instructions"):

    st.markdown(
        """
**To activate full AI answers:**

1. Add `streamlit` and `google-genai` to your `requirements.txt`.
2. Create a Gemini API key using Google AI Studio.
3. Open your app in Streamlit Community Cloud.
4. Go to **App settings → Secrets**.
5. Add the setting shown below, replacing the example with your private key.
        """
    )

    st.code(
        'GEMINI_API_KEY = "YOUR_PRIVATE_API_KEY"',
        language="toml"
    )

    st.warning(
        "Never put your private API key in this Python file "
        "or commit it to a public GitHub repository."
    )

# ----------------------------- FOOTER -----------------------------

st.markdown(
    """
    <div class="footer">
        🎓 Muhammad Abdullah School AI
        · Educational support for Classes 1–10
        <br>
        Check important answers against your textbook
        and teacher’s instructions.
    </div>
    """,
    unsafe_allow_html=True,
)
