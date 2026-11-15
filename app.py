
import streamlit as st
import time

st.set_page_config(
    page_title="Muhammad Abdullah School AI",
    page_icon="🎓",
    layout="wide"
)

# ---------------- SESSION SETTINGS ----------------

TRIAL_SECONDS = 24 * 60 * 60
WEEKLY_PRICE = 200
MONTHLY_PRICE = 500

if "trial_started" not in st.session_state:
    st.session_state.trial_started = time.time()

if "subscription_until" not in st.session_state:
    st.session_state.subscription_until = 0

now = time.time()

trial_active = (
    now - st.session_state.trial_started < TRIAL_SECONDS
)

paid_active = now < st.session_state.subscription_until

# ---------------- PROFESSIONAL DESIGN ----------------

st.markdown("""
<style>

.stApp {
    background:
    radial-gradient(circle at top left, #263c78 0%, transparent 35%),
    radial-gradient(circle at bottom right, #542d80 0%, transparent 35%),
    linear-gradient(135deg, #080e20, #101a35 55%, #17102e);
    color: white;
}

header, footer {
    visibility: hidden;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    text-align: center;
    padding: 35px 15px 25px 15px;
}

.hero h1 {
    color: #ffffff;
    font-size: clamp(30px, 5vw, 48px);
    font-weight: 800;
    letter-spacing: -1px;
}

.hero p {
    color: #b9c7e8;
    font-size: 17px;
}

.plan-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 20px;
    padding: 26px 22px;
    min-height: 245px;
    backdrop-filter: blur(15px);
    box-shadow: 0 12px 35px rgba(0,0,0,0.22);
    margin-bottom: 12px;
}

.featured {
    border: 2px solid #8b7bff;
    background: linear-gradient(
        145deg,
        rgba(91,74,180,0.35),
        rgba(255,255,255,0.07)
    );
}

.plan-name {
    font-size: 21px;
    font-weight: 700;
    color: white;
}

.plan-price {
    font-size: 36px;
    font-weight: 800;
    color: #a99cff;
    margin: 14px 0;
}

.plan-description {
    color: #c2cce3;
    font-size: 14px;
}

.tag {
    display: inline-block;
    background: #6654cb;
    color: white;
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: bold;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    min-height: 48px;
    border: 1px solid #8175ed;
    background: linear-gradient(90deg, #6654cb, #9276f5);
    color: white;
    font-weight: 700;
    transition: 0.2s;
}

.stButton > button:hover {
    border-color: white;
    background: linear-gradient(90deg, #7968e2, #a18bff);
    color: white;
}

.notice {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 14px;
    padding: 16px;
    color: #cbd5e1;
    text-align: center;
    margin-top: 22px;
}

.footer {
    text-align: center;
    color: #8492b3;
    padding: 25px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SUBSCRIPTION SCREEN ----------------

def show_subscription():

    st.markdown("""
    <div class="hero">
        <div style="font-size:55px;">🎓</div>
        <h1>Muhammad Abdullah School AI</h1>
        <p>Your Smart Learning Partner</p>
        <div class="tag">PREMIUM EDUCATION EXPERIENCE</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<h2 style='text-align:center;color:white;'>Choose Your Plan</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;color:#b9c7e8;'>"
        "Select an access plan to continue learning."
        "</p>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown("""
        <div class="plan-card">
            <div class="plan-name">🎁 Free Trial</div>
            <div class="plan-price">Rs. 0</div>
            <div class="plan-description">
                • 1 Day Access<br><br>
                • Explore the chatbot<br><br>
                • Try learning features
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Start Free Trial", key="trial"):
            st.session_state.trial_started = time.time()
            st.rerun()

    with col2:
        st.markdown("""
        <div class="plan-card">
            <div class="plan-name">📅 Weekly Plan</div>
            <div class="plan-price">Rs. 200</div>
            <div class="plan-description">
                • 7 Days Access<br><br>
                • School AI Assistant<br><br>
                • Learning support
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select Weekly Plan", key="weekly"):
            st.session_state.selected_plan = "weekly"
            st.info("Payment setup is required before activation.")

    with col3:
        st.markdown("""
        <div class="plan-card featured">
            <div class="tag">POPULAR PLAN</div>
            <div class="plan-name">⭐ Monthly Plan</div>
            <div class="plan-price">Rs. 500</div>
            <div class="plan-description">
                • 30 Days Access<br><br>
                • School AI Assistant<br><br>
                • Learning support
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Select Monthly Plan", key="monthly"):
            st.session_state.selected_plan = "monthly"
            st.info("Payment setup is required before activation.")

    st.markdown("""
    <div class="notice">
        🔒 Secure access • Smart learning • Student-friendly experience
        <br><br>
        Payment activation will be available after a verified payment
        gateway is connected.
    </div>

    <div class="footer">
        © 2026 Muhammad Abdullah School AI
        <br>
        Designed for smarter learning.
    </div>
    """, unsafe_allow_html=True)


# ---------------- ACCESS CONTROL ----------------

if paid_active:

    st.success("Your subscription is active!")

elif trial_active:

    remaining = int(
        TRIAL_SECONDS - (now - st.session_state.trial_started)
    )

    hours = remaining // 3600
    minutes = (remaining % 3600) // 60

    st.markdown("""
    <div class="hero">
        <h1>🎓 Muhammad Abdullah School AI</h1>
        <p>Your free learning trial is active!</p>
    </div>
    """, unsafe_allow_html=True)

    st.success("🎉 Your 1-day free trial is active!")
    st.info(f"⏳ Time remaining: {hours} hours and {minutes} minutes")

    st.markdown("### Your AI School Assistant")
    st.write("Paste your existing chatbot interface code below this section.")

else:
    show_subscription()
    st.stop()
