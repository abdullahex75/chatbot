import streamlit as st

# صفحہ کی سیٹنگ
st.set_page_config(
    page_title="School Educational Chatbot",
    page_icon="🤖",
    layout="centered"
)

# سٹائلنگ اور ڈیزائن
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        color: #2b580c;
        font-size: 32px;
        font-weight: bold;
    }
    .sub-title {
        text-align: center;
        color: #555555;
        font-size: 16px;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="main-title">📚 School AI Educational Chatbot</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-title">Classes 1 to 10 | Urdu, English, Science, & Islamiat</p>',
    unsafe_allow_html=True,
)

# سائیڈ بار میں طالب علم کی معلومات
st.sidebar.header("🎓 Student Settings")
student_class = st.sidebar.selectbox(
    "Select Your Class:",
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
        "Class 10",
    ],
)
selected_subject = st.sidebar.selectbox(
    "Select Subject:", ["General / All Subjects", "Urdu", "Science", "Islamiat", "English"]
)

# چیট ہسٹری کو محفوظ کرنا
if "messages" not in st.session_state:
    st.session_state.messages = []

# پرانی چٹس کو سکرین پر دکھانا
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# یوزر کا ان پٹ لینا
user_prompt = st.chat_input(
    "Ask your question here (اردو یا English میں سوال پوچھیں)..."
)

if user_prompt:
    # یوزر کا پیغام شامل کریں
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # بوٹ کا جواب تیار کرنا (یہاں آپ اپنی ضرورت کے مطابق اے آئی ماڈل یا منطق جوڑ سکتے ہیں)
    with st.chat_message("assistant"):
        if (
            "urdu" in selected_subject.lower()
            or "اردو" in user_prompt
            or any("\u0600" <= c <= "\u06FF" for c in user_prompt)
        ):
            bot_response = f"وعلیکم السلام! آپ نے **{student_class}** کے مضمون **{selected_subject}** کے حوالے سے پوچھا ہے۔ آپ کے اس سوال کا بہترین اور آسان جواب یہ ہے کہ: \n\n (یہاں آپ کا تعلیمی جواب ظاہر ہوگا، آپ اس کوڈ کو کسی بھی AI API سے لنک کر سکتے ہیں)۔"
        else:
            bot_response = f"Hello! I am your AI tutor for **{student_class}** in **{selected_subject}**. I'd be happy to help you with your homework and concepts. Here is the explanation for your query: '{user_prompt}'."

        st.markdown(bot_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": bot_response}
        )
