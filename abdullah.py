```python
import streamlit as st
from openai import OpenAI
import re

# ============================================================
# SCHOOL AI EDUCATIONAL CHATBOT
# Classes 1–10 | Urdu + English | Major School Subjects
# ============================================================

# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------
st.set_page_config(
    page_title="School AI Educational Chatbot",
    page_icon="🎓",
    layout="wide"
)

# ------------------------------------------------------------
# CUSTOM DESIGN
# ------------------------------------------------------------
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: gray;
        margin-bottom: 30px;
    }

    .footer {
        text-align: center;
        color: gray;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------
st.markdown(
    "<div class='main-title'>🎓 School AI Educational Chatbot</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='subtitle'>
    Your Smart Learning Assistant 🤖📚<br>
    Classes 1 to 10 | Urdu & English | Major School Subjects
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# API SETUP
# ============================================================

try:
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )
except Exception:
    client = None


# ============================================================
# SIDEBAR SETTINGS
# ============================================================

with st.sidebar:

    st.title("⚙️ Student Settings")

    student_class = st.selectbox(
        "🎓 Select Your Class",
        [f"Class {i}" for i in range(1, 11)]
    )

    subjects = [
        "General / All Subjects",
        "English",
        "Urdu",
        "Mathematics",
        "General Science",
        "Physics",
        "Chemistry",
        "Biology",
        "Computer Science",
        "Information Technology",
        "Islamiat",
        "Pakistan Studies",
        "Social Studies",
        "General Knowledge"
    ]

    selected_subject = st.selectbox(
        "📚 Select Subject",
        subjects
    )

    st.divider()

    st.subheader("🤖 Chatbot Features")

    st.write("✅ Classes 1–10")
    st.write("✅ Urdu & English")
    st.write("✅ Major School Subjects")
    st.write("✅ Homework Help")
    st.write("✅ Step-by-Step Learning")
    st.write("✅ AI Powered Answers")

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# RESPECTFUL LANGUAGE HANDLING
# ============================================================

def is_inappropriate(text):

    # اپنی school policy کے مطابق مزید keywords شامل کیے جا سکتے ہیں
    blocked_patterns = [
        r"\b(abuseword1)\b",
        r"\b(abuseword2)\b"
    ]

    text_lower = text.lower()

    for pattern in blocked_patterns:
        if re.search(pattern, text_lower):
            return True

    return False


# ============================================================
# BASIC URDU + ENGLISH CONVERSATION
# ============================================================

def basic_chat_response(user_message):

    message = user_message.lower().strip()

    # ENGLISH GREETINGS
    if message in ["hello", "hi", "hey", "hello chatbot"]:
        return (
            "Hello! 😊 How are you? "
            "I am your School AI Educational Assistant. "
            "How can I help you today?"
        )

    # URDU GREETINGS
    elif "السلام علیکم" in user_message:
        return (
            "وعلیکم السلام! 😊 "
            "آپ کیسے ہیں؟ میں آپ کی پڑھائی میں کیسے مدد کر سکتا ہوں؟"
        )

    # HOW ARE YOU
    elif "how are you" in message:
        return (
            "I am doing great! 😊 "
            "Thank you for asking. How can I help you with your studies?"
        )

    elif "کیسے ہو" in user_message or "کیا حال ہے" in user_message:
        return (
            "میں بالکل ٹھیک ہوں 😊 "
            "آپ سنائیں! میں آپ کی پڑھائی میں کیسے مدد کر سکتا ہوں؟"
        )

    # NAME
    elif "your name" in message:
        return (
            "My name is School AI Educational Chatbot 🤖📚 "
            "I am here to help students learn and understand their subjects."
        )

    elif "آپ کا نام" in user_message or "تمہارا نام" in user_message:
        return (
            "میرا نام School AI Educational Chatbot ہے 🤖📚 "
            "میں آپ کی تعلیم اور پڑھائی میں مدد کے لیے موجود ہوں۔"
        )

    # HELP
    elif "help" == message or "can you help me" in message:
        return (
            "Of course! 😊 I can help you with school subjects, "
            "homework, concepts, mathematics, science, English and more."
        )

    elif "مدد" == user_message.strip():
        return (
            "ضرور! 😊 میں آپ کی پڑھائی، ہوم ورک "
            "اور مختلف مضامین کے سوالات میں مدد کر سکتا ہوں۔"
        )

    # THANK YOU
    elif "thank you" in message or "thanks" in message:
        return (
            "You're welcome! 😊 "
            "I am always happy to help you learn."
        )

    elif "شکریہ" in user_message:
        return (
            "آپ کا بہت شکریہ! 😊 "
            "مجھے خوشی ہے کہ میں آپ کی مدد کر سکا۔"
        )

    # GOODBYE
    elif message in ["bye", "goodbye"]:
        return (
            "Goodbye! 😊 Keep learning and have a great day! 📚✨"
        )

    elif "اللہ حافظ" in user_message:
        return (
            "اللہ حافظ! 😊 "
            "اپنی پڑھائی جاری رکھیں اور ہمیشہ کامیاب رہیں۔ 📚✨"
        )

    return None


# ============================================================
# AI SYSTEM PROMPT
# ============================================================

def get_system_prompt(student_class, subject):

    return f"""
You are a professional School AI Educational Assistant.

Student Class: {student_class}
Selected Subject: {subject}

Your purpose is to help school students learn safely and clearly.

IMPORTANT RULES:

1. Explain according to the student's class level.
2. Use simple and easy language.
3. If the student writes in Urdu, reply mainly in Urdu.
4. If the student writes in English, reply mainly in English.
5. Help with homework and educational concepts.
6. For Mathematics, explain the solution step by step.
7. For Science subjects, explain concepts clearly.
8. For English, help with grammar, writing and comprehension.
9. For Urdu, help with grammar, writing and explanations.
10. For Computer Science and IT, explain concepts clearly and provide safe code examples.
11. Be respectful, friendly and encouraging.
12. Never insult or shame the student.
13. If you are unsure about a fact, say so clearly.
14. Do not invent facts or sources.
15. Encourage students to understand concepts instead of only copying answers.
16. Keep answers suitable for school students.

Supported educational areas include:

- English
- Urdu
- Mathematics
- General Science
- Physics
- Chemistry
- Biology
- Computer Science
- Information Technology
- Islamiat
- Pakistan Studies
- Social Studies
- General Knowledge

Always try to give clear, useful and educational answers.
"""


# ============================================================
# DISPLAY PREVIOUS CHAT
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================================
# USER INPUT
# ============================================================

user_prompt = st.chat_input(
    "Ask your question in Urdu or English..."
)


# ============================================================
# PROCESS USER MESSAGE
# ============================================================

if user_prompt:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)


    # --------------------------------------------------------
    # ASSISTANT RESPONSE
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        # Check respectful language
        if is_inappropriate(user_prompt):

            bot_response = """
⚠️ **Please use respectful language.**

This chatbot is designed to help students with:

📚 Education  
📝 Homework  
🔬 School Subjects  
🧠 Learning Concepts  

Please ask your question politely. 😊
"""

            st.markdown(bot_response)


        else:

            # Check basic conversation first
            basic_response = basic_chat_response(user_prompt)

            if basic_response:

                bot_response = basic_response
                st.markdown(bot_response)


            # ------------------------------------------------
            # AI RESPONSE
            # ------------------------------------------------

            else:

                if client is None:

                    bot_response = """
⚠️ **AI API Key Not Connected**

The chatbot design is working, but the AI brain needs an API key.

Please add your API key in:

`.streamlit/secrets.toml`
"""

                    st.markdown(bot_response)

                else:

                    try:

                        messages = [
                            {
                                "role": "system",
                                "content": get_system_prompt(
                                    student_class,
                                    selected_subject
                                )
                            }
                        ]

                        # Add previous conversation
                        for message in st.session_state.messages:

                            messages.append({
                                "role": message["role"],
                                "content": message["content"]
                            })


                        with st.spinner("🤖 Thinking..."):

                            response = client.chat.completions.create(
                                model="gpt-4.1-mini",
                                messages=messages
                            )


                        bot_response = (
                            response.choices[0]
                            .message.content
                        )

                        st.markdown(bot_response)


                    except Exception:

                        bot_response = """
⚠️ **Connection Error**

The chatbot could not connect to the AI service.

Please check:

1. Your API Key
2. Internet Connection
3. Streamlit Secrets Configuration
4. OpenAI Account/API Access
"""

                        st.markdown(bot_response)


        # ----------------------------------------------------
        # SAVE ASSISTANT MESSAGE
        # ----------------------------------------------------

        st.session_state.messages.append({
            "role": "assistant",
            "content": bot_response
        })


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class='footer'>
    🎓 School AI Educational Chatbot<br>
    Smart Learning Assistant for Classes 1–10 🤖📚
    </div>
    """,
    unsafe_allow_html=True
)
```