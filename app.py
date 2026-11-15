"""
Muhammad Abdullah School AI
---------------------------
A Streamlit learning assistant for Class 1-10 students.

Features: password login, offline knowledge-base chatbot (English / Urdu /
Roman Urdu), optional Claude AI for unknown questions, calculator, notes,
quiz and study planner.

Run:  streamlit run app.py
"""

from __future__ import annotations

import ast
import difflib
import hmac
import html
import json
import operator
import os
import random
import re
import uuid
from datetime import date, datetime
from pathlib import Path

import streamlit as st

try:  # Optional: only needed for AI mode
    import anthropic
except ImportError:  # pragma: no cover
    anthropic = None

# ==================================================
# 1. APP CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="School AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_NAME = "Muhammad Abdullah School AI"
MAX_LOGIN_ATTEMPTS = 5

DATA_DIR = Path(os.getenv("SCHOOL_AI_DATA_DIR", "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
NOTES_FILE = DATA_DIR / "school_ai_notes.json"
PLANNER_FILE = DATA_DIR / "school_ai_planner.json"

CLASSES = [f"Class {i}" for i in range(1, 11)]
SUBJECTS = [
    "Mathematics", "English", "Urdu", "Physics", "Chemistry", "Biology",
    "Computer Science", "General Science", "Islamiat", "Pakistan Studies",
    "History", "Geography", "General Knowledge", "Other",
]
LANGUAGES = ["Simple English", "Urdu", "Roman Urdu"]


def get_secret(name: str, default: str | None = None) -> str | None:
    """Read a value from Streamlit secrets, then environment variables."""
    try:
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass
    return os.getenv(name, default)


AI_MODEL = get_secret("CHATBOT_MODEL", "claude-sonnet-5-5")


def ai_available() -> bool:
    return anthropic is not None and bool(get_secret("ANTHROPIC_API_KEY"))


# ==================================================
# 2. SESSION STATE
# ==================================================

DEFAULTS = {
    "authenticated": False,
    "attempts": 0,
    "messages": [],
    "student_class": "Class 10",
    "subject": "Mathematics",
    "language": "Simple English",
    "use_ai": True,
    "quiz_version": 0,
}
for _key, _value in DEFAULTS.items():
    if _key not in st.session_state:
        st.session_state[_key] = _value

# ==================================================
# 3. STYLING
# ==================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu&display=swap');

.stApp { background: linear-gradient(135deg, #071426, #102d50); color: #ffffff; }
[data-testid="stSidebar"] { background: #081a30; }

.main-title { text-align: center; font-size: 36px; font-weight: 900; color: #55c7ff; }
.subtitle { text-align: center; color: #c4d9ee; font-size: 16px; }

.panel {
    background: rgba(22, 55, 88, 0.75);
    border: 1px solid #28547c;
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 12px;
}

div.stButton > button, div.stFormSubmitButton > button {
    background: #078bd5; color: white; border: none;
    border-radius: 10px; font-weight: bold; min-height: 42px;
}
div.stButton > button:hover, div.stFormSubmitButton > button:hover {
    background: #0069a8; color: white;
}

h1, h2, h3 { color: #67caff; }

.rtl {
    direction: rtl; text-align: right;
    font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', serif;
    line-height: 2.1;
}
.done { text-decoration: line-through; opacity: 0.6; }
</style>
""",
    unsafe_allow_html=True,
)

# ==================================================
# 4. STORAGE HELPERS
# ==================================================


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(path: Path, data) -> None:
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    tmp.replace(path)  # atomic write


def load_items(path: Path) -> list[dict]:
    """Load a list of records and make sure each has a unique id."""
    items = load_json(path, [])
    if not isinstance(items, list):
        return []
    changed = False
    for item in items:
        if "id" not in item:
            item["id"] = uuid.uuid4().hex
            changed = True
    if changed:
        save_json(path, items)
    return items


# ==================================================
# 5. KNOWLEDGE BASE  (answer, subject)
# ==================================================

KNOWLEDGE: dict[str, tuple[str, str]] = {
    # ---- Computer Science
    "what is computer": ("A computer is an electronic device that accepts data, processes it, stores it and produces information.", "Computer Science"),
    "what is ai": ("Artificial Intelligence (AI) is a branch of computer science that develops systems able to perform tasks such as recognizing patterns, understanding language and solving problems.", "Computer Science"),
    "what is internet": ("The Internet is a worldwide network of connected computers and devices that exchange information.", "Computer Science"),
    "what is website": ("A website is a collection of connected web pages that people can access through a web browser.", "Computer Science"),
    "what is python": ("Python is a high-level programming language known for readable syntax. It is used in automation, data science, websites and AI.", "Computer Science"),
    "what is algorithm": ("An algorithm is a step-by-step procedure for solving a problem or completing a task.", "Computer Science"),
    "what is hardware": ("Hardware means the physical parts of a computer, such as the keyboard, mouse, monitor and processor.", "Computer Science"),
    "what is software": ("Software is a set of programs and instructions that tell a computer what to do.", "Computer Science"),
    "what is cpu": ("CPU stands for Central Processing Unit. It executes instructions and performs calculations in a computer.", "Computer Science"),
    "what is ram": ("RAM stands for Random Access Memory. It temporarily stores data that the computer is currently using.", "Computer Science"),
    # ---- Biology
    "what is photosynthesis": ("Photosynthesis is the process by which green plants use sunlight, water and carbon dioxide to make glucose and release oxygen.", "Biology"),
    "what is cell": ("A cell is the basic structural and functional unit of life. All living organisms are made of one or more cells.", "Biology"),
    "what is nucleus": ("The nucleus is a cell organelle that contains genetic material and helps control cell activities.", "Biology"),
    "what is dna": ("DNA stands for Deoxyribonucleic Acid. It carries genetic information in living organisms.", "Biology"),
    "what is ecosystem": ("An ecosystem includes living organisms and the non-living environment interacting with one another.", "Biology"),
    "what is respiration": ("Respiration is the process by which cells release energy from food molecules.", "Biology"),
    # ---- Chemistry
    "what is atom": ("An atom is the smallest unit of an element that retains the chemical properties of that element.", "Chemistry"),
    "what is molecule": ("A molecule consists of two or more atoms chemically bonded together.", "Chemistry"),
    "what is element": ("An element is a pure substance made up of atoms that have the same number of protons.", "Chemistry"),
    "what is compound": ("A compound is a pure substance formed when two or more different elements chemically combine in fixed proportions.", "Chemistry"),
    "what is acid": ("An acid is a substance that donates hydrogen ions in an aqueous solution. Many common acids have a pH below 7.", "Chemistry"),
    # ---- Physics
    "what is gravity": ("Gravity is the attractive force between objects that have mass. Earth's gravity pulls objects toward its centre.", "Physics"),
    "what is force": ("Force is a push or pull that can change an object's motion or shape. Its SI unit is the newton.", "Physics"),
    "what is energy": ("Energy is the capacity to do work or cause change. Common forms include kinetic, potential, thermal and electrical energy.", "Physics"),
    "what is speed": ("Speed is the distance travelled per unit of time. Formula: Speed = Distance / Time.", "Physics"),
    "what is electricity": ("Electricity involves electric charges and their movement. It is used to power many everyday devices.", "Physics"),
    # ---- Mathematics
    "what is mathematics": ("Mathematics is the study of numbers, quantities, shapes, patterns and logical relationships.", "Mathematics"),
    "what is algebra": ("Algebra is a branch of mathematics that uses letters and symbols to represent unknown values.", "Mathematics"),
    "what is geometry": ("Geometry is the branch of mathematics that studies points, lines, angles, shapes and space.", "Mathematics"),
    "what is percentage": ("A percentage is a number expressed as a fraction of 100. For example, 25% means 25 out of 100.", "Mathematics"),
    # ---- English
    "what is english": ("English is a language used for communication, education, literature and international exchange.", "English"),
    "what is noun": ("A noun is a word used to name a person, place, thing or idea. Examples include teacher, school, book and honesty.", "English"),
    "what is verb": ("A verb is a word that expresses an action or a state of being. Examples include run, write, think and is.", "English"),
    "what is adjective": ("An adjective describes a noun or pronoun. Examples include beautiful, tall, clever and blue.", "English"),
    # ---- Pakistan Studies / History / Geography
    "what is pakistan": ("Pakistan is a country in South Asia. It became independent on 14 August 1947.", "Pakistan Studies"),
    "who founded pakistan": ("Muhammad Ali Jinnah is widely known as the founder of Pakistan and its first Governor-General.", "Pakistan Studies"),
    "when pakistan became independent": ("Pakistan became independent on 14 August 1947.", "Pakistan Studies"),
    "what is democracy": ("Democracy is a system of government in which people participate in choosing their representatives.", "History"),
    "what is geography": ("Geography is the study of Earth, its physical features, people, places and environments.", "Geography"),
    "what is history": ("History is the study of past events and human societies using evidence and historical sources.", "History"),
    # ---- General Science
    "what is water": ("Water is a substance essential for life. A water molecule contains two hydrogen atoms and one oxygen atom: H2O.", "General Science"),
    "what is environment": ("The environment includes the surroundings, conditions and natural systems in which living organisms exist.", "General Science"),
    # ---- Islamiat
    "what is islam": ("Islam is a monotheistic religion. Muslims believe in one God, Allah, and follow the teachings of the Quran and Prophet Muhammad (peace be upon him).", "Islamiat"),
    "what is zakat": ("Zakat is an obligatory form of charity in Islam for eligible Muslims who meet the required conditions.", "Islamiat"),
    "what is ramadan": ("Ramadan is the ninth month of the Islamic lunar calendar. Muslims who are able observe fasting during this month.", "Islamiat"),
}

URDU_ANSWERS = {
    "what is computer": "کمپیوٹر ایک الیکٹرانک مشین ہے جو ڈیٹا وصول کرتی ہے، اسے پراسیس کرتی ہے، محفوظ کرتی ہے اور معلومات فراہم کرتی ہے۔",
    "what is ai": "مصنوعی ذہانت (AI) کمپیوٹر سائنس کی ایک شاخ ہے جو مشینوں کو مختلف ذہین کام کرنے کے قابل بناتی ہے۔",
    "what is internet": "انٹرنیٹ دنیا بھر کے کمپیوٹرز اور آلات کا ایک نیٹ ورک ہے جو معلومات کا تبادلہ کرتا ہے۔",
    "what is photosynthesis": "ضیائی تالیف وہ عمل ہے جس میں سبز پودے سورج کی روشنی، پانی اور کاربن ڈائی آکسائیڈ کی مدد سے خوراک بناتے ہیں۔",
    "what is cell": "خلیہ زندگی کی بنیادی ساختی اور فعلی اکائی ہے۔ تمام جاندار ایک یا زیادہ خلیوں سے بنے ہوتے ہیں۔",
    "what is gravity": "کششِ ثقل وہ قوت ہے جو اجسام کو ایک دوسرے کی طرف کھینچتی ہے۔ زمین کی کشش ہمیں زمین پر رکھتی ہے۔",
    "what is pakistan": "پاکستان جنوبی ایشیا کا ایک ملک ہے۔ پاکستان 14 اگست 1947 کو آزاد ہوا۔",
    "what is force": "قوت کسی چیز کو دھکا دینے یا کھینچنے کا عمل ہے۔ قوت کی SI اکائی نیوٹن ہے۔",
    "what is water": "پانی زندگی کے لیے ضروری ہے۔ اس کا کیمیائی فارمولا H2O ہے۔",
}

GREETINGS = {"hello", "hi", "hey", "salam", "assalamualaikum", "assalam"}

# ==================================================
# 6. CHATBOT ENGINE
# ==================================================


def normalize(question: str) -> str:
    """Lower-case, strip punctuation and rewrite 'define X' as 'what is X'."""
    q = question.lower().strip()
    q = re.sub(r"[^\w\s']", " ", q)
    q = re.sub(r"\s+", " ", q).strip()
    q = q.replace("what's", "what is").replace("whats", "what is")
    q = re.sub(
        r"^(define|explain|describe|meaning of|tell me about|what are|what do you mean by)\s+",
        "what is ",
        q,
    )
    q = re.sub(r"^what is (an?|the) ", "what is ", q)
    return q


def find_in_knowledge(question: str) -> str | None:
    """Return the matching knowledge-base key, or None."""
    nq = normalize(question)
    if nq in KNOWLEDGE:
        return nq

    # Whole-phrase match (word boundaries, so 'air' never matches 'ai').
    for key in KNOWLEDGE:
        if re.search(rf"\b{re.escape(key)}\b", nq):
            return key

    # Typo tolerance for longer topics only (acronyms need exact matches).
    topic = nq.removeprefix("what is ")
    best_key, best_score = None, 0.0
    if len(topic) >= 5:
        for key in KNOWLEDGE:
            candidate = key.removeprefix("what is ")
            if len(candidate) < 5:
                continue
            score = difflib.SequenceMatcher(None, topic, candidate).ratio()
            if score > best_score:
                best_key, best_score = key, score
    return best_key if best_score >= 0.85 else None


def ask_ai(question, subject, language, student_class, history) -> str | None:
    """Ask Claude. Returns None if AI is unavailable or the call fails."""
    if not ai_available():
        return None

    system = (
        "You are a friendly, accurate school tutor for students in Pakistan. "
        f"The student is in {student_class} and is studying {subject}. "
        f"Answer in {language}. Keep answers clear, correct, age-appropriate "
        "and reasonably short, with a simple example when helpful. "
        "If a request is unsafe or not educational, politely redirect to studying."
    )
    messages = [
        {"role": m["role"], "content": m["content"]}
        for m in history[-10:]
        if m["role"] in ("user", "assistant")
    ]
    while messages and messages[0]["role"] != "user":
        messages.pop(0)
    messages.append({"role": "user", "content": question})

    try:
        client = anthropic.Anthropic(api_key=get_secret("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model=AI_MODEL,
            max_tokens=800,
            system=system,
            messages=messages,
        )
        return "".join(b.text for b in response.content if b.type == "text").strip()
    except Exception:
        return None


def chatbot(question, subject, language, student_class, history) -> tuple[str, str]:
    """Return (answer, source)."""
    q = normalize(question)
    if not q:
        return "Please enter a question.", "System"

    words = q.split()
    if words and words[0] in GREETINGS and len(words) <= 3:
        if language == "Urdu":
            return "السلام علیکم! میں آپ کا School AI Assistant ہوں۔ اپنا سوال پوچھیں۔", "System"
        if language == "Roman Urdu":
            return "Assalamualaikum! Main aap ka School AI Assistant hoon. Apna sawal poochain.", "System"
        return "Hello! Welcome to Muhammad Abdullah School AI. What would you like to learn today?", "System"

    key = find_in_knowledge(question)
    if key:
        answer, topic_subject = KNOWLEDGE[key]
        if language == "Urdu":
            return URDU_ANSWERS.get(key, answer), "Knowledge base"
        if language == "Roman Urdu":
            return "Jawab: " + answer, "Knowledge base"
        return (
            f"**Answer:** {answer}  \n"
            f"**Subject:** {topic_subject}  \n"
            f"**Class:** {student_class}",
            "Knowledge base",
        )

    if any(w in q for w in ("calculate", "solve", "plus", "minus", "multiply")):
        return (
            "I can help with basic calculations. Open the **Calculator** page "
            "and enter a mathematical expression.",
            "System",
        )

    if st.session_state.use_ai:
        ai_answer = ask_ai(question, subject, language, student_class, history)
        if ai_answer:
            return ai_answer, "AI tutor"

    if language == "Urdu":
        return (
            f"آپ کا سوال {subject} کے بارے میں موصول ہوا ہے۔ اس سوال کا تیار شدہ جواب "
            "موجود نہیں۔ براہ کرم سوال کو آسان الفاظ میں لکھیں۔",
            "System",
        )
    if language == "Roman Urdu":
        return (
            f"Aap ka sawal {subject} ke bare mein hai. Is sawal ka tayyar jawab mojood nahi. "
            "Meherbani karke sawal asaan alfaaz mein likhein.",
            "System",
        )
    return (
        f"I received your question about **{subject}** for **{student_class}**, "
        "but I do not have a prepared answer for it. Try different words, or "
        "choose a related topic.",
        "System",
    )


# ==================================================
# 7. SAFE CALCULATOR
# ==================================================

BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}
UNARY_OPS = {ast.USub: operator.neg, ast.UAdd: operator.pos}


def safe_calculate(expression: str):
    expression = (
        expression.replace("^", "**").replace("×", "*").replace("÷", "/").strip()
    )
    if not expression or len(expression) > 100:
        raise ValueError("Invalid expression")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in BINARY_OPS:
            left, right = evaluate(node.left), evaluate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent too large")
            result = BINARY_OPS[type(node.op)](left, right)
            if abs(result) > 10**12:
                raise ValueError("Result too large")
            return result
        if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPS:
            return UNARY_OPS[type(node.op)](evaluate(node.operand))
        raise ValueError("Invalid expression")

    result = evaluate(ast.parse(expression, mode="eval"))
    if isinstance(result, float):
        result = int(result) if result.is_integer() else round(result, 10)
    return result


# ==================================================
# 8. LOGIN
# ==================================================


def login_screen() -> None:
    st.markdown(f'<div class="main-title">🎓 {APP_NAME}</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your Professional Learning Assistant</div>', unsafe_allow_html=True)
    st.write("")

    _, center, _ = st.columns([1, 1.3, 1])
    with center:
        expected = get_secret("APP_PASSWORD")

        if not expected:
            st.error("No password is configured.")
            st.markdown(
                "Create `.streamlit/secrets.toml` next to `app.py` and add:"
            )
            st.code('APP_PASSWORD = "choose-a-strong-password"', language="toml")
            return

        st.subheader("🔐 Secure Login")
        locked = st.session_state.attempts >= MAX_LOGIN_ATTEMPTS

        with st.form("login_form"):
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("🚀 Open School AI", use_container_width=True)

        if submitted:
            if locked:
                st.error("Too many failed attempts. Refresh the page to try again.")
            elif hmac.compare_digest(password.encode(), expected.encode()):
                st.session_state.authenticated = True
                st.session_state.attempts = 0
                st.rerun()
            else:
                st.session_state.attempts += 1
                left = MAX_LOGIN_ATTEMPTS - st.session_state.attempts
                st.error(f"Incorrect password. Attempts left: {max(left, 0)}")

        st.caption(f"© {APP_NAME}")


# ==================================================
# 9. PAGES
# ==================================================


def home_page() -> None:
    st.markdown('<div class="main-title">Welcome to School AI 🎓</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Learn Smarter • Study Better • Achieve More</div>', unsafe_allow_html=True)
    st.write("")

    notes = load_items(NOTES_FILE)
    tasks = load_items(PLANNER_FILE)
    pending = sum(1 for t in tasks if not t.get("completed"))

    a, b, c, d = st.columns(4)
    a.metric("Subjects", len(SUBJECTS))
    b.metric("Knowledge Topics", len(KNOWLEDGE))
    c.metric("Saved Notes", len(notes))
    d.metric("Pending Tasks", pending)

    st.divider()
    st.subheader("🚀 Learning Tools")

    cards = [
        ("🤖 AI Chatbot", "Ask educational questions."),
        ("🧮 Calculator", "Solve basic maths problems."),
        ("📝 Notes", "Write and save study notes."),
        ("🧠 Quiz", "Test your knowledge."),
        ("📅 Study Planner", "Organize your study tasks."),
        ("📚 Knowledge Base", "Explore prepared questions."),
    ]
    columns = st.columns(3)
    for i, (title, description) in enumerate(cards):
        with columns[i % 3]:
            st.markdown(
                f'<div class="panel"><h3>{title}</h3><p>{description}</p></div>',
                unsafe_allow_html=True,
            )

    if ai_available():
        st.success("AI tutor is connected. Unknown questions are answered by AI.")
    else:
        st.info("Running in offline mode: answers come from the built-in knowledge base.")


def render_message(msg: dict) -> None:
    with st.chat_message(msg["role"]):
        if msg.get("rtl"):
            safe = html.escape(msg["content"]).replace("\n", "<br>")
            st.markdown(f'<div class="rtl">{safe}</div>', unsafe_allow_html=True)
        else:
            st.markdown(msg["content"])
        if msg.get("source") and msg["source"] != "System":
            st.caption(f"Source: {msg['source']}")


def chatbot_page() -> None:
    st.title("🤖 School AI Chatbot")
    s = st.session_state
    st.caption(f"{s.student_class}  •  {s.subject}  •  {s.language}  (change in the sidebar)")

    for message in s.messages:
        render_message(message)

    question = st.chat_input("Ask your educational question...")
    if question:
        history = list(s.messages)
        s.messages.append({"role": "user", "content": question})
        with st.spinner("Thinking..."):
            answer, source = chatbot(question, s.subject, s.language, s.student_class, history)
        s.messages.append(
            {"role": "assistant", "content": answer, "source": source, "rtl": s.language == "Urdu"}
        )
        st.rerun()

    if s.messages and st.button("🗑️ Clear Conversation"):
        s.messages = []
