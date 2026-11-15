import streamlit as st
import datetime
import uuid
import json
import os
import re
import time
from typing import Dict, List, Any, Optional

# ==============================================================================
# 1. CONFIGURATION & CONSTANTS (EDIT HERE)
# ==============================================================================
APP_TITLE = "MUHAMMAD ABDULLAH SCHOOL AI"
APP_SUBTITLE = "Next-Generation Smart Learning Platform (Class 1 – Class 10)"
APP_PASSWORD = "Muhammad Abdullah"  # <--- CONFIGURE LOGIN PASSWORD HERE

# JazzCash Guardian-Approved Payment Details
JAZZCASH_NUMBER = "03483020351"  # <--- APNA JAZZCASH NUMBER YAHAN LIKHEIN
JAZZCASH_ACCOUNT_NAME = "School Chatbot"          # <--- APNA ACCOUNT NAME YAHAN LIKHEIN

FREE_MESSAGE_LIMIT = 10
DATA_FILE = "school_ai_chats.json"

CLASSES = [f"Class {i}" for i in range(1, 11)]

SUBJECTS = {
    "General Knowledge": "🌍",
    "Mathematics": "📐",
    "English": "📖",
    "Computer Science": "💻",
    "Biology": "🧬",
    "Physics": "⚛️",
    "Chemistry": "🧪",
    "Urdu": "✍️",
    "Islamic Studies": "🕌",
    "Pakistan Studies": "🇵🇰",
}

SUBSCRIPTION_PLANS = {
    "weekly": {
        "name": "Weekly Scholar Pass",
        "price": "PKR 200",
        "duration": "7 Days Access",
        "popular": False,
        "features": [
            "Unlimited AI Tutor Questions (7 Days)",
            "All 10 Subjects (Class 1 – 10)",
            "Step-by-Step Math & Science Solutions",
            "Exam Revision Notes & Summaries",
        ],
    },
    "monthly": {
        "name": "Monthly Pro Pass",
        "price": "PKR 500",
        "duration": "30 Days Access",
        "popular": True,
        "features": [
            "Unlimited AI Tutor Questions (30 Days)",
            "Priority Response Generation",
            "Board Exam Past Paper Explanations",
            "Bilingual English & Urdu Support",
            "Full Chat History & Export",
        ],
    },
}

