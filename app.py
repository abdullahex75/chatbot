
import streamlit as st
import json
import hashlib
import hmac
import secrets
import os
import re
import ast
import operator
from pathlib import Path
from datetime import datetime

# =========================================================
# MUHAMMAD ABDULLAH SCHOOL AI - PROFESSIONAL EDITION
# OFFLINE | NO API | NO GEMINI | NO API KEY
# =========================================================

st.set_page_config(
    page_title="Muhammad Abdullah | School AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent
DB_FILE = BASE_DIR / "users.json"

SUBJECTS = [
    "All Subjects", "Mathematics", "English", "Urdu",
    "General Science", "Physics", "Chemistry", "Biology",
    "Computer Science", "Islamiyat", "Pakistan Studies",
    "Social Studies", "History", "Geography"
]

LANGUAGES = [
    "Simple English",
    "Urdu",
    "Roman Urdu"
]

STUDY_MODES = [
    "Normal Chat",
    "Explain a Topic",
    "Solve Homework",
    "Make Revision Notes",
    "Create Practice Quiz",
    "Give Examples"
]

# =========================================================
# SESSION STATE
# =========================================================

DEFAULTS = {
    "logged_in": False,
    "page": "signin",
    "messages": [],
    "user_email": None,
    "user_name": None,
    "grade": None,
    "new_chat_count": 0
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# DATABASE
# =========================================================

def load_users():
    if not DB_FILE.exists():
        return {}

    try:
        return json.loads(DB_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_users(users):
    temp = DB_FILE.with_suffix(".tmp")

    temp.write_text(
        json.dumps(users, indent=4),
        encoding="utf-8"
    )

    os.replace(temp, DB_FILE)


def make_password(password):
    salt = secrets.token_bytes(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        300000
    )

    return {
        "salt": salt.hex(),
        "hash": hashed.hex()
    }


def check_password(password, stored):
    try:
        salt = bytes.fromhex(stored["salt"])

        hashed = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            300000
        )

        return hmac.compare_digest(
            hashed.hex(),
            stored["hash"]
        )

    except (KeyError, TypeError, ValueError):
        return False


# =========================================================
# LOGIN FUNCTIONS
# =========================================================

def login_user(email, user):
    st.session_state.logged_in = True
    st.session_state.user_email = email
    st.session_state.user_name = user["name"]
    st.session_state.grade = user["grade"]
    st.session_state.messages = []
    st.session_state.page = "chat"
    st.rerun()


def logout_user():
    for key in [
        "logged_in",
        "user_email",
        "user_name",
        "grade",
        "messages"
    ]:
        if key in st.session_state:
            del st.session_state[key]

    st.session_state.logged_in = False
    st.session_state.page = "signin"
    st.session_state.messages = []
    st.rerun()


# =========================================================
# PROFESSIONAL CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 85% 0%,#17466F 0%,transparent 32%),
        linear-gradient(145deg,#061426 0%,#0B2340 55%,#102F52 100%);
    color:#F4F8FC;
}

[data-testid="stHeader"] {
    background:rgba(6,20,38,.75);
}

[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#061426,#102F52);
}

[data-testid="stSidebar"] * {
    color:#F4F8FC !important;
}

[data-testid="stSidebar"] input,
[data-testid="stSidebar"] [data-baseweb="select"] {
    color:#102A43 !important;
}

.hero {
    padding:30px;
    border-radius:22px;
    background:linear-gradient(115deg,#07182B,#123B63 58%,#176B9A);
    border:1px solid rgba(142,190,230,.3);
    box-shadow:0 14px 34px rgba(0,0,0,.28);
    margin-bottom:20px;
}

.hero h1 {
    color:#FFFFFF !important;
    font-size:2.1rem;
}

.hero p {
    color:#DCEBFA !important;
}

.mini-card {
    background:linear-gradient(145deg,#102B49,#15395E);
    border:1px solid #28527A;
    border-radius:17px;
    padding:18px;
    min-height:105px;
    box-shadow:0 6px 18px rgba(0,0,0,.16);
}

.mini-card b {
    color:white;
    font-size:1.05rem;
}

.mini-card span {
    color:#C5D8EA;
    font-size:.88rem;
}

.auth-card {
    background:linear-gradient(145deg,#102B49,#15395E);
    border:1px solid #3475A8;
    border-radius:20px;
    padding:20px;
}

div[data-testid="stChatMessage"] {
    background:rgba(13,37,64,.96);
    border:1px solid #294D70;
    border-radius:16px;
    padding:14px;
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
    min-height:42px;
}

.footer {
    text-align:center;
    color:#B5C9DC;
    font-size:.85rem;
    padding:24px 0 8px;
}

[data-testid="stMetric"] {
    background:#102B49;
    padding:15px;
    border-radius:14px;
    border:1px solid #28527A;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIGN UP PAGE
# =========================================================

def signup_page():

    st.markdown("""
    <div class="hero">
        <h1>🎓 Create Your Account</h1>
        <p>Join Muhammad Abdullah School AI</p>
        <p>Your personal school learning platform.</p>
    </div>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.7, 1])

    with center:

        st.markdown("### 📝 Student Registration")

        with st.form("registration_form"):

            name = st.text_input(
                "Full Name",
                placeholder="Enter your full name"
            )

            email = st.text_input(
                "Email Address",
                placeholder="example@email.com"
            )

            grade = st.selectbox(
                "Select Your Class",
                [f"Class {i}" for i in range(1, 11)]
            )

            password = st.text_input(
                "Create Password",
                type="password"
            )

            confirm = st.text_input(
                "Confirm Password",
                type="password"
            )

            agree = st.checkbox(
                "I confirm that the information is correct."
            )

            submit = st.form_submit_button(
                "🚀 Create Account",
                use_container_width=True
            )

            if submit:

                users = load_users()
                email = email.strip().lower()

                if not name.strip() or not email or not password:
                    st.error("Please complete all required fields.")

                elif not re.fullmatch(
                    r"[^@\s]+@[^@\s]+\.[^@\s]+",
                    email
                ):
                    st.error("Please enter a valid email.")

                elif len(password) < 8:
                    st.error("Password must be at least 8 characters.")

                elif password != confirm:
                    st.error("Passwords do not match.")

                elif not agree:
                    st.error("Please confirm your information.")

                elif email in users:
                    st.error("This account already exists. Please sign in.")

                else:

                    users[email] = {
                        "name": name.strip(),
                        "grade": grade,
                        "password": make_password(password),
                        "created_at": datetime.now().isoformat()
                    }

                    save_users(users)

                    # AUTOMATIC LOGIN AFTER SIGNUP
                    login_user(email, users[email])

        st.write("")

        if st.button(
            "Already have an account? Sign In",
            use_container_width=True
        ):
            st.session_state.page = "signin"
            st.rerun()


# =========================================================
# SIGN IN PAGE
# =========================================================

def signin_page():

    st.markdown("""
    <div class="hero">
        <h1>🎓 Muhammad Abdullah School AI</h1>
        <p>Welcome back to your smart learning platform.</p>
        <p>Learn • Practice • Improve</p>
    </div>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.7, 1])

    with center:

        st.markdown("### 🔐 Student Sign In")

        with st.form("login_form"):

            email = st.text_input(
                "Email Address",
                placeholder="Enter your registered email"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            submit = st.form_submit_button(
                "🔓 Sign In",
                use_container_width=True
            )

            if submit:

                users = load_users()
                email = email.strip().lower()
                user = users.get(email)

                if user and check_password(
                    password,
                    user.get("password", {})
                ):

                    login_user(email, user)

                else:
                    st.error("Incorrect email or password.")

        st.write("")

        if st.button(
            "New Student? Create Account",
            use_container_width=True
        ):
            st.session_state.page = "signup"
            st.rerun()


# =========================================================
# BUILT-IN OFFLINE KNOWLEDGE BASE
# =========================================================

KNOWLEDGE = {

    "photosynthesis": """
### 🌱 Photosynthesis

Photosynthesis is the process by which green plants make their food.

Plants need:
1. Sunlight
2. Water
3. Carbon dioxide

Oxygen is released during this process.

**Remember:** Photosynthesis helps plants prepare food.
""",

    "fraction": """
### 📐 Fractions

A fraction represents a part of a whole.

Example: 1/2

- 1 = Numerator
- 2 = Denominator

Example: If a pizza has two equal pieces and you take one,
you have 1/2 of the pizza.
""",

    "noun": """
### 📖 Noun

A noun is the name of a person, place, animal or thing.

Examples:
- Person: Teacher
- Place: School
- Animal: Cat
- Thing: Book
""",

    "verb": """
### ✍️ Verb

A verb tells us about an action or state.

Examples:
- Run
- Eat
- Write
- Read
- Play
""",

    "adjective": """
### 📚 Adjective

An adjective describes a noun.

Examples:
- Beautiful flower
- Clever student
- Red car
- Tall building
""",

    "planet": """
### 🌍 Solar System

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
### 💻 Computer

A computer is an electronic machine that processes data.

Main parts:
1. Input devices
2. CPU
3. Memory
4. Output devices

Examples of input devices: Keyboard and mouse.
""",

    "water": """
### 💧 Water

Water is essential for life.

Its chemical formula is H₂O.

Uses:
- Drinking
- Cooking
- Cleaning
- Agriculture
""",

    "pakistan": """
### 🇵🇰 Pakistan

Pakistan became independent on 14 August 1947.

Founder: Quaid-e-Azam Muhammad Ali Jinnah.

Capital: Islamabad.

National language: Urdu.
""",

    "gravity": """
### 🌎 Gravity

Gravity is a force of attraction between objects.

Earth's gravity keeps us on the ground
and causes objects to fall toward Earth.
""",

    "solar system": """
### ☀️ Solar System

The solar system consists of the Sun
and the objects that orbit around it.

It includes eight planets, moons,
asteroids and comets.
""",

    "atom": """
### ⚛️ Atom

An atom is the basic unit of an element.

It contains:
1. Protons
2. Neutrons
3. Electrons
""",

    "democracy": """
### 🏛️ Democracy

Democracy is a system of government
in which people participate in choosing their leaders.
"""
}


# =========================================================
# SAFE MATHEMATICS CALCULATOR
# =========================================================

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos
}


def calculate_expression(expression):

    try:

        if len(expression) > 60:
            return None

        tree = ast.parse(expression, mode="eval")

        def evaluate(node):

            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant):
                if type(node.value) in (int, float):
                    return node.value
                raise ValueError()

            if isinstance(node, ast.BinOp):
                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError()

                left = evaluate(node.left)
                right = evaluate(node.right)

                if isinstance(node.op, ast.Pow) and abs(right) > 10:
                    raise ValueError()

                result = operation(left, right)

                if abs(result) > 10**15:
                    raise ValueError()

                return result

            if isinstance(node, ast.UnaryOp):
                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError()

                return operation(evaluate(node.operand))

            raise ValueError()

        result = evaluate(tree)

        if not isinstance(result, (int, float)):
            return None

        return result

    except (
        ValueError,
        TypeError,
        SyntaxError,
        ZeroDivisionError,
        OverflowError
    ):
        return None


# =========================================================
# CHATBOT RESPONSE ENGINE
# =========================================================

def get_answer(question, subject, language, mode, grade):

    q = question.lower().strip()

    # GREETINGS
    if any(word in q for word in [
        "hello", "hi", "hey", "salam",
        "assalam", "good morning", "good evening"
    ]):

        return f"""
Hello {st.session_state.user_name}! 👋

Welcome to **Muhammad Abdullah School AI**.

I am your offline study assistant.

Your class: **{grade}**

You can ask me about:
- Mathematics
- English
- Urdu
- Science
- Computer
- Pakistan Studies

How can I help you today?
"""

    # BUILT-IN KNOWLEDGE
    for keyword, answer in KNOWLEDGE.items():

        if keyword in q:
            return answer

    # MATHEMATICS
    if re.fullmatch(r"[\d\s+\-*/().]+", q):

        result = calculate_expression(q)

        if result is not None:
            return f"""
### 🧮 Mathematics Answer

**Question:** `{question}`

**Answer:** {result}

Great work! Keep practising.
"""

    # QUIZ GENERATOR
    if "quiz" in q or mode == "Create Practice Quiz":

        return """
### 📝 School Practice Quiz

**Question 1:** What is photosynthesis?

**Question 2:** What is a noun?

**Question 3:** How many planets are in our solar system?

**Question 4:** What is the chemical formula of water?

**Question 5:** Who founded Pakistan?

---

### Answer Key

1. Process by which plants make food.
2. Name of a person, place, animal or thing.
3. Eight.
4. H₂O.
5. Muhammad Ali Jinnah.
"""

    # REVISION NOTES
    if mode == "Make Revision Notes" or "notes" in q:

        return f"""
### 📚 Revision Notes

**Selected Subject:** {subject}

**Student Class:** {grade}

1. Read the topic carefully.
2. Learn important definitions.
3. Remember the main points.
4. Practise examples.
5. Revise regularly.

For detailed notes, ask about a specific topic.
"""

    # EXAMPLES
    if mode == "Give Examples":

        return """
### ✍️ Educational Examples

**Noun:** Book, Teacher, School.

**Verb:** Run, Read, Write.

**Adjective:** Beautiful, Clever, Happy.

**Mathematics:** 5 + 5 = 10.

**Science:** Water = H₂O.
"""

    # LANGUAGE
    if language == "Urdu":

        return """
مجھے اس سوال کا مکمل جواب اپنے آف لائن ڈیٹا میں نہیں ملا۔

آپ ان موضوعات کے بارے میں پوچھ سکتے ہیں:

- Photosynthesis
- Fractions
- Noun
- Verb
- Planets
- Computer
- Water
- Pakistan

میں آپ کے سوالات کے مطابق اپنے موجودہ علم سے مدد کرنے کی کوشش کروں گا۔
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

Aap apna sawal kisi specific topic ke sath likhein.
"""

    # DEFAULT
    return f"""
### 🎓 Muhammad Abdullah School AI

I couldn't find a matching answer in my offline knowledge base.

**Your Class:** {grade}

**Selected Subject:** {subject}

**Try asking:**

- What is photosynthesis?
- Explain fractions.
- What is a noun?
- What is a verb?
- Explain planets.
- What is gravity?
- What is a computer?
- Tell me about Pakistan.

**Study Tip:** Ask one clear question at a time.

<small>This is a rule-based offline chatbot, not a live generative AI model.</small>
"""


# =========================================================
# CHAT PAGE
# =========================================================

def chatbot_page():

    # SIDEBAR
    with st.sidebar:

        st.title("🎓 School AI")

        st.caption("Student Dashboard")

        st.divider()

        st.success(
            "👤 " + st.session_state.user_name
        )

        st.write(
            "🎓 " + st.session_state.grade
        )

        st.divider()

        if st.button("➕ New Chat", use_container_width=True):

            st.session_state.messages = []
            st.session_state.new_chat_count += 1
            st.rerun()

        subject = st.selectbox(
            "📚 Choose Subject",
            SUBJECTS
        )

        language = st.selectbox(
            "🌐 Answer Language",
            LANGUAGES
        )

        mode = st.selectbox(
            "🧠 Study Mode",
            STUDY_MODES
        )

        st.divider()

        st.caption("LEARN • PRACTISE • IMPROVE")

        with st.expander("👤 Student Profile"):

            st.write("**Name:** " + st.session_state.user_name)
            st.write("**Email:** " + st.session_state.user_email)
            st.write("**Class:** " + st.session_state.grade)

        st.divider()

        if st.button("🗑️ Clear Chat", use_container_width=True):

            st.session_state.messages = []
            st.rerun()

        if st.button("🚪 Logout", use_container_width=True):

            logout_user()

    # HEADER
    st.markdown("""
    <div class="hero">
        <h1>🎓 Muhammad Abdullah School AI</h1>
        <p>Your smart and friendly school learning assistant.</p>
        <p>Learn • Practice • Improve</p>
    </div>
    """, unsafe_allow_html=True)

    # WELCOME
    st.markdown(
        f"### Hello, {st.session_state.user_name}! 👋"
    )

    st.caption(
        "Your personal educational assistant is ready."
    )

    # FEATURE CARDS
    c1, c2, c3 = st.columns(3)

    for col, heading, detail in [
        (c1, "📚 Classes 1–10", "School-level learning"),
        (c2, "🧠 All Subjects", "Multiple study subjects"),
        (c3, "✍️ Study Tools", "Notes, quizzes and maths")
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

    # SUGGESTIONS
    with st.expander("💡 Try These Questions"):

        suggestions = [
            "What is photosynthesis?",
            "Explain fractions",
            "What is a noun?",
            "What is gravity?",
            "Tell me about Pakistan",
            "Create a quiz"
        ]

        for item in suggestions:

            if st.button(item, key="suggest_" + item):
                st.session_state.messages.append({
                    "role": "user",
                    "content": item
                })

                answer = get_answer(
                    item,
                    subject,
                    language,
                    mode,
                    st.session_state.grade
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                st.rerun()

    st.divider()

    st.subheader("💬 School AI Chat")

    st.caption(
        "Ask questions, learn topics and practise your lessons."
    )

    # CHAT HISTORY
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # CHAT INPUT
    question = st.chat_input(
        "Message Muhammad Abdullah School AI..."
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

    # FOOTER
    st.markdown("""
    <div class="footer">
        🎓 Muhammad Abdullah School AI
        <br>
        Professional Offline Educational Platform
        <br>
        Created by Muhammad Abdullah
        <br>
        No API • No Gemini • No API Key
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# APPLICATION ROUTER
# =========================================================

if st.session_state.logged_in:

    chatbot_page()

elif st.session_state.page == "signup":

    signup_page()

else:

    signin_page()
