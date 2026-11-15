
import streamlit as st
import time

st.set_page_config(
    page_title="Muhammad Abdullah School AI",
    page_icon="🎓",
    layout="wide"
)

# ==========================================
# SETTINGS
# ==========================================

APP_PASSWORD = "Muhammad Abdullah"

FREE_MESSAGE_LIMIT = 10

WEEKLY_PRICE = 200
MONTHLY_PRICE = 500

# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "logged_in": False,
    "message_count": 0,
    "premium_until": 0,
    "chat_history": [],
    "selected_class": "Class 10",
    "selected_subject": "General Knowledge"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================================
# PROFESSIONAL DESIGN
# ==========================================

st.markdown("""
<style>

.stApp {
    background:
    radial-gradient(circle at top left, #26365F, transparent 35%),
    linear-gradient(135deg, #080D1B, #111A33, #211438);
    color: white;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}

h1, h2, h3, p, label {
    color: white;
}

.brand {
    text-align: center;
    padding: 20px 5px;
}

.brand h1 {
    font-size: clamp(28px, 5vw, 43px);
    font-weight: 800;
}

.brand p {
    color: #B9C5E0;
}

.plan-card {
    background: #202B43;
    border: 1px solid #465675;
    border-radius: 18px;
    padding: 22px;
    min-height: 220px;
    margin-bottom: 12px;
}

.featured {
    border: 2px solid #917BFF;
    background: linear-gradient(145deg, #302755, #202B43);
}

.price {
    font-size: 34px;
    font-weight: 800;
    color: #AA98FF;
    margin: 12px 0;
}

.small-text {
    color: #C0CAE0;
    font-size: 14px;
}

.stButton button {
    width: 100%;
    min-height: 45px;
    border-radius: 12px;
    background: linear-gradient(90deg, #6554D9, #9279F5);
    color: white;
    border: none;
    font-weight: bold;
}

.stButton button:hover {
    color: white;
    border: 1px solid white;
}

.footer {
    text-align: center;
    color: #8492B3;
    padding: 25px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# PASSWORD LOGIN
# ==========================================

def login_page():

    st.markdown("""
    <div class="brand">
        <div style="font-size:55px">🎓</div>
        <h1>Muhammad Abdullah School AI</h1>
        <p>Your Smart Educational Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):

        st.subheader("🔐 Secure Login")

        password = st.text_input(
            "Enter School AI Password",
            type="password"
        )

        if st.button("Login to School AI"):

            if password == APP_PASSWORD:
                st.session_state.logged_in = True
                st.rerun()

            else:
                st.error("Incorrect password. Please try again.")

        st.caption("Welcome to Muhammad Abdullah School AI")


# ==========================================
# SUBSCRIPTION / UPGRADE SCREEN
# ==========================================

