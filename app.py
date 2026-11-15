
import streamlit as st
import json
import os
import ast
import operator
import random
from datetime import datetime, date

# ==================================================
# 1. APP CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Muhammad Abdullah",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

APP_NAME = "School AI chatbot"
APP_PASSWORD = "CES Abdullah"

NOTES_FILE = "school_ai_notes.json"
PLANNER_FILE = "school_ai_planner.json"

CLASSES = [f"Class {i}" for i in range(1, 11)]

SUBJECTS = [
    "Mathematics",
    "English",
    "Urdu",
    "Physics",
    "Chemistry",
    "Biology",
    "Computer Science",
    "General Science",
    "Islamiat",
    "Pakistan Studies",
    "History",
    "Geography",
    "General Knowledge",
    "Other"
]

# ==================================================
# 2. SESSION STATE
# ==================================================

defaults = {
    "authenticated": False,
    "messages": [],
    "student_class": "Class 10",
    "subject": "Mathematics",
    "language": "Simple English"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==================================================
# 3. PROFESSIONAL DESIGN
# ==================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #071426, #102d50);
    color: #ffffff;
}

[data-testid="stSidebar"] {
    background: #081a30;
}

.main-title {
    text-align: center;
    font-size: 36px;
    font-weight: 900;
    color: #55c7ff;
}

.subtitle {
    text-align: center;
    color: #c4d9ee;
    font-size: 16px;
}

.panel {
    background: rgba(22, 55, 88, 0.75);
    border: 1px solid #28547c;
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 12px;
}

div.stButton > button {
    background: #078bd5;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    min-height: 42px;
}

div.stButton > button:hover {
    background: #0069a8;
    color: white;
}

