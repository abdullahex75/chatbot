
Student question:
{question}

Teaching rules:
- Use age-appropriate language and explain difficult words simply.
- Stay suitable for a school student in {grade}.
- Teach the method, not just the final answer.
- For maths, show clear steps and check the result.
- For science, explain the idea and give a familiar example.
- For language subjects, explain grammar, vocabulary or writing clearly.
- For Islamiyat and Pakistan Studies, be respectful and distinguish facts from opinions.
- If the request is a quiz, create 5 questions and put answers in a separate answer key.
- Never pretend to know the student's textbook page or syllabus if it was not provided.
- If the question is unclear, ask one short clarifying question.
- Do not invent facts. If unsure, say so.
- Be encouraging, concise and helpful.
"""

def offline_answer(question: str) -> str:
    """Basic sample help when no AI key has been configured."""
    q = question.lower()
    if any(greeting in q for greeting in ["hello", "hi", "salam", "assalam"]):
        return "Hello! 👋 Welcome to Muhammad Abdullah School AI. Ask me a question from any school subject."
    if "photosynthesis" in q:
        return (
            "**Photosynthesis** is how green plants make their food. Plants use sunlight, "
            "water and carbon dioxide. This process mainly happens in leaves, and oxygen is released."
        )
    if "fraction" in q:
        return (
            "A **fraction** shows part of a whole. In 1/2, the top number (1) is the numerator "
            "and the bottom number (2) is the denominator. It means one of two equal parts."
        )
    if "noun" in q:
        return "A **noun** names a person, place, animal or thing. Examples: teacher, school, cat and book."
    if "verb" in q:
        return "A **verb** tells an action or state. Examples: read, write, run, is and are."
    return (
        "The AI answer service is not connected yet, so I can't give a reliable full answer to this question. "
        "The app is ready for AI once you add a Gemini API key in Streamlit Secrets. "
        "You can still try: photosynthesis, fraction, noun or verb."
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show conversation history
for item in st.session_state.messages:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])

question = st.chat_input("Ask a school question…")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Preparing your study explanation…"):
            api_key = get_api_key()
            if api_key:
                try:
                    from google import genai

                    client = genai.Client(api_key=api_key)
                    result = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=build_prompt(question),
                    )
                    answer = result.text or "Sorry, I couldn't prepare an answer. Please try again."
                except Exception:
                    answer = (
                        "I couldn't connect to the AI service. Please check your Gemini API key "
                        "in Streamlit Secrets and try again."
                    )
            else:
                answer = offline_answer(question)

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

if st.session_state.messages:
    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()

with st.expander("⚙️ Setup: enable full AI answers"):
    st.markdown(
        """
1. Add the packages from `requirements.txt`.
2. Create a Gemini API key using Google AI Studio.
3. In Streamlit Community Cloud, open your app's **Settings → Secrets**.
4. Add this secret (replace the example text with your own key):

```toml
GEMINI_API_KEY = "YOUR_PRIVATE_API_KEY"
```

**Security:** Never paste your API key into this Python file or commit it to a public GitHub repository.
        """
    )

st.markdown(
    '<p class="small-note">Educational support only. Check important homework answers against your textbook and teacher’s instructions.</p>',
    unsafe_allow_html=True,
)
