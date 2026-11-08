import streamlit as st
import re

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="School AI Educational Chatbot",
    page_icon="🎓",
    layout="wide"
)


# =====================================================
# CUSTOM CSS
# =====================================================

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
    color: #666;
    margin-bottom: 30px;
}

.info-box {
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# HEADER
# =====================================================

st.markdown(
    "<div class='main-title'>🎓 School AI Educational Chatbot</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Your Smart Learning Assistant | Classes 1 to 10 | All Major Subjects</div>",
    unsafe_allow_html=True
)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("⚙️ Student Settings")

    student_class = st.selectbox(
        "🎓 Select Your Class",
        [
            "Class 1",
            "Class 2",
            "Class 3",
            "Class 4",
            "Class 5",
            "Class 6",
            "Class 7",
            "Class 8",
            "Class 9",
            "Class 10"
        ]
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

    st.write("### 🤖 Chatbot Features")

    st.write("""
    ✅ Classes 1–10  
    ✅ Multiple Subjects  
    ✅ Urdu & English Support  
    ✅ Homework Help  
    ✅ Concept Explanation  
    ✅ Chat History  
    """)

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =====================================================
# BASIC LANGUAGE / BAD WORD FILTER
# =====================================================

def contains_inappropriate_language(text):

    # یہاں آپ اپنی ضرورت کے مطابق inappropriate words شامل کر سکتے ہیں
    blocked_words = [
        # جان بوجھ کر یہاں گالیوں کی فہرست شامل نہیں کی گئی
    ]

    text_lower = text.lower()

    for word in blocked_words:

        if word in text_lower:

            return True

    return False


# =====================================================
# EDUCATIONAL RESPONSE FUNCTION
# =====================================================

def generate_educational_response(question, student_class, subject):

    response = f"""
## 📚 Educational Assistant

**Class:** {student_class}  
**Subject:** {subject}

### ❓ Your Question:
{question}

---

🤖 **Educational Response:**

I am ready to help you understand this topic step by step.

Please note that this chatbot should be connected to an AI model
to generate accurate answers for every educational question.

You can ask me about:

- 📖 English
- 🇵🇰 Urdu
- ➗ Mathematics
- 🔬 Science
- ⚛️ Physics
- ⚗️ Chemistry
- 🧬 Biology
- 💻 Computer Science
- 🕌 Islamiat
- 🇵🇰 Pakistan Studies

I will explain concepts according to your selected class level.
"""

    return response


# =====================================================
# DISPLAY CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =====================================================
# CHAT INPUT
# =====================================================

user_prompt = st.chat_input(
    "Ask any educational question in Urdu or English..."
)


# =====================================================
# PROCESS USER QUESTION
# =====================================================

if user_prompt:

    # -----------------------------------------
    # DISPLAY USER MESSAGE
    # -----------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(user_prompt)


    # -----------------------------------------
    # DISPLAY BOT RESPONSE
    # -----------------------------------------

    with st.chat_message("assistant"):

        # CHECK INAPPROPRIATE LANGUAGE

        if contains_inappropriate_language(user_prompt):

            bot_response = """
### ⚠️ Educational Chatbot Notice

Please use respectful and appropriate language.

🤝 This chatbot is designed to help students with:

- Education
- Homework
- School Subjects
- Learning Concepts

Please ask your educational question politely. 😊
"""

        else:

            bot_response = generate_educational_response(
                user_prompt,
                student_class,
                selected_subject
            )

        st.markdown(bot_response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": bot_response
            }
        )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "🎓 School AI Educational Chatbot | Classes 1–10 | Smart Learning Assistant"
)