h1, h2, h3 {
    color: #67caff;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# 4. DATABASE FUNCTIONS
# ==================================================

def load_json(filename, default):
    if not os.path.exists(filename):
        return default

    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ==================================================
# 5. KNOWLEDGE BASE
# ==================================================

KNOWLEDGE = {
    "what is computer": {
        "answer": "A computer is an electronic device that accepts data, processes it, stores it and produces information.",
        "subject": "Computer Science"
    },

    "what is ai": {
        "answer": "Artificial Intelligence (AI) is a branch of computer science that develops systems able to perform tasks such as recognizing patterns, understanding language and solving problems.",
        "subject": "Computer Science"
    },

    "what is internet": {
        "answer": "The Internet is a worldwide network of connected computers and devices that exchange information.",
        "subject": "Computer Science"
    },

    "what is website": {
        "answer": "A website is a collection of connected web pages that people can access through a web browser.",
        "subject": "Computer Science"
    },

    "what is python": {
        "answer": "Python is a high-level programming language known for readable syntax. It is used in automation, data science, websites and AI.",
        "subject": "Computer Science"
    },

    "what is algorithm": {
        "answer": "An algorithm is a step-by-step procedure for solving a problem or completing a task.",
        "subject": "Computer Science"
    },

    "what is hardware": {
        "answer": "Hardware means the physical parts of a computer, such as the keyboard, mouse, monitor and processor.",
        "subject": "Computer Science"
    },

    "what is software": {
        "answer": "Software is a set of programs and instructions that tell a computer what to do.",
        "subject": "Computer Science"
    },

    "what is cpu": {
        "answer": "CPU stands for Central Processing Unit. It executes instructions and performs calculations in a computer.",
        "subject": "Computer Science"
    },

    "what is ram": {
        "answer": "RAM stands for Random Access Memory. It temporarily stores data that the computer is currently using.",
        "subject": "Computer Science"
    },

    "what is photosynthesis": {
        "answer": "Photosynthesis is the process by which green plants use sunlight, water and carbon dioxide to make glucose and release oxygen.",
        "subject": "Biology"
    },

    "what is cell": {
        "answer": "A cell is the basic structural and functional unit of life. All living organisms are made of one or more cells.",
        "subject": "Biology"
    },

    "what is nucleus": {
        "answer": "The nucleus is a cell organelle that contains genetic material and helps control cell activities.",
        "subject": "Biology"
    },

    "what is dna": {
        "answer": "DNA stands for Deoxyribonucleic Acid. It carries genetic information in living organisms.",
        "subject": "Biology"
    },

    "what is ecosystem": {
        "answer": "An ecosystem includes living organisms and the non-living environment interacting with one another.",
        "subject": "Biology"
    },

    "what is respiration": {
        "answer": "Respiration is the process by which cells release energy from food molecules.",
        "subject": "Biology"
    },

    "what is atom": {
        "answer": "An atom is the smallest unit of an element that retains the chemical properties of that element.",
        "subject": "Chemistry"
    },

    "what is molecule": {
        "answer": "A molecule consists of two or more atoms chemically bonded together.",
        "subject": "Chemistry"
    },

    "what is element": {
        "answer": "An element is a pure substance made up of atoms that have the same number of protons.",
        "subject": "Chemistry"
    },

    "what is compound": {
        "answer": "A compound is a pure substance formed when two or more different elements chemically combine in fixed proportions.",
        "subject": "Chemistry"
    },

    "what is acid": {
        "answer": "An acid is a substance that donates hydrogen ions in an aqueous solution. Many common acids have a pH below 7.",
        "subject": "Chemistry"
    },

    "what is gravity": {
        "answer": "Gravity is the attractive force between objects that have mass. Earth's gravity pulls objects toward its centre.",
        "subject": "Physics"
    },

    "what is force": {
        "answer": "Force is a push or pull that can change an object's motion or shape. Its SI unit is the newton.",
        "subject": "Physics"
    },

    "what is energy": {
        "answer": "Energy is the capacity to do work or cause change. Common forms include kinetic, potential, thermal and electrical energy.",
        "subject": "Physics"
    },

    "what is speed": {
        "answer": "Speed is the distance travelled per unit of time. Formula: Speed = Distance / Time.",
        "subject": "Physics"
    },

    "what is electricity": {
        "answer": "Electricity involves electric charges and their movement. It is used to power many everyday devices.",
        "subject": "Physics"
    },

    "what is mathematics": {
        "answer": "Mathematics is the study of numbers, quantities, shapes, patterns and logical relationships.",
        "subject": "Mathematics"
    },

    "what is algebra": {
        "answer": "Algebra is a branch of mathematics that uses letters and symbols to represent unknown values.",
        "subject": "Mathematics"
    },

    "what is geometry": {
        "answer": "Geometry is the branch of mathematics that studies points, lines, angles, shapes and space.",
        "subject": "Mathematics"
    },

    "what is percentage": {
        "answer": "A percentage is a number expressed as a fraction of 100. For example, 25% means 25 out of 100.",
        "subject": "Mathematics"
    },

    "what is english": {
        "answer": "English is a language used for communication, education, literature and international exchange.",
        "subject": "English"
    },

    "what is noun": {
        "answer": "A noun is a word used to name a person, place, thing or idea. Examples include teacher, school, book and honesty.",
        "subject": "English"
    },

    "what is verb": {
        "answer": "A verb is a word that expresses an action or a state of being. Examples include run, write, think and is.",
        "subject": "English"
    },

    "what is adjective": {
        "answer": "An adjective describes a noun or pronoun. Examples include beautiful, tall, clever and blue.",
        "subject": "English"
    },

    "what is pakistan": {
        "answer": "Pakistan is a country in South Asia. It became independent on 14 August 1947.",
        "subject": "Pakistan Studies"
    },

    "who founded pakistan": {
        "answer": "Muhammad Ali Jinnah is widely known as the founder of Pakistan and its first Governor-General.",
        "subject": "Pakistan Studies"
    },

    "when pakistan became independent": {
        "answer": "Pakistan became independent on 14 August 1947.",
        "subject": "Pakistan Studies"
    },

    "what is democracy": {
        "answer": "Democracy is a system of government in which people participate in choosing their representatives.",
        "subject": "History"
    },

    "what is geography": {
        "answer": "Geography is the study of Earth, its physical features, people, places and environments.",
        "subject": "Geography"
    },

    "what is history": {
        "answer": "History is the study of past events and human societies using evidence and historical sources.",
        "subject": "History"
    },

    "what is water": {
        "answer": "Water is a substance essential for life. A water molecule contains two hydrogen atoms and one oxygen atom: H2O.",
        "subject": "General Science"
    },

    "what is environment": {
        "answer": "The environment includes the surroundings, conditions and natural systems in which living organisms exist.",
        "subject": "General Science"
    },

    "what is islam": {
        "answer": "Islam is a monotheistic religion. Muslims believe in one God, Allah, and follow the teachings of the Quran and Prophet Muhammad (peace be upon him).",
        "subject": "Islamiat"
    },

    "what is zakat": {
        "answer": "Zakat is an obligatory form of charity in Islam for eligible Muslims who meet the required conditions.",
        "subject": "Islamiat"
    },

    "what is ramadan": {
        "answer": "Ramadan is the ninth month of the Islamic lunar calendar. Muslims who are able observe fasting during this month.",
        "subject": "Islamiat"
    }
}

# ==================================================
# 6. URDU ANSWER TRANSLATIONS
# ==================================================

URDU_ANSWERS = {
    "what is computer":
        "کمپیوٹر ایک الیکٹرانک مشین ہے جو ڈیٹا وصول کرتی ہے، اسے پراسیس کرتی ہے، محفوظ کرتی ہے اور معلومات فراہم کرتی ہے۔",

    "what is ai":
        "مصنوعی ذہانت (AI) کمپیوٹر سائنس کی ایک شاخ ہے جو مشینوں کو مختلف ذہین کام کرنے کے قابل بناتی ہے۔",

    "what is internet":
        "انٹرنیٹ دنیا بھر کے کمپیوٹرز اور آلات کا ایک نیٹ ورک ہے جو معلومات کا تبادلہ کرتا ہے۔",

    "what is photosynthesis":
        "ضیائی تالیف وہ عمل ہے جس میں سبز پودے سورج کی روشنی، پانی اور کاربن ڈائی آکسائیڈ کی مدد سے خوراک بناتے ہیں۔",

    "what is cell":
        "خلیہ زندگی کی بنیادی ساختی اور فعلی اکائی ہے۔ تمام جاندار ایک یا زیادہ خلیوں سے بنے ہوتے ہیں۔",

    "what is gravity":
        "کششِ ثقل وہ قوت ہے جو اجسام کو ایک دوسرے کی طرف کھینچتی ہے۔ زمین کی کشش ہمیں زمین پر رکھتی ہے۔",

    "what is pakistan":
        "پاکستان جنوبی ایشیا کا ایک ملک ہے۔ پاکستان 14 اگست 1947 کو آزاد ہوا۔",

    "what is force":
        "قوت کسی چیز کو دھکا دینے یا کھینچنے کا عمل ہے۔ قوت کی SI اکائی نیوٹن ہے۔",

    "what is water":
        "پانی زندگی کے لیے ضروری ہے۔ اس کا کیمیائی فارمولا H2O ہے۔"
}

# ==================================================
# 7. CHATBOT ENGINE
# ==================================================

def chatbot(question, subject, language, student_class):
    q = question.lower().strip()

    if not q:
        return "Please enter a question."

    greetings = ["hello", "hi", "hey", "salam", "assalamualaikum"]

    if q in greetings:
        if language == "Urdu":
            return "السلام علیکم! میں آپ کا School AI Assistant ہوں۔ اپنا سوال پوچھیں۔"

        if language == "Roman Urdu":
            return "Assalamualaikum! Main aap ka School AI Assistant hoon. Apna sawal poochain."

        return "Hello! Welcome to Muhammad Abdullah School AI. What would you like to learn today?"

    # Search exact and partial question matches
    for key, item in KNOWLEDGE.items():
        if q == key or key in q:
            if language == "Urdu":
                return URDU_ANSWERS.get(key, item["answer"])

            if language == "Roman Urdu":
                return "Jawab: " + item["answer"]

            return (
                f"**Answer:** {item['answer']}\n\n"
                f"**Subject:** {item['subject']}\n"
                f"**Class:** {student_class}"
            )

    # Simple maths detection
    math_words = ["calculate", "solve", "plus", "minus", "multiply"]

    if any(word in q for word in math_words):
        return (
            "I can help with basic calculations. "
            "Open the Calculator section and enter a mathematical expression."
        )

    # Subject-based fallback
    if language == "Urdu":
        return (
            f"آپ کا سوال {subject} کے بارے میں موصول ہوا ہے۔ "
            "اس آف لائن ڈیمو میں اس سوال کا تیار شدہ جواب موجود نہیں۔ "
            "براہ کرم سوال کو آسان الفاظ میں لکھیں۔"
        )

    if language == "Roman Urdu":
        return (
            f"Aap ka sawal {subject} ke bare mein hai. "
            "Is offline demo mein is sawal ka jawab mojood nahi. "
            "Meherbani karke sawal asaan alfaaz mein likhein."
        )

    return (
        f"I received your question about **{subject}** for **{student_class}**.\n\n"
        "I do not have a prepared answer for this question in my offline "
        "knowledge base yet. Try using different words or choose a related "
        "topic from the subject."
    )

# ==================================================
# 8. SAFE CALCULATOR
# ==================================================

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod
}