# ==============================================================================
# 2. PAGE CONFIGURATION & CUSTOM CSS (CHATGPT-INSPIRED DARK NAVY/PURPLE UI)
# ==============================================================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* Global App Styling */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .stApp {
            background: radial-gradient(circle at 15% 15%, #161b33 0%, #0b0e1a 45%, #070911 100%);
            color: #f1f5f9;
        }

        /* Hide default Streamlit branding clutter while keeping sidebar toggle */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {
            background: rgba(11, 14, 26, 0.75);
            backdrop-filter: blur(10px);
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0d1120 0%, #090c16 100%);
            border-right: 1px solid rgba(139, 92, 246, 0.2);
        }

        section[data-testid="stSidebar"] .stButton > button {
            border-radius: 10px;
            transition: all 0.2s ease;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(255, 255, 255, 0.03);
            color: #e2e8f0;
            font-weight: 500;
        }

        section[data-testid="stSidebar"] .stButton > button:hover {
            border-color: #8b5cf6;
            background: linear-gradient(90deg, rgba(139, 92, 246, 0.2), rgba(59, 130, 246, 0.2));
            color: #ffffff;
            transform: translateY(-1px);
        }

        /* Primary Gradient Buttons */
        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 15px rgba(124, 58, 237, 0.35);
            transition: all 0.25s ease !important;
        }

        div.stButton > button[kind="primary"]:hover {
            box-shadow: 0 6px 22px rgba(59, 130, 246, 0.55) !important;
            transform: translateY(-1px);
        }

        /* Brand Header Card in Sidebar */
        .brand-box {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.22), rgba(37, 99, 235, 0.18));
            border: 1px solid rgba(139, 92, 246, 0.35);
            border-radius: 14px;
            padding: 14px 16px;
            margin-bottom: 14px;
            text-align: center;
        }
        .brand-title {
            font-size: 1.02rem;
            font-weight: 800;
            letter-spacing: 0.4px;
            background: linear-gradient(90deg, #c084fc, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }
        .brand-sub {
            font-size: 0.72rem;
            color: #94a3b8;
            margin-top: 3px;
        }

        /* Top Context Bar */
        .context-banner {
            background: rgba(20, 26, 48, 0.75);
            border: 1px solid rgba(139, 92, 246, 0.28);
            border-radius: 14px;
            padding: 12px 18px;
            margin-bottom: 18px;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            backdrop-filter: blur(8px);
        }

        .badge-pill {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
            margin-right: 6px;
        }
        .badge-class {
            background: rgba(124, 58, 237, 0.25);
            color: #d8b4fe;
            border: 1px solid rgba(168, 85, 247, 0.4);
        }
        .badge-subject {
            background: rgba(37, 99, 235, 0.25);
            color: #93c5fd;
            border: 1px solid rgba(59, 130, 246, 0.4);
        }
        .badge-status {
            background: rgba(16, 185, 129, 0.18);
            color: #6ee7b7;
            border: 1px solid rgba(16, 185, 129, 0.35);
        }

        /* Welcome Hero Card */
        .welcome-card {
            background: linear-gradient(145deg, rgba(24, 31, 58, 0.85), rgba(14, 18, 36, 0.92));
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 20px;
            padding: 28px;
            margin: 10px 0 22px 0;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.35);
        }
        .welcome-title {
            font-size: 1.75rem;
            font-weight: 800;
            background: linear-gradient(90deg, #ffffff, #c4b5fd, #93c5fd);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        /* Chat Message Containers */
        div[data-testid="stChatMessage"] {
            background: rgba(20, 26, 46, 0.65);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 16px;
            padding: 14px 18px;
            margin-bottom: 12px;
        }

        /* Sidebar Cards */
        .sidebar-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 10px;
        }

        /* Pricing Cards */
        .pricing-card {
            background: linear-gradient(160deg, #151b33 0%, #0d1122 100%);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 18px;
            padding: 24px;
            height: 100%;
            position: relative;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        }
        .pricing-card-popular {
            background: linear-gradient(160deg, #1e1b4b 0%, #111827 100%);
            border: 2px solid #8b5cf6;
            border-radius: 18px;
            padding: 24px;
            height: 100%;
            position: relative;
            box-shadow: 0 12px 38px rgba(124, 58, 237, 0.35);
        }
        .popular-ribbon {
            display: inline-block;
            background: linear-gradient(90deg, #8b5cf6, #3b82f6);
            color: #ffffff;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 999px;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin-bottom: 10px;
        }
        .price-tag {
            font-size: 2.1rem;
            font-weight: 800;
            color: #ffffff;
            margin: 8px 0 2px 0;
        }
        .price-duration {
            color: #93c5fd;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 14px;
        }

        /* Login Screen Container */
        .login-card {
            background: linear-gradient(145deg, rgba(22, 28, 54, 0.92), rgba(11, 14, 27, 0.96));
            border: 1px solid rgba(139, 92, 246, 0.35);
            border-radius: 22px;
            padding: 34px 30px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.55);
            margin-top: 30px;
        }

        /* Footer */
        .custom-footer {
            text-align: center;
            color: #64748b;
            font-size: 0.78rem;
            padding: 18px 0 8px 0;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            margin-top: 28px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# 3. PERSISTENT LOCAL STORAGE HELPERS
# ==============================================================================
def load_saved_chats() -> Dict[str, Any]:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except Exception:
            return {}
    return {}


def save_chats_to_disk(chats: Dict[str, Any]) -> None:
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(chats, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ==============================================================================
# 4. EDUCATIONAL KNOWLEDGE BASE & CONVERSATIONAL AI ENGINE
# ==============================================================================
CURRICULUM_KB = {
    "Mathematics": {
        "keywords": ["algebra", "equation", "fraction", "geometry", "triangle", "circle", "area", "perimeter", "percentage", "ratio", "matrix", "quadratic", "trigonometry", "sin", "cos", "theorem", "pythagoras", "prime", "lcm", "hcf", "number"],
        "concepts": {
            "pythagoras": (
                "**Pythagoras Theorem**\n\n"
                "In a right-angled triangle, the square of the hypotenuse ($c$) is equal to the sum of the squares of the base ($a$) and perpendicular ($b$):\n\n"
                "$$c^2 = a^2 + b^2$$\n\n"
                "**Worked Example:**\n"
                "If base $a = 3\\text{ cm}$ and perpendicular $b = 4\\text{ cm}$:\n"
                "1. $c^2 = 3^2 + 4^2 = 9 + 16 = 25$\n"
                "2. $c = \\sqrt{25} = 5\\text{ cm}$"
            ),
            "quadratic": (
                "**Quadratic Equations (Standard Form & Formula)**\n\n"
                "A quadratic equation has the standard form:\n"
                "$$ax^2 + bx + c = 0 \\quad (a \\neq 0)$$\n\n"
                "**Quadratic Formula:**\n"
                "$$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$\n\n"
                "**Key Tip:** The expression $\\Delta = b^2 - 4ac$ is called the **discriminant**, which tells us whether the roots are real, equal, or imaginary."
            ),
        },
        "overview": "Mathematics builds logical reasoning across Arithmetic, Algebra, Geometry, Trigonometry, and Matrices.",
    },
    "Physics": {
        "keywords": ["newton", "force", "motion", "velocity", "acceleration", "gravity", "energy", "work", "power", "light", "lens", "mirror", "electricity", "ohm", "current", "voltage"],
        "concepts": {
            "newton": (
                "**Newton's Three Laws of Motion**\n\n"
                "1. **First Law (Law of Inertia):** An object remains at rest or in uniform motion unless acted upon by an external net force.\n"
                "2. **Second Law ($F = ma$):** Acceleration is directly proportional to net force and inversely proportional to mass.\n"
                "3. **Third Law:** To every action, there is always an equal and opposite reaction."
            ),
        },
        "overview": "Physics explains matter, energy, motion, forces, electricity, and the fundamental laws of the universe.",
    },
    "General Knowledge": {
        "keywords": ["capital", "planet", "solar", "continent", "ocean", "currency", "invention", "science", "world", "earth"],
        "concepts": {
            "solar": (
                "**Our Solar System**\n\n"
                "The Solar System consists of the Sun and **8 planets** orbiting around it:\n"
                "Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune."
            ),
        },
        "overview": "General Knowledge expands curiosity across world geography, space, inventions, and everyday science.",
    },
}


def check_conversational_intent(prompt: str, selected_class: str, selected_subject: str) -> Optional[str]:
    """
    Handles professional, polite conversational greetings (Assalam-o-Alaikum, Walaikum-o-Salam,
    Hello, Hi, Kya hal hai, Kaisi ho, etc.) and farewells naturally.
    """
    clean = re.sub(r"[^\w\s]", "", prompt.lower()).strip()
    words = clean.split()
    student_name = st.session_state.get("student_name", "Student")
    subj_icon = SUBJECTS.get(selected_subject, "📚")

    greeting_triggers = {
        "hi", "hello", "hey", "helo", "hii", "hiii",
        "salam", "assalam", "assalamualaikum", "assalam o alaikum",
        "aoa", "slam", "good morning", "good afternoon", "good evening",
    }
    wellbeing_triggers = [
        "kya hal hai", "kya haal hai", "kya hal ha", "kya haal ha",
        "kaisi ho", "kaise ho", "kesi ho", "kese ho", "kasy ho", "kasi ho",
        "how are you", "how r u", "how are u", "what's up", "whats up", "sup",
        "theek ho", "thik ho", "sab theek",
    ]
    farewell_triggers = [
        "bye", "goodbye", "good bye", "allah hafiz", "khuda hafiz",
        "take care", "see you", "tata", "good night", "goodnight",
        "shukriya", "thank you", "thanks", "thx", "bohat shukriya", "jazakallah",
    ]

    # 1. Farewell / Gratitude Handler
    if any(phrase in clean for phrase in farewell_triggers) and len(words) <= 6:
        if any(t in clean for t in ["shukriya", "thank", "thx", "jazakallah"]):
            return (
                f"You're very welcome, **{student_name}**! 😊✨\n\n"
                f"Aapki parhai mein madad karke mujhe bohat khushi hui. Agar **{selected_subject}** ({selected_class}) ya kisi aur topic mein koi aur sawal ho to zaroor poochein.\n\n"
                f"**Allah Hafiz & Best of Luck with your studies!** 🎓📚"
            )
        return (
            f"**Allah Hafiz, {student_name}!** 👋🌟\n\n"
            f"Apna bohat khayal rakhiyega aur dil laga kar parhai kijiyega. Jab bhi aapko **{selected_class}** ke kisi bhi subject mein madad chahiye ho, main yahan hazir hoon."
        )

    # 2. Greeting + Wellbeing Handler (Assalam-o-Alaikum -> Walaikum-o-Salam)
    has_greeting = (clean in greeting_triggers) or any(w in greeting_triggers for w in words[:3])
    has_wellbeing = any(phrase in clean for phrase in wellbeing_triggers)

    if (has_greeting or has_wellbeing) and len(words) <= 8:
        if has_wellbeing or "salam" in clean or "assalam" in clean or "aoa" in clean:
            return (
                f"**Wa Alaikum Assalam & Hello {student_name}!** 👋😊\n\n"
                f"Alhamdulillah, main bilkul theek aur tayyar hoon aapki parhai mein madad karne ke liye! Aap sunayein, aap kaise hain?\n\n"
                f"Abhi aap **{selected_class}** aur **{subj_icon} {selected_subject}** par kaam kar rahe hain. Batayein aaj hum kaunsa topic ya sawal samjhein?"
            )
        return (
            f"**Wa Alaikum Assalam & Hello {student_name}!** 👋🎓\n\n"
            f"**{APP_TITLE}** mein khush amdeed! Main bilkul theek hoon, umeed hai aap bhi khairiyat se honge.\n\n"
            f"Aap ne **{selected_class}** aur **{subj_icon} {selected_subject}** select kiya hua hai. Aap apna koi bhi sawal, definition, ya homework topic likh kar pooch sakte hain!"
        )

    return None


def try_evaluate_math_expression(prompt: str) -> Optional[str]:
    cleaned = prompt.lower().replace("what is", "").replace("calculate", "").replace("solve", "").replace("=", "").replace("?", "").strip()
    if re.fullmatch(r"[0-9\+\-\*\/\(\)\.\s\^]+", cleaned) and any(op in cleaned for op in ["+", "-", "*", "/", "^"]):
        expr = cleaned.replace("^", "**")
        try:
            result = eval(expr, {"__builtins__": None}, {})
            if isinstance(result, (int, float)):
                formatted_res = int(result) if isinstance(result, float) and result.is_integer() else round(result, 6)
                return (
                    f"**Step-by-Step Arithmetic Solution**\n\n"
                    f"- **Expression:** `{cleaned}`\n"
                    f"- **Order of Operations:** Brackets $\\rightarrow$ Orders $\\rightarrow$ Division/Multiplication $\\rightarrow$ Addition/Subtraction\n"
                    f"- **Final Answer:** **{formatted_res}**"
                )
        except Exception:
            return None
    return None


def get_grade_pedagogy_note(selected_class: str) -> str:
    grade_num = int(selected_class.split()[-1])
    if grade_num <= 3:
        return "Primary Level (Foundational & Easy-to-Understand Explanation)"
    elif grade_num <= 5:
        return "Elementary Level (Clear Concepts with Everyday Examples)"
    elif grade_num <= 8:
        return "Middle School Level (Structured Concepts, Definitions & Practice)"
    else:
        return "Secondary / Matric Board Level (Exam-Focused & Analytical Explanation)"


def generate_educational_response(user_prompt: str, selected_class: str, selected_subject: str) -> str:
    conv_reply = check_conversational_intent(user_prompt, selected_class, selected_subject)
    if conv_reply:
        return conv_reply

    prompt_lower = user_prompt.strip().lower()
    grade_level_label = get_grade_pedagogy_note(selected_class)
    subject_icon = SUBJECTS.get(selected_subject, "📚")

    if selected_subject in ["Mathematics", "Physics", "General Knowledge"]:
        math_solution = try_evaluate_math_expression(user_prompt)
        if math_solution:
            return (
                f"### {subject_icon} {selected_subject} • {selected_class}\n"
                f"*{grade_level_label}*\n\n"
                f"{math_solution}\n\n"
                f"💡 **Study Tip:** Always double-check signs and brackets when solving multi-step problems."
            )

    subject_data = CURRICULUM_KB.get(selected_subject, CURRICULUM_KB["General Knowledge"])
    matched_concept = None

    for key, explanation in subject_data["concepts"].items():
        if key in prompt_lower:
            matched_concept = explanation
            break

    if not matched_concept:
        for subj_name, subj_info in CURRICULUM_KB.items():
            for key, explanation in subj_info["concepts"].items():
                if key in prompt_lower:
                    matched_concept = explanation
                    break
            if matched_concept:
                break

    if matched_concept:
        return (
            f"### {subject_icon} {selected_subject} • {selected_class}\n"
            f"*{grade_level_label}*\n\n"
            f"{matched_concept}\n\n"
            f"---\n"
            f"**Want to practice?** Ask me for *practice questions*, *MCQs*, or a *simpler explanation* for **{selected_class}**!"
        )

    grade_num = int(selected_class.split()[-1])
    if grade_num <= 5:
        explanation_body = (
            f"#### 1. Simple Meaning\n"
            f"In **{selected_subject}** for **{selected_class}**, **\"{user_prompt}\"** is an important topic that helps us understand how things work in our daily life.\n\n"
            f"#### 2. Key Points to Remember\n"
            f"- **Core Idea:** Focus on the main definition and real-world examples first.\n"
            f"- **Observation:** Look for patterns, keywords, and rules connected to this topic in your textbook.\n"
            f"- **Practice:** Write down 3 short sentences or solve 2 basic examples in your notebook."
        )
    else:
        explanation_body = (
            f"#### 1. Concept Overview\n"
            f"Within **{selected_subject}** ({selected_class} curriculum), **\"{user_prompt}\"** requires understanding both theoretical definitions and practical applications.\n\n"
            f"#### 2. Structured Study Breakdown\n"
            f"- **Definition & Scope:** Identify the core principle, formula, or scientific rule governing this topic.\n"
            f"- **Board Exam Approach:** Present answers with clear headings, labeled diagrams/equations where applicable, and concise bullet points."
        )

    return (
        f"### {subject_icon} {selected_subject} • {selected_class}\n"
        f"*{grade_level_label}*\n\n"
        f"> **Topic / Question:** {user_prompt}\n\n"
        f"{explanation_body}"
    )


# ==============================================================================
# 5. SESSION STATE INITIALIZATION
# ==============================================================================
def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "student_name" not in st.session_state:
        st.session_state.student_name = "Muhammad Abdullah"

    if "selected_class" not in st.session_state:
        st.session_state.selected_class = "Class 9"

    if "selected_subject" not in st.session_state:
        st.session_state.selected_subject = "Mathematics"

    if "chats" not in st.session_state:
        saved = load_saved_chats()
        st.session_state.chats = saved

    if "current_chat_id" not in st.session_state:
        if st.session_state.chats:
            st.session_state.current_chat_id = list(st.session_state.chats.keys())[0]
        else:
            create_new_chat(switch=True)

    if "search_query" not in st.session_state:
        st.session_state.search_query = ""

    if "show_search_box" not in st.session_state:
        st.session_state.show_search_box = False

    if "active_view" not in st.session_state:
        st.session_state.active_view = "chat"

    if "messages_used" not in st.session_state:
        st.session_state.messages_used = 0

    if "is_premium" not in st.session_state:
        st.session_state.is_premium = False

    if "subscription_plan_name" not in st.session_state:
        st.session_state.subscription_plan_name = "Free Tier"

    if "subscription_expiry" not in st.session_state:
        st.session_state.subscription_expiry = None

    if "pending_plan_choice" not in st.session_state:
        st.session_state.pending_plan_choice = None

    if "copied_msg_id" not in st.session_state:
        st.session_state.copied_msg_id = None


def create_new_chat(switch: bool = True) -> str:
    chat_id = str(uuid.uuid4())[:8]
    now_str = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    st.session_state.chats[chat_id] = {
        "id": chat_id,
        "title": "New Study Session",
        "class": st.session_state.get("selected_class", "Class 9"),
        "subject": st.session_state.get("selected_subject", "Mathematics"),
        "created_at": now_str,
        "updated_at": now_str,
        "messages": [],
    }
    if switch:
        st.session_state.current_chat_id = chat_id
        st.session_state.active_view = "chat"
    save_chats_to_disk(st.session_state.chats)
    return chat_id


def delete_chat(chat_id: str):
    if chat_id in st.session_state.chats:
        del st.session_state.chats[chat_id]
        save_chats_to_disk(st.session_state.chats)
        if st.session_state.current_chat_id == chat_id:
            if st.session_state.chats:
                st.session_state.current_chat_id = list(st.session_state.chats.keys())[0]
            else:
                create_new_chat(switch=True)


# ==============================================================================
# 6. LOGIN SCREEN
# ==============================================================================
def render_login_page():
    _, col_center, _ = st.columns([1, 1.35, 1])
    with col_center:
        st.markdown(
            f"""
            <div class="login-card">
                <div style="text-align: center; margin-bottom: 22px;">
                    <div style="font-size: 3rem; margin-bottom: 6px;">🎓</div>
                    <h1 style="font-size: 1.6rem; font-weight: 800; margin: 0;
                        background: linear-gradient(90deg, #c084fc, #60a5fa);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        {APP_TITLE}
                    </h1>
                    <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 6px;">
                        {APP_SUBTITLE}
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container():
            st.markdown("#### 🔐 Student Access Portal")
            st.caption("Enter the school access password to launch your AI study workspace.")

            show_password = st.checkbox("👁️ Show password", value=False, key="login_show_pwd_toggle")
            pwd_input = st.text_input(
                "School Access Password",
                type="default" if show_password else "password",
                placeholder="Enter access password...",
                key="login_password_input",
            )

            student_display_name = st.text_input(
                "Student Name",
                value=st.session_state.student_name,
                placeholder="e.g., Muhammad Abdullah",
                key="login_student_name_input",
            )

            login_clicked = st.button("🚀 Access School AI", type="primary", use_container_width=True, key="login_submit_btn")

            if login_clicked:
                if pwd_input == APP_PASSWORD:
                    st.session_state.authenticated = True
                    if student_display_name.strip():
                        st.session_state.student_name = student_display_name.strip()
                    st.success("Authentication verified! Loading workspace...")
                    time.sleep(0.35)
                    st.rerun()
                else:
                    st.error("❌ Incorrect password. Please check your access password and try again.")


# ==============================================================================
# 7. SIDEBAR NAVIGATION
# ==============================================================================
def render_sidebar():
    with st.sidebar:
        st.markdown(
            f"""
            <div class="brand-box">
                <div style="font-size: 1.75rem; margin-bottom: 4px;">🎓</div>
                <div class="brand-title">{APP_TITLE}</div>
                <div class="brand-sub">Smart Tutor • Class 1 to Class 10</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_new, col_search = st.columns([1.35, 1])
        with col_new:
            if st.button("➕ New Chat", use_container_width=True, type="primary", key="sb_new_chat_btn"):
                create_new_chat(switch=True)
                st.rerun()
        with col_search:
            if st.button("🔍 Search", use_container_width=True, key="sb_toggle_search_btn"):
                st.session_state.show_search_box = not st.session_state.show_search_box
                if not st.session_state.show_search_box:
                    st.session_state.search_query = ""
                st.rerun()

        if st.session_state.show_search_box:
            st.session_state.search_query = st.text_input(
                "Search conversations",
                value=st.session_state.search_query,
                placeholder="Filter chats...",
                label_visibility="collapsed",
                key="sb_search_input",
            )

        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            if st.button("💬 AI Tutor", use_container_width=True, key="sb_nav_chat_btn"):
                st.session_state.active_view = "chat"
                st.rerun()
        with nav_col2:
            if st.button("📊 Dashboard", use_container_width=True, key="sb_nav_dash_btn"):
                st.session_state.active_view = "dashboard"
                st.rerun()

        st.markdown("---")

        st.markdown("##### 📚 Academic Settings")
        selected_class = st.selectbox(
            "Select Class",
            options=CLASSES,
            index=CLASSES.index(st.session_state.selected_class),
            key="sb_class_select",
        )
        if selected_class != st.session_state.selected_class:
            st.session_state.selected_class = selected_class
            if st.session_state.current_chat_id in st.session_state.chats:
                st.session_state.chats[st.session_state.current_chat_id]["class"] = selected_class
                save_chats_to_disk(st.session_state.chats)

        subject_options = list(SUBJECTS.keys())
        selected_subject = st.selectbox(
            "Select Subject",
            options=subject_options,
            index=subject_options.index(st.session_state.selected_subject),
            format_func=lambda s: f"{SUBJECTS[s]} {s}",
            key="sb_subject_select",
        )
        if selected_subject != st.session_state.selected_subject:
            st.session_state.selected_subject = selected_subject
            if st.session_state.current_chat_id in st.session_state.chats:
                st.session_state.chats[st.session_state.current_chat_id]["subject"] = selected_subject
                save_chats_to_disk(st.session_state.chats)

        st.markdown("---")

        st.markdown("##### 🕒 Recent Chats")
        query = st.session_state.search_query.strip().lower()
        chat_items = list(reversed(list(st.session_state.chats.values())))

        filtered_chats = [
            c for c in chat_items
            if not query or query in c.get("title", "").lower() or query in c.get("subject", "").lower()
        ]

        if not filtered_chats:
            st.caption("No matching conversations found.")
        else:
            for chat in filtered_chats[:12]:
                cid = chat["id"]
                is_active = (cid == st.session_state.current_chat_id) and (st.session_state.active_view == "chat")
                subj_emoji = SUBJECTS.get(chat.get("subject", ""), "💬")
                raw_title = chat.get("title", "New Study Session")
                short_title = (raw_title[:22] + "…") if len(raw_title) > 23 else raw_title
                label = f"{'🟣' if is_active else subj_emoji} {short_title}"

                c_open, c_del = st.columns([4.3, 1])
                with c_open:
                    if st.button(label, key=f"open_chat_{cid}", use_container_width=True):
                        st.session_state.current_chat_id = cid
                        st.session_state.selected_class = chat.get("class", st.session_state.selected_class)
                        st.session_state.selected_subject =
