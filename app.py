
import streamlit as st
import os

# ==========================================
# MUHAMMAD ABDULLAH - SCHOOL AI CHATBOT
# ==========================================

st.set_page_config(
    page_title="Muhammad Abdullah | School AI",
    page_icon="🎓",
    layout="wide"
)

# Professional Design
st.markdown("""
<style>
.stApp {
    background: #f3f6fc;
}
.main-title {
    background: linear-gradient(120deg, #102a43, #176b87);
    padding: 30px;
    border-radius: 18px;
    color: white;
    text-align: center;
}
.main-title h1 {
    color: white;
}
.main-title p {
    color: #e0f2fe;
}
.stButton button {
    background: #176b87;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🎓 Muhammad Abdullah")
    st.caption("Your School AI Assistant")
    st.divider()

    student = st.text_input("Your Name")

    grade = st.selectbox(
        "Select Your Class",
        [f"Class {i}" for i in range(1, 11)]
    )

    subject = st.selectbox(
        "Select Subject",
        [
            "All Subjects",
            "Mathematics",
            "English",
            "Urdu",
            "Science",
            "Physics",
            "Chemistry",
            "Biology",
            "Computer Science",
            "Islamiyat",
            "Pakistan Studies",
            "Social Studies",
            "History",
            "Geography"
        ]
    )

    language = st.selectbox(
        "Answer Language",
        ["English", "Urdu", "Roman Urdu"]
    )

    mode = st.selectbox(
        "Study Help",
        [
            "Explain Topic",
            "Homework Help",
            "Step-by-Step Solution",
            "Make Short Notes",
            "Create Quiz",
            "Exam Preparation",
            "Give Examples",
            "Explain Difficult Words"
        ]
    )

    st.divider()
    st.write("Created by Muhammad Abdullah ❤️")

# Main Header
st.markdown("""
<div class="main-title">
<h1>🎓 Muhammad Abdullah</h1>
<h2>School AI Chatbot</h2>
<p>Your Smart Learning Partner | Classes 1 to 10</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# Features
col1, col2, col3 = st.columns(3)

col1.info("📚 All School Subjects")
col2.info("🧠 Smart Study Help")
col3.info("✍️ Homework Assistant")

st.subheader("🤖 Ask Muhammad Abdullah AI")

st.write(
    "Ask questions, understand lessons, "
    "prepare for exams and improve your knowledge!"
)

# Gemini API
def get_api_key():
    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return os.getenv("GEMINI_API_KEY", "")

# AI Prompt
def create_prompt(question):
    return f"""
You are Muhammad Abdullah School AI.

Student: {student or 'Student'}
Class: {grade}
Subject: {subject}
Language: {language}
Study Mode: {mode}

Student Question:
{question}

Instructions:
1. Give accurate educational answers.
2. Use language suitable for the student's class.
3. Explain difficult concepts simply.
4. Show mathematics solutions step by step.
5. Give examples where useful.
6. Help with English and Urdu grammar.
7. Explain science topics clearly.
8. Help students understand homework.
9. Create 5 questions for quiz requests.
10. Include an answer key for quizzes.
11. Help students prepare for examinations.
12. Be friendly, respectful and encouraging.
13. Never invent facts.
14. If unsure, explain that you are unsure.
"""

# Basic Offline Help
def offline_answer(question):
    q = question.lower()

    if "photosynthesis" in q:
        return """
### 🌱 Photosynthesis

Photosynthesis is the process by which green
plants make their own food.

Plants need:
- Sunlight
- Water
- Carbon dioxide

Oxygen is released during this process.
"""

    elif "fraction" in q:
        return """
### ➗ Fractions

A fraction represents a part of a whole.

Example: 1/2

1 = Numerator
2 = Denominator

It means one out of two equal parts.
"""

    elif "noun" in q:
        return """
### 📖 Noun

A noun is the name of a person, place,
animal or thing.

Examples:
- Ali
- School
- Cat
- Book
"""

    elif "verb" in q:
        return """
### 📖 Verb

A verb is an action or being word.

Examples:
- Read
- Write
- Play
- Run
"""

    return """
### ⚙️ AI Not Connected

Please add your Gemini API key in
Streamlit Secrets to enable intelligent
answers across all school subjects.

You can still try:
- Photosynthesis
- Fractions
- Nouns
- Verbs
"""

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
question = st.chat_input("Ask your school question here...")

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):

        with st.spinner("Muhammad Abdullah AI is thinking..."):

            api_key = get_api_key()

            if api_key:
                try:
                    from google import genai

                    client = genai.Client(api_key=api_key)

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=create_prompt(question)
                    )

                    answer = response.text

                except Exception:
                    answer = (
                        "AI connection failed. Please check "
                        "your Gemini API key and try again."
                    )

            else:
                answer = offline_answer(question)

            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

# Clear Chat
if st.session_state.messages:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.divider()

st.markdown("""
<div style="text-align:center">
<h3>🎓 Muhammad Abdullah</h3>
<p>School AI Chatbot | Classes 1–10</p>
<p>Made with ❤️ by Muhammad Abdullah</p>
</div>
""", unsafe_allow_html=True)

# API Setup Instructions
with st.expander("⚙️ AI Setup Instructions"):

    st.write("""
    To activate full AI answers:

    1. Get a Gemini API key from Google AI Studio.
    2. Open Streamlit Community Cloud.
    3. Open your app Settings → Secrets.
    4. Add:

    GEMINI_API_KEY = "YOUR_API_KEY"

    Never publish your private API key on GitHub.
    """)


