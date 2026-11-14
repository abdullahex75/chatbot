
import streamlit as st
import ast
import operator
import json
import os
from datetime import datetime

# -------------------------------
# PAGE SETTINGS
# -------------------------------
st.set_page_config(
    page_title="Muhammad Abdullah School AI",
    page_icon="🎓",
    layout="wide"
)

# -------------------------------
# LOGIN SETTINGS
# -------------------------------
APP_PASSWORD = "Muhammad Abdullah"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# DATABASE
# -------------------------------
NOTES_FILE = "school_notes.json"

def load_notes():
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []

def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)

# -------------------------------
# DESIGN
# -------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #061426, #102e50);
    color: white;
}
.title {
    text-align: center;
    color: #52c8ff;
    font-size: 38px;
    font-weight: 900;
}
.subtitle {
    text-align: center;
    color: #d0e4f5;
    font-size: 17px;
}
div.stButton > button {
    background: #078bd5;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: bold;
    width: 100%;
}
div.stButton > button:hover {
    background: #0069a8;
    color: white;
}
[data-testid="stSidebar"] {
    background: #091b30;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# OFFLINE KNOWLEDGE BASE
# -------------------------------
def get_answer(question, subject, language):
    q = question.lower().strip()

    knowledge = {
        "hello": "Hello! Welcome to Muhammad Abdullah School AI. How can I help you?",
        "hi": "Hi! Ask me any school question.",
        "what is ai": "AI stands for Artificial Intelligence. It helps computers perform tasks that normally require human intelligence.",
        "what is computer": "A computer is an electronic machine that accepts data, processes it, stores it and gives information.",
        "what is science": "Science is the systematic study of the natural world through observation and experiments.",
        "what is mathematics": "Mathematics is the study of numbers, shapes, patterns and calculations.",
        "what is internet": "The Internet is a worldwide network that connects computers and shares information.",
        "what is website": "A website is a collection of web pages that people can access through the Internet.",
        "what is python": "Python is a programming language used for software, websites, automation and AI projects.",
        "what is water": "Water is essential for life. Its chemical formula is H2O.",
        "what is photosynthesis": "Photosynthesis is the process by which green plants use sunlight, water and carbon dioxide to make food.",
        "what is gravity": "Gravity is the force that attracts objects toward one another.",
        "what is pakistan": "Pakistan is a country in South Asia. It became independent on 14 August 1947.",
        "what is english": "English is a language used for communication around the world."
    }

    for key, answer in knowledge.items():
        if key in q:
            return answer

    if language == "Urdu":
        return (
            "آپ کا سوال موصول ہوگیا ہے۔ یہ آف لائن ڈیمو چیٹ بوٹ ہے۔ "
            "براہِ کرم سوال آسان الفاظ میں لکھیں یا دوسرا سوال پوچھیں۔"
        )

    if language == "Roman Urdu":
        return (
            "Aap ka sawal mil gaya hai. Yeh offline demo chatbot hai. "
            "Meherbani karke sawal asaan alfaaz mein likhein."
        )

    return (
        f"Your question about {subject} has been received. "
        "I am an offline demo chatbot, so I do not have an answer "
        "for every question yet. Please try a simpler question."
    )

# -------------------------------
# SAFE CALCULATOR
# -------------------------------
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod
}

def calculate(expression):
    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Power too large")

            result = OPS[type(node.op)](left, right)

            if abs(result) > 10**12:
                raise ValueError("Result too large")

            return result

        if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
            return OPS[type(node.op)](evaluate(node.operand))

        raise ValueError("Invalid calculation")

    return evaluate(ast.parse(expression, mode="eval"))

# -------------------------------
# LOGIN PAGE
# -------------------------------
def login_page():
    st.markdown(
        '<div class="title">🎓 Muhammad Abdullah School AI</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">Your Smart School Learning Assistant</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    left, center, right = st.columns([1, 1.2, 1])

    with center:
        st.markdown("### 🔐 Welcome Back")
        st.write("Enter your password to open School AI.")

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        if st.button("🚀 Open School AI"):
            if password == APP_PASSWORD:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")

        st.caption("© Muhammad Abdullah School AI")

# -------------------------------
# MAIN DASHBOARD
# -------------------------------
def dashboard():
    st.sidebar.title("🎓 School AI")
    st.sidebar.write("Welcome, Muhammad Abdullah")

    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "🤖 AI Chatbot", "🧮 Calculator", "📝 Notes", "ℹ️ About"]
    )

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.messages = []
        st.rerun()

    if page == "🏠 Home":
        st.markdown(
            '<div class="title">Welcome to School AI</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="subtitle">Learn Smarter • Study Better • Grow Faster</div>',
            unsafe_allow_html=True
        )

        st.write("")
        a, b, c = st.columns(3)

        a.metric("Subjects", "14")
        b.metric("Study Assistant", "Online")
        c.metric("Mode", "Offline Demo")

        st.subheader("🚀 Your Learning Dashboard")
        st.write("Choose a feature from the sidebar to get started.")

        st.info(
            "This is an offline demo. It does not connect to an online AI service."
        )

    elif page == "🤖 AI Chatbot":
        st.title("🤖 School AI Chatbot")

        class_name = st.selectbox(
            "Select Your Class",
            [f"Class {i}" for i in range(1, 11)]
        )

        subject = st.selectbox(
            "Select Subject",
            [
                "Mathematics", "English", "Urdu", "Science",
                "Computer", "Physics", "Chemistry", "Biology",
                "Islamiat", "Pakistan Studies", "History",
                "Geography", "General Knowledge", "Other"
            ]
        )

        language = st.selectbox(
            "Answer Language",
            ["Simple English", "Urdu", "Roman Urdu"]
        )

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input("Ask your school question...")

        if question:
            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            with st.chat_message("user"):
                st.markdown(question)

            answer = get_answer(question, subject, language)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            with st.chat_message("assistant"):
                st.markdown(answer)

        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    elif page == "🧮 Calculator":
        st.title("🧮 School Calculator")
        expression = st.text_input(
            "Enter calculation",
            placeholder="Example: 25 * 4 + 10"
        )

        if st.button("Calculate"):
            try:
                result = calculate(expression)
                st.success(f"Answer: {result}")
            except Exception:
                st.error("Invalid calculation. Please try again.")

    elif page == "📝 Notes":
        st.title("📝 My Study Notes")

        notes = load_notes()
        title = st.text_input("Note Title")
        content = st.text_area("Write your notes here...")

        if st.button("Save Note"):
            if title.strip() and content.strip():
                notes.append({
                    "title": title.strip(),
                    "content": content.strip(),
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                save_notes(notes)
                st.success("Note saved successfully!")
                st.rerun()
            else:
                st.warning("Please enter a title and note.")

        st.divider()
        st.subheader("Saved Notes")

        for i, note in enumerate(notes):
            with st.expander(note["title"]):
                st.caption(note["date"])
                st.write(note["content"])

                if st.button("Delete Note", key=f"delete_{i}"):
                    notes.pop(i)
                    save_notes(notes)
                    st.rerun()

    elif page == "ℹ️ About":
        st.title("ℹ️ About School AI")
        st.write("""
        **Muhammad Abdullah School AI**

        A simple offline educational chatbot project.

        Features:
        - Student learning chatbot
        - Multiple school subjects
        - English, Urdu and Roman Urdu
        - Safe calculator
        - Study notes
        - Simple password login

        Version: 1.0
        """)

# -------------------------------
# APP START
# -------------------------------
if st.session_state.logged_in:
    dashboard()
else:
    login_page()
