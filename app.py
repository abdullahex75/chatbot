
import streamlit as st
import json
import hashlib
import hmac
import os
import re
from pathlib import Path

# =====================================================
# MUHAMMAD ABDULLAH SCHOOL AI
# COMPLETE OFFLINE CHATBOT + SIGN UP + SIGN IN
# =====================================================

st.set_page_config(
    page_title="Muhammad Abdullah | School AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

APP_DIR = Path(__file__).parent
DB_FILE = APP_DIR / "users.json"

SUBJECTS = [
    "All Subjects", "Mathematics", "English", "Urdu",
    "General Science", "Physics", "Chemistry", "Biology",
    "Computer Science", "Islamiyat", "Pakistan Studies",
    "Social Studies", "History", "Geography"
]

LANGUAGES = ["Simple English", "Urdu", "Roman Urdu"]

STUDY_MODES = [
    "Explain a topic",
    "Solve homework step by step",
    "Make short revision notes",
    "Create a practice quiz",
    "Give examples",
    "Explain difficult words",
    "Check my understanding"
]

# =====================================================
# DATABASE
# =====================================================

def load_users():
    if DB_FILE.exists():
        try:
            return json.loads(DB_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_users(users):
    temp_file = DB_FILE.with_suffix(".tmp")
    temp_file.write_text(
        json.dumps(users, indent=4),
        encoding="utf-8"
    )
    os.replace(temp_file, DB_FILE)


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        200000
    ).hex()


def create_password_hash(password):
    import secrets
    salt = secrets.token_bytes(16)
    return {
        "salt": salt.hex(),
        "hash": hash_password(password, salt.hex())
    }


def verify_password(password, stored):
    try:
        calculated = hash_password(password, stored["salt"])
        return hmac.compare_digest(calculated, stored["hash"])
    except (KeyError, TypeError):
        return False


# =====================================================
# SESSION STATE
# =====================================================

defaults = {
    "logged_in": False,
    "messages": [],
    "auth_page": "Sign In"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# PROFESSIONAL DESIGN
# =====================================================

st.markdown("""
<style>

:root {
    --navy:#07182B;
    --blue:#123B63;
    --teal:#176B9A;
    --ice:#DCEBFA;
}

.stApp {
    background:
        radial-gradient(circle at 85% 0%,#17466F 0%,transparent 32%),
        linear-gradient(145deg,#061426 0%,#0B2340 55%,#102F52 100%);
    color:#F4F8FC;
}

[data-testid="stHeader"] {
    background:rgba(6,20,38,.72);
}

[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#061426,#102F52);
}

[data-testid="stSidebar"] * {
    color:#F4F8FC !important;
}

.hero {
    padding:28px 30px;
    border-radius:22px;
    color:white;
    background:linear-gradient(115deg,#07182B,#123B63 58%,#176B9A);
    border:1px solid rgba(142,190,230,.22);
    box-shadow:0 14px 34px rgba(0,0,0,.28);
    margin-bottom:18px;
}

.hero h1 {
    color:white !important;
    font-size:2.1rem;
}

.hero p {
    color:#DCEBFA !important;
}

.mini-card {
    background:linear-gradient(145deg,#102B49,#15395E);
    border:1px solid #28527A;
    border-radius:16px;
    padding:17px;
    min-height:95px;
    box-shadow:0 6px 18px rgba(0,0,0,.16);
}

.mini-card b {
    color:white;
    font-size:1.03rem;
}

.mini-card span {
    color:#C5D8EA;
    font-size:.88rem;
}

.auth-card {
    background:linear-gradient(145deg,#102B49,#15395E);
    border:1px solid #3475A8;
    border-radius:20px;
    padding:22px;
}

div[data-testid="stChatMessage"] {
    border:1px solid #294D70;
    border-radius:16px;
    padding:12px;
    background:rgba(13,37,64,.94);
    color:#F4F8FC;
}

div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li {
    color:#F4F8FC;
}

.stButton button {
    border-radius:12px;
    border:1px solid #3475A8;
    font-weight:600;
    background:linear-gradient(100deg,#174D7A,#176B9A);
    color:white;
}

.footer {
    text-align:center;
    color:#B5C9DC;
    font-size:.85rem;
    padding:22px 0 8px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# AUTHENTICATION
# =====================================================

def signup():

    st.markdown("""
    <div class="hero">
        <h1>📝 Create Your Account</h1>
        <p>Join Muhammad Abdullah School AI</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("signup_form"):

        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "Email Address",
            placeholder="example@email.com"
        )

        grade = st.selectbox(
            "Choose Your Class",
            [f"Class {n}" for n in range(1, 11)]
        )

        password = st.text_input(
            "Create Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )

        if submitted:

            users = load_users()
            email = email.strip().lower()

            if not name.strip() or not email or not password:
                st.error("Please complete all fields.")

            elif not re.fullmatch(
                r"[^@\s]+@[^@\s]+\.[^@\s]+", email
            ):
                st.error("Please enter a valid email address.")

            elif len(password) < 8:
                st.error("Password must be at least 8 characters.")

            elif password != confirm:
                st.error("Passwords do not match.")

            elif email in users:
                st.error("Account already exists. Please sign in.")

            else:

                password_data = create_password_hash(password)

                users[email] = {
                    "name": name.strip(),
                    "grade": grade,
                    "password": password_data
                }

                save_users(users)

                st.success("Account created successfully!")
                st.info("Now open Sign In and login to your account.")


def signin():

    st.markdown("""
    <div class="hero">
        <h1>🔐 Welcome Back</h1>
        <p>Sign in to your School AI account</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("signin_form"):

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Sign In",
            use_container_width=True
        )

        if submitted:

            users = load_users()
            email = email.strip().lower()
            user = users.get(email)

            if user and verify_password(
                password, user.get("password", {})
            ):

                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.user_name = user["name"]
                st.session_state.grade = user["grade"]
                st.session_state.messages = []

                st.rerun()

            else:
                st.error("Incorrect email or password.")


# =====================================================
# OFFLINE KNOWLEDGE BASE
# =====================================================

KNOWLEDGE = {

    "photosynthesis": """
### 🌱 Photosynthesis

Photosynthesis is the process by which green plants make food.

Plants need:
1. Sunlight
2. Water
3. Carbon dioxide

Oxygen is released during this process.
""",

    "fraction": """
### 📐 Fractions

A fraction represents a part of a whole.

Example: 1/2

- 1 is the numerator.
- 2 is the denominator.

Example: Half of a pizza is 1/2.
""",

    "noun": """
### 📖 Noun

A noun is the name of a person, place, animal or thing.

Examples:
- Teacher
- School
- Cat
- Book
""",

    "verb": """
### ✍️ Verb

A verb tells an action or state.

Examples:
- Run
- Eat
- Write
- Read
""",

    "planet": """
### 🌍 Solar System

There are eight planets:

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
### 💻 Computer

A computer is an electronic machine that processes data.

Main components:
1. Input devices
2. CPU
3. Memory
4. Output devices
""",

    "water": """
### 💧 Water

Water is essential for life.

Its chemical formula is H₂O.

Water is used for drinking, cooking and cleaning.
""",

    "pakistan": """
### 🇵🇰 Pakistan

Pakistan became independent on 14 August 1947.

Its founder was Quaid-e-Azam Muhammad Ali Jinnah.

Its capital is Islamabad.
""",

    "gravity": """
### 🌎 Gravity

Gravity is a force that attracts objects toward each other.

Earth's gravity keeps us on the ground.
"""
}


# =====================================================
# OFFLINE ANSWER ENGINE
# =====================================================

def get_answer(question, subject, language, mode, grade):

    q = question.lower().strip()

    greetings = ["hello", "hi", "hey", "salam", "assalam"]

    if any(word in q for word in greetings):

        return """
Hello! 👋

Welcome to **Muhammad Abdullah School AI**.

I am your offline school study assistant.

Ask me about Mathematics, English, Science and other subjects.
"""

    # Knowledge search
    for keyword, answer in KNOWLEDGE.items():

        if keyword in q:
            return answer

    # Basic calculator
    if re.fullmatch(r"\s*\d+\s*[\+\-\*/]\s*\d+\s*", q):

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

        return f"""
### 🧮 Mathematics Answer

{a} {op} {b} = **{result}**

Great job! Keep practising.
"""

    # Quiz
    if "quiz" in q or mode == "Create a practice quiz":

        return """
### 📝 Practice Quiz

1. What is photosynthesis?
2. What is a noun?
3. How many planets are in our solar system?
4. What is the chemical formula of water?
5. Who founded Pakistan?

Try answering these questions!

**Answer Key:**

1. Process by which plants make food.
2. Name of a person, place, animal or thing.
3. Eight.
4. H₂O.
5. Muhammad Ali Jinnah.
"""

    # Notes
    if "note" in q or mode == "Make short revision notes":

        return """
### 📚 Revision Notes

- Read your topic carefully.
- Learn important definitions.
- Remember key points.
- Practise examples.
- Revise regularly.

Ask about a specific topic for more focused notes.
"""

    # Examples
    if mode == "Give examples":

        return """
### ✍️ Examples

**Noun:** Book, School, Teacher.

**Verb:** Run, Write, Read.

**Adjective:** Beautiful, Happy, Clever.

**Number:** 2 + 2 = 4.
"""

    if language == "Urdu":
        return """
مجھے اس سوال کا جواب اپنے آف لائن ڈیٹا میں نہیں ملا۔

آپ ان موضوعات کے بارے میں سوال پوچھ سکتے ہیں:

- Photosynthesis
- Fractions
- Noun
- Verb
- Planets
- Computer
- Water
- Pakistan
"""

    if language == "Roman Urdu":
        return """
Mujhe is sawal ka jawab apne offline data mein nahi mila.

Aap in topics ke bare mein pooch sakte hain:

- Photosynthesis
- Fractions
- Noun
- Verb
- Planets
- Computer
- Water
- Pakistan
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

**Note:** This chatbot uses a built-in knowledge base, not a live AI model.
"""


# =====================================================
# LOGIN SCREEN
# =====================================================

if not st.session_state.logged_in:

    st.markdown("""
    <div class="hero">
        <h1>🎓 Muhammad Abdullah School AI</h1>
        <p>Your Smart Offline Educational Assistant</p>
        <p>Learn • Practice • Improve</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<h3 style='text-align:center'>Welcome to School AI</h3>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        tab1, tab2 = st.tabs([
            "🔐 Sign In",
            "📝 Sign Up"
        ])

        with tab1:
            signin()

        with tab2:
            signup()

    st.markdown("""
    <div class="footer">
    🎓 Muhammad Abdullah School AI<br>
    Created by Muhammad Abdullah
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# =====================================================
# SIDEBAR DASHBOARD
# =====================================================

with st.sidebar:

    st.title("🎓 School AI")

    st.caption("Student Dashboard")

    st.divider()

    st.success(
        "Welcome, " + st.session_state.user_name
    )

    st.write("🎓 " + st.session_state.grade)

    subject = st.selectbox(
        "Choose Subject",
        SUBJECTS
    )

    language = st.selectbox(
        "Answer Language",
        LANGUAGES
    )

    mode = st.selectbox(
        "Study Mode",
        STUDY_MODES
    )

    st.divider()

    st.caption("Learn • Practise • Improve")

    st.caption("Created by Muhammad Abdullah")

    if st.button("🚪 Logout", use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.messages = []

        for key in [
            "user_email",
            "user_name",
            "grade"
        ]:
            st.session_state.pop(key, None)

        st.rerun()


# =====================================================
# MAIN HEADER
# =====================================================

st.markdown("""
<div class="hero">
    <h1>🎓 Muhammad Abdullah School AI</h1>
    <p>
    Your smart and friendly study companion —
    understand lessons, practise questions and prepare confidently.
    </p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# FEATURE CARDS
# =====================================================

c1, c2, c3 = st.columns(3)

for col, heading, detail in [
    (c1, "📚 Classes 1–10", "Learning support by class level"),
    (c2, "🧠 All Subjects", "Maths, languages and sciences"),
    (c3, "✍️ Study Tools", "Notes, quizzes and examples"),
]:

    col.markdown(
        f"""
        <div class="mini-card">
            <b>{heading}</b><br>
            <span>{detail}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")

with st.expander("📖 Subjects and Features"):

    st.write(", ".join(SUBJECTS[1:]))

    st.write(
        "Ask for topic explanations, homework guidance, "
        "examples, revision notes and practice quizzes."
    )


# =====================================================
# CHAT INTERFACE
# =====================================================

st.subheader(
    "💬 Study Chat — " + st.session_state.user_name
)

st.caption(
    "Ask your school questions. This chatbot works offline."
)

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# Chat Input
question = st.chat_input(
    "Ask a question about your school subjects..."
)

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Preparing your study answer..."):

            answer = get_answer(
                question,
                subject,
                language,
                mode,
                st.session_state.grade
            )

            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# =====================================================
# CLEAR CHAT
# =====================================================

if st.session_state.messages:

    if st.button("🗑️ Clear Conversation"):

        st.session_state.messages = []

        st.rerun()


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">
🎓 Muhammad Abdullah School AI
<br>
Professional Offline Educational Assistant
<br>
Created by Muhammad Abdullah
<br>
No API • No Gemini • No API Key
</div>
""", unsafe_allow_html=True)
