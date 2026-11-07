import streamlit as st

# ویب سائٹ کا ٹائٹل اور سیٹنگ
st.set_page_config(page_title="School Student AI Chatbot", page_icon="📚", layout="centered")

st.title("📚 School Student Helper Chatbot (Classes 1 to 10)")
st.write("ہیلو! میں آپ کا اسکول کا اسسٹنٹ ہوں۔ آپ مجھ سے اردو، انگلش، سائنس (فزکس، کیمسٹری)، اسلامیات یا کسی بھی مضمون کے بارے میں پوچھ سکتے ہیں، یا ہوم ورک، خطوط (Khutoot) اور مضامین میں مدد لے سکتے ہیں!")

# چیٹ کی ہسٹری کو محفوظ رکھنے کے لیے
if "messages" not in st.session_state:
    st.session_state.messages = []

# پرانی چیٹس کو سکرین پر دکھانا
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# یوزر کا ان پٹ لینے کے لیے باکس
user_input = st.chat_input("یہاں اپنا سوال پوچھیں (مثلاً: سائنس کا کوئی سوال، انگلش لیٹر، یا اردو کا خط)...")

if user_input:
    # یوزر کا پیغام دکھانا
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # باٹ کا جواب (یہاں آپ بعد میں AI کی API جوڑ سکتے ہیں، فی الحال یہ آپ کی رہنمائی کے لیے تیار ہے)
    if "urdu" in user_input.lower() or "خات" in user_input.lower() or "خط" in user_input.lower():
        bot_response = "آپ نے اردو یا خط کے بارے میں پوچھا ہے۔ (یہاں باٹ آپ کے مطلوبہ خط یا مضمون کی مکمل تفصیل اردو میں فراہم کرے گا)۔"
    elif "physics" in user_input.lower() or "chemistry" in user_input.lower() or "science" in user_input.lower():
        bot_response = "یہ سائنس (فزکس/کیمسٹری) سے متعلق سوال ہے۔ (یہاں اس کا سائنسی جواب اور آسان وضاحت دی جائے گی)۔"
    else:
        bot_response = f"موصول ہوا! آپ نے پوچھا ہے: '{user_input}'۔ میں کلاس 1 سے 10 تک کے نصاب کے مطابق اس کی مکمل وضاحت اور مدد فراہم کر رہا ہوں۔"

    # باٹ کا جواب دکھانا
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