def upgrade_screen():

    st.markdown("""
    <div class="brand">
        <div style="font-size:55px">🎓</div>
        <h1>Muhammad Abdullah School AI</h1>
        <p>Your Smart Learning Partner</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("## ⏳ You've reached your free usage limit")

    st.write(
        "You've used all your free messages. "
        "Choose a plan to continue chatting."
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:

        st.markdown("""
        <div class="plan-card">
            <h3>📅 Weekly Plan</h3>
            <div class="price">Rs. 200</div>
            <div class="small-text">
                ✓ 7 Days Access<br><br>
                ✓ School AI Chatbot<br><br>
                ✓ Educational Support
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Choose Weekly Plan - Rs. 200"):

            st.session_state.selected_plan = "weekly"

            st.info(
                "Weekly plan selected. "
                "Payment gateway is not connected yet."
            )

    with col2:

        st.markdown("""
        <div class="plan-card featured">
            <div style="color:#B6A5FF;font-weight:bold">
                ⭐ POPULAR PLAN
            </div>
            <h3>Monthly Plan</h3>
            <div class="price">Rs. 500</div>
            <div class="small-text">
                ✓ 30 Days Access<br><br>
                ✓ School AI Chatbot<br><br>
                ✓ Educational Support
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Choose Monthly Plan - Rs. 500"):

            st.session_state.selected_plan = "monthly"

            st.info(
                "Monthly plan selected. "
                "Payment gateway is not connected yet."
            )

    st.info(
        "🔒 Premium activation requires verified payment."
    )

    st.markdown(
        '<div class="footer">© 2026 Muhammad Abdullah School AI</div>',
        unsafe_allow_html=True
    )


# ==========================================
# OFFLINE SCHOOL KNOWLEDGE BASE
# ==========================================

knowledge = {

    "General Knowledge": {
        "what is computer":
            "A computer is an electronic machine that processes data.",

        "what is pakistan":
            "Pakistan is a country in South Asia. Its capital is Islamabad.",

        "who is the founder of pakistan":
            "Quaid-e-Azam Muhammad Ali Jinnah is the founder of Pakistan.",

        "what is science":
            "Science is the systematic study of the natural world.",

        "what is education":
            "Education is the process of gaining knowledge and skills."
    },

    "Mathematics": {
        "what is mathematics":
            "Mathematics is the study of numbers, shapes and patterns.",

        "what is addition":
            "Addition means combining two or more numbers.",

        "what is subtraction":
            "Subtraction means taking one number away from another.",

        "what is multiplication":
            "Multiplication is repeated addition.",

        "what is division":
            "Division means sharing a quantity into equal parts."
    },

    "English": {
        "what is noun":
            "A noun is the name of a person, place, animal or thing.",

        "what is verb":
            "A verb is an action or state word.",

        "what is adjective":
            "An adjective describes a noun.",

        "what is sentence":
            "A sentence is a group of words expressing a complete idea."
    },

    "Computer Science": {
        "what is internet":
            "The internet is a global network connecting computers.",

        "what is website":
            "A website is a collection of related web pages.",

        "what is python":
            "Python is a popular programming language.",

        "what is software":
            "Software is a set of instructions used by a computer."
    },

    "Biology": {
        "what is cell":
            "The cell is the basic structural and functional unit of life.",

        "what is photosynthesis":
            "Photosynthesis is the process by which green plants make food using sunlight.",

        "what is heart":
            "The heart is an organ that pumps blood around the body."
    },

    "Physics": {
        "what is force":
            "Force is a push or pull that can change an object's motion.",

        "what is energy":
            "Energy is the ability to do work.",

        "what is gravity":
            "Gravity is the force of attraction between objects with mass."
    },

    "Chemistry": {
        "what is atom":
            "An atom is the basic unit of an element.",

        "what is water":
            "Water is a chemical compound with the formula H2O.",

        "what is element":
            "An element is a pure substance made of one type of atom."
    }
}


def get_answer(question, subject):

    q = question.lower().strip()

    if subject in knowledge:

        for key, answer in knowledge[subject].items():

            if key in q or q in key:
                return answer

    for subject_data in knowledge.values():

        for key, answer in subject_data.items():

            if key in q or q in key:
                return answer

    return (
        "I don't have this answer in my offline knowledge base yet. "
        "Please try another question or ask your teacher."
    )


# ==========================================
# SCHOOL AI CHATBOT
# ==========================================

def school_ai():

    st.markdown("""
    <div class="brand">
        <h1>🎓 Muhammad Abdullah School AI</h1>
        <p>Smart Education • Smart Learning • Smart Future</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:

        st.title("🎓 School AI")

        st.write("Student Dashboard")

        st.selectbox(
            "Select Class",
            [f"Class {i}" for i in range(1, 11)],
            key="selected_class"
        )

        st.selectbox(
            "Select Subject",
            list(knowledge.keys()),
            key="selected_subject"
        )

        st.divider()

        st.write("📊 Account Usage")

        if not st.session_state.premium_until:
            remaining = max(
                0,
                FREE_MESSAGE_LIMIT - st.session_state.message_count
            )

            st.progress(
                min(1.0, remaining / FREE_MESSAGE_LIMIT)
            )

            st.caption(
                f"{remaining} free messages remaining"
            )
        else:
            st.success("Premium Account")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    st.subheader("💬 AI School Assistant")

    st.caption(
        f"{st.session_state.selected_class} | "
        f"{st.session_state.selected_subject}"
    )

    # Chat history
    for msg in st.session_state.chat_history:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input("Ask your school question...")

    if question:

        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        answer = get_answer(
            question,
            st.session_state.selected_subject
        )

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

        if not st.session_state.premium_until:
            st.session_state.message_count += 1

        st.rerun()

    st.divider()

    st.caption(
        "Muhammad Abdullah School AI | Offline Educational Demo"
    )


# ==========================================
# MAIN APP CONTROL
# ==========================================

if not st.session_state.logged_in:

    login_page()

elif (
    st.session_state.premium_until > time.time()
):

    school_ai()

elif (
    st.session_state.message_count >= FREE_MESSAGE_LIMIT
):

    upgrade_screen()

else:

    school_ai()