def safe_calculate(expression):

    def evaluate(node):

        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value

        if isinstance(node, ast.BinOp):
            if type(node.op) not in OPERATORS:
                raise ValueError("Unsupported operation")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent too large")

            result = OPERATORS[type(node.op)](left, right)

            if abs(result) > 10**12:
                raise ValueError("Result too large")

            return result

        if isinstance(node, ast.UnaryOp):
            if type(node.op) not in OPERATORS:
                raise ValueError("Unsupported operation")

            return OPERATORS[type(node.op)](evaluate(node.operand))

        raise ValueError("Invalid expression")

    return evaluate(ast.parse(expression, mode="eval"))

# ==================================================
# 9. LOGIN SCREEN
# ==================================================

def login_screen():

    st.markdown(
        '<div class="main-title">🎓 Muhammad Abdullah School AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Your Professional Learning Assistant</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    left, center, right = st.columns([1, 1.3, 1])

    with center:

        st.markdown('<div class="panel">', unsafe_allow_html=True)

        st.subheader("🔐 Secure Login")
        st.write("Enter your password to continue.")

        password = st.text_input(
            "School AI Password",
            type="password",
            placeholder="Enter password"
        )

        if st.button("🚀 Open School AI", use_container_width=True):

            if password == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")

        st.markdown('</div>', unsafe_allow_html=True)

        st.caption("© Muhammad Abdullah School AI")

# ==================================================
# 10. HOME DASHBOARD
# ==================================================

def home_page():

    st.markdown(
        '<div class="main-title">Welcome to School AI 🎓</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Learn Smarter • Study Better • Achieve More</div>',
        unsafe_allow_html=True
    )

    st.write("")

    a, b, c = st.columns(3)

    a.metric("Classes", "1–10")
    b.metric("Subjects", len(SUBJECTS))
    c.metric("Knowledge Topics", len(KNOWLEDGE))

    st.divider()

    st.subheader("🚀 Learning Tools")

    columns = st.columns(3)

    cards = [
        ("🤖 AI Chatbot", "Ask educational questions."),
        ("🧮 Calculator", "Solve basic maths problems."),
        ("📝 Notes", "Write and save study notes."),
        ("🧠 Quiz", "Test your knowledge."),
        ("📅 Study Planner", "Organize your study tasks."),
        ("📚 Knowledge Base", "Explore prepared questions.")
    ]

    for i, (title, description) in enumerate(cards):
        with columns[i % 3]:
            st.markdown(
                f"""
                <div class="panel">
                <h3>{title}</h3>
                <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.info(
        "This is an offline educational demo. "
        "Its answers come from the built-in knowledge base."
    )

# ==================================================
# 11. CHATBOT PAGE
# ==================================================

def chatbot_page():

    st.title("🤖 School AI Chatbot")

    st.session_state.student_class = st.selectbox(
        "Select Class",
        CLASSES,
        index=CLASSES.index(st.session_state.student_class)
    )

    st.session_state.subject = st.selectbox(
        "Select Subject",
        SUBJECTS,
        index=SUBJECTS.index(st.session_state.subject)
    )

    st.session_state.language = st.selectbox(
        "Answer Language",
        ["Simple English", "Urdu", "Roman Urdu"],
        index=["Simple English", "Urdu", "Roman Urdu"].index(
            st.session_state.language
        )
    )

    st.divider()

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask your educational question...")

    if question:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        answer = chatbot(
            question,
            st.session_state.subject,
            st.session_state.language,
            st.session_state.student_class
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# ==================================================
# 12. CALCULATOR PAGE
# ==================================================

def calculator_page():

    st.title("🧮 Smart Calculator")

    expression = st.text_input(
        "Enter mathematical expression",
        placeholder="Example: (25 + 15) * 2"
    )

    if st.button("Calculate"):

        try:
            result = safe_calculate(expression)
            st.success(f"Answer: {result}")

        except Exception:
            st.error("Invalid calculation. Check your expression.")

    st.markdown("### Examples")
    st.code("25 + 15")
    st.code("100 / 5")
    st.code("(10 + 5) * 3")
    st.code("2 ** 4")

# ==================================================
# 13. NOTES PAGE
# ==================================================

def notes_page():

    st.title("📝 Study Notes Manager")

    notes = load_json(NOTES_FILE, [])

    title = st.text_input("Note Title")
    subject = st.selectbox("Note Subject", SUBJECTS)
    content = st.text_area("Write Your Notes", height=180)

    if st.button("💾 Save Note"):

        if title.strip() and content.strip():

            notes.append({
                "title": title.strip(),
                "subject": subject,
                "content": content.strip(),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

            save_json(NOTES_FILE, notes)

            st.success("Your note has been saved.")
            st.rerun()

        else:
            st.warning("Please enter a title and note.")

    st.divider()
    st.subheader("Saved Notes")

    if not notes:
        st.info("No notes saved yet.")

    for index, note in enumerate(notes):

        with st.expander(note["title"]):

            st.caption(
                f"{note['subject']} • {note['date']}"
            )

            st.write(note["content"])

            if st.button("Delete Note", key=f"note_{index}"):

                notes.pop(index)
                save_json(NOTES_FILE, notes)
                st.rerun()

# ==================================================
# 14. QUIZ PAGE
# ==================================================

QUIZ = [
    {
        "question": "What is the chemical formula of water?",
        "options": ["CO2", "H2O", "O2", "NaCl"],
        "answer": "H2O",
        "explanation": "Water contains two hydrogen atoms and one oxygen atom."
    },
    {
        "question": "What is the capital of Pakistan?",
        "options": ["Lahore", "Karachi", "Islamabad", "Quetta"],
        "answer": "Islamabad",
        "explanation": "Islamabad is the capital city of Pakistan."
    },
    {
        "question": "What does CPU stand for?",
        "options": [
            "Central Processing Unit",
            "Computer Power Utility",
            "Central Program User",
            "Control Processing User"
        ],
        "answer": "Central Processing Unit",
        "explanation": "CPU stands for Central Processing Unit."
    },
    {
        "question": "What is 12 × 8?",
        "options": ["86", "96", "108", "88"],
        "answer": "96",
        "explanation": "12 multiplied by 8 equals 96."
    },
    {
        "question": "Which organelle contains genetic material?",
        "options": ["Nucleus", "Ribosome", "Cell wall", "Vacuole"],
        "answer": "Nucleus",
        "explanation": "The nucleus contains most of the cell's genetic material."
    },
    {
        "question": "Which force pulls objects toward Earth?",
        "options": ["Friction", "Gravity", "Magnetism", "Tension"],
        "answer": "Gravity",
        "explanation": "Gravity attracts objects toward Earth's centre."
    },
    {
        "question": "Who is known as the founder of Pakistan?",
        "options": [
            "Allama Iqbal",
            "Liaquat Ali Khan",
            "Muhammad Ali Jinnah",
            "Sir Syed Ahmad Khan"
        ],
        "answer": "Muhammad Ali Jinnah",
        "explanation": "Muhammad Ali Jinnah is widely known as the founder of Pakistan."
    }
]

def quiz_page():

    st.title("🧠 Knowledge Quiz")

    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = random.sample(
            QUIZ, len(QUIZ)
        )

    questions = st.session_state.quiz_questions

    with st.form("quiz_form"):

        answers = []

        for i, item in enumerate(questions):

            st.markdown(f"**Q{i + 1}. {item['question']}**")

            selected = st.radio(
                "Choose an answer:",
                item["options"],
                key=f"quiz_answer_{i}",
                index=None
            )

            answers.append(selected)
            st.divider()

        submitted = st.form_submit_button("Submit Quiz")

    if submitted:

        score = 0

        for i, item in enumerate(questions):

            if answers[i] == item["answer"]:
                score += 1
                st.success(f"Q{i + 1}: Correct!")
            else:
                st.error(
                    f"Q{i + 1}: Correct answer: {item['answer']}"
                )

            st.caption(item["explanation"])

        st.metric("Your Score", f"{score} / {len(questions)}")

    if st.button("🔄 New Quiz"):
        st.session_state.quiz_questions = random.sample(
            QUIZ, len(QUIZ)
        )
        st.rerun()

# ==================================================
# 15. STUDY PLANNER
# ==================================================

def planner_page():

    st.title("📅 Study Planner")

    tasks = load_json(PLANNER_FILE, [])

    task_name = st.text_input("Study Task")
    task_subject = st.selectbox(
        "Task Subject",
        SUBJECTS,
        key="planner_subject"
    )
    task_date = st.date_input("Study Date", date.today())

    if st.button("Add Study Task"):

        if task_name.strip():

            tasks.append({
                "task": task_name.strip(),
                "subject": task_subject,
                "date": str(task_date),
                "completed": False
            })

            save_json(PLANNER_FILE, tasks)
            st.success("Study task added.")
            st.rerun()

        else:
            st.warning("Enter a task name.")

    st.divider()
    st.subheader("Your Study Tasks")

    if not tasks:
        st.info("No study tasks yet.")

    for i, task in enumerate(tasks):

        st.write(
            f"**{task['task']}** — {task['subject']} — {task['date']}"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Complete", key=f"complete_{i}"):
                tasks.pop(i)
                save_json(PLANNER_FILE, tasks)
                st.rerun()

        with col2:
            if st.button("Delete", key=f"delete_{i}"):
                tasks.pop(i)
                save_json(PLANNER_FILE, tasks)
                st.rerun()

        st.divider()

# ==================================================
# 16. KNOWLEDGE BASE PAGE
# ==================================================

def knowledge_page():

    st.title("📚 School Knowledge Base")

    search = st.text_input("Search a question or topic")

    for question, item in KNOWLEDGE.items():

        if search.lower() in question or not search:

            with st.expander(question.title()):

                st.write(item["answer"])
                st.caption(f"Subject: {item['subject']}")

# ==================================================
# 17. ABOUT PAGE
# ==================================================

def about_page():

    st.title("ℹ️ About This Project")

    st.markdown(f"""
    ## 🎓 {APP_NAME}

    A professional offline educational demo.

    **Features:**
    - Password protected entry
    - Class 1 to Class 10
    - 14 school subjects
    - Educational chatbot
    - English, Urdu and Roman Urdu
    - Study notes
    - Calculator
    - Knowledge quiz
    - Study planner
    - Built-in question database

    **Version:** 1.0

    **Developer:** Muhammad Abdullah
    """)

    st.warning(
        "This app uses prepared offline answers. "
        "It is not a generative AI model and cannot answer every new question."
    )

# ==================================================
# 18. MAIN APPLICATION
# ==================================================

def main_app():

    st.sidebar.title("🎓 School AI")
    st.sidebar.caption("Professional Learning Dashboard")

    st.sidebar.success("Welcome, Muhammad Abdullah")

    page = st.sidebar.radio(
        "MAIN MENU",
        [
            "🏠 Home",
            "🤖 AI Chatbot",
            "🧮 Calculator",
            "📝 Study Notes",
            "🧠 Quiz",
            "📅 Study Planner",
            "📚 Knowledge Base",
            "ℹ️ About"
        ]
    )

    st.sidebar.divider()

    st.sidebar.write("**Student Settings**")

    st.sidebar.selectbox(
        "Class",
        CLASSES,
        key="sidebar_class"
    )

    st.sidebar.caption("Muhammad Abdullah School AI")

    if st.sidebar.button("🚪 Logout", use_container_width=True):

        st.session_state.authenticated = False
        st.session_state.messages = []
        st.rerun()

    if page == "🏠 Home":
        home_page()

    elif page == "🤖 AI Chatbot":
        chatbot_page()

    elif page == "🧮 Calculator":
        calculator_page()

    elif page == "📝 Study Notes":
        notes_page()

    elif page == "🧠 Quiz":
        quiz_page()

    elif page == "📅 Study Planner":
        planner_page()

    elif page == "📚 Knowledge Base":
        knowledge_page()

    elif page == "ℹ️ About":
        about_page()

# ==================================================
# 19. START APPLICATION
# ==================================================

if st.session_state.authenticated:
    main_app()
else:
    login_screen()
