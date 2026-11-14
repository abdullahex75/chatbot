
import streamlit as st
from pathlib import Path
import random
import re

# ==========================================
# MUHAMMAD ABDULLAH SCHOOL AI
# 100% OFFLINE | NO API | NO API KEY
# ==========================================

st.set_page_config(
    page_title="Muhammad Abdullah | School AI",
    page_icon="🎓",
    layout="wide"
)

SUBJECTS = [
    "All Subjects", "Mathematics", "English", "Urdu",
    "General Science", "Physics", "Chemistry",
    "Biology", "Computer Science", "Islamiyat",
    "Pakistan Studies", "History", "Geography"
]

LANGUAGES = ["Simple English", "Urdu", "Roman Urdu"]

# ==========================================
# PROFESSIONAL DESIGN
# ==========================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#061426,#102F52);
    color: white;
}

[data-testid="stSidebar"] {
    background: #07182B;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.hero {
    background: linear-gradient(120deg,#07182B,#176B9A);
    padding: 30px;
    border-radius: 20px;
    border: 1px solid #3475A8;
    margin-bottom: 22px;
}

.hero h1 {
    color: white;
    font-size: 34px;
}

.hero p {
    color: #DCEBFA;
}

.card {
    background: #102B49;
    border: 1px solid #28527A;
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 10px;
}

div[data-testid="stChatMessage"] {
    background: #102B49;
    border: 1px solid #28527A;
    border-radius: 15px;
}

.stButton button {
    background: linear-gradient(90deg,#174D7A,#176B9A);
    color: white;
    border-radius: 12px;
    border: 1px solid #3475A8;
}

.footer {
    text-align: center;
    color: #B5C9DC;
    padding: 25px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🎓 School AI")

    st.caption("Created by Muhammad Abdullah")

    st.divider()

    student = st.text_input(
        "Student Name",
        placeholder="Enter your name"
    )

    grade = st.selectbox(
        "Select Class",
        [f"Class {i}" for i in range(1, 11)]
    )

    subject = st.selectbox(
        "Select Subject",
        SUBJECTS
    )

    language = st.selectbox(
        "Answer Language",
        LANGUAGES
    )

    mode = st.selectbox(
        "Study Mode",
        [
            "Explain a Topic",
            "Solve Homework",
            "Make Notes",
            "Create Quiz",
            "Give Examples"
        ]
    )

    st.divider()

    st.success("100% Offline Mode")

    st.caption("No API • No API Key")

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="hero">
    <h1>🎓 Muhammad Abdullah School AI</h1>
    <p>Your Smart Offline School Assistant</p>
    <p>Learn • Practice • Improve</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="card">
    📚 <b>Classes 1–10</b><br>
    <small>School learning support</small>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
    🧠 <b>All Subjects</b><br>
    <small>Multiple school subjects</small>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
    ✍️ <b>Study Tools</b><br>
    <small>Notes, examples and quizzes</small>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# OFFLINE KNOWLEDGE BASE
# ==========================================

KNOWLEDGE = {
    "photosynthesis": """
**Photosynthesis 🌱**

Photosynthesis is the process by which green plants make food.

Plants need:
1. Sunlight
2. Water
3. Carbon dioxide

Oxygen is released during this process.
""",

    "fraction": """
**Fractions 📐**

A fraction represents a part of a whole.

Example: 1/2

1 = Numerator
2 = Denominator

Example: Half of a pizza is 1/2.
""",

    "noun": """
**Noun 📖**

A noun is the name of a person, place, animal or thing.

Examples:
- Ali
- School
- Cat
- Book
""",

    "verb": """
**Verb ✍️**

A verb is an action or state word.

Examples:
- Run
- Eat
- Write
- Read
""",

    "planet": """
**Planets 🌍**

There are eight planets in our solar system:

1. Mercury
2. Venus
3. Earth
4. Mars
5. Jupiter
6. Saturn
7. Uranus
8. Neptune
""",

    "computer": """
**Computer 💻**

A computer is an electronic machine that processes data.

Main components:
1. Input devices
2. CPU
3. Memory
4. Output devices
""",

    "water": """
**Water 💧**

Water is essential for life.

Its chemical formula is H2O.

Water is used for drinking, cooking and cleaning.
""",

    "pakistan": """
**Pakistan 🇵🇰**

Pakistan became independent on 14 August 1947.

Its founder was Quaid-e-Azam Muhammad Ali Jinnah.

Its capital is Islamabad.
"""
}

# ==========================================
# RESPONSE ENGINE
# ==========================================

def get_answer(question):

    q = question.lower().strip()

    if any(x in q for x in [
        "hello", "hi", "salam", "assalam",
        "hey", "how are you"
    ]):
        return """
Hello! 👋

Welcome to **Muhammad Abdullah School AI**.

I am your offline study assistant.

Ask me about Mathematics, English, Science and other subjects.
"""

    # Knowledge search
    for keyword, answer in KNOWLEDGE.items():
        if keyword in q:
            return answer

    # Basic Mathematics
    if re.fullmatch(r"\s*\d+\s*[\+\-\*/]\s*\d+\s*", q):
        try:
            parts = re.match(
                r"\s*(\d+)\s*([\+\-\*/])\s*(\d+)\s*", q
            )
            a = int(parts.group(1))
            op = parts.group(2)
            b = int(parts.group(3))

            if op == "+":
                result = a + b
            elif op == "-":
                result = a - b
            elif op == "*":
                result = a * b
            else:
                if b == 0:
                    return "Division by zero is not allowed."
                result = a / b

            return f"**Math Answer 🧮**\n\n{a} {op} {b} = **{result}**"

        except Exception:
            pass

    if "quiz" in q or mode == "Create Quiz":

        return """
**Practice Quiz 📝**

1. What is photosynthesis?
2. What is a noun?
3. How many planets are in our solar system?
4. What is the chemical formula of water?
5. Who founded Pakistan?

Try answering these questions!
"""

    if "note" in q or mode == "Make Notes":

        return """
**Short Revision Notes 📚**

- Read the topic carefully.
- Remember important definitions.
- Learn key points.
- Practise examples.
- Revise regularly.

Enter a specific topic for more focused notes.
"""

    if "meaning" in q:

        return """
**Word Meaning 📖**

Please write the specific English word whose meaning you want to learn.
"""

    if "help" in q:

        return """
**I can help you with:**

- Mathematics
- English Grammar
- Urdu
- General Science
- Physics
- Chemistry
- Biology
- Computer Science
- Pakistan Studies
- Practice Quizzes
"""

    return """
I don't have an offline answer for this question yet. 😊

Try asking about:

- Photosynthesis
- Fractions
- Noun
- Verb
- Planets
- Computer
- Water
- Pakistan

**Note:** This is an offline sample chatbot. Its knowledge is limited to its built-in answers.
"""

# ==========================================
# CHAT HISTORY
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================================
# CHAT INPUT
# ==========================================

question = st.chat_input(
    "Ask your school question here..."
)

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Preparing your answer..."):

            answer = get_answer(question)

            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

# ==========================================
# CLEAR CHAT
# ==========================================

if st.session_state.messages:

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer">
🎓 Muhammad Abdullah School AI<br>
Professional Offline Educational Chatbot<br>
Created by Muhammad Abdullah
</div>
""", unsafe_allow_html=True)
