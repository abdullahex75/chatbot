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
APP_PASSWORD = "CES Abdullah"  # <--- CONFIGURE LOGIN PASSWORD HERE

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
    page_title="School Chatbot",
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
# 3. PERSISTENT LOCAL STORAGE HELPERS (WINDOWS & CLOUD SAFE)
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
            "fraction": (
                "**Understanding Fractions**\n\n"
                "A fraction $\\frac{a}{b}$ represents equal parts of a whole, where:\n"
                "- **$a$ (Numerator):** Number of parts taken.\n"
                "- **$b$ (Denominator):** Total equal parts ($b \\neq 0$).\n\n"
                "**Addition Rule:** Make denominators equal using LCM, then add numerators:\n"
                "$$\\frac{1}{2} + \\frac{1}{3} = \\frac{3}{6} + \\frac{2}{6} = \\frac{5}{6}$$"
            ),
            "percentage": (
                "**Percentage Formula & Applications**\n\n"
                "Percentage means *per hundred* (%):\n"
                "$$\\text{Percentage} = \\left(\\frac{\\text{Obtained Value}}{\\text{Total Value}}\\right) \\times 100$$\n\n"
                "**Example:** If a student scores $425$ out of $500$ marks:\n"
                "$$\\frac{425}{500} \\times 100 = 85\\%$$"
            ),
        },
        "overview": "Mathematics builds logical reasoning across Arithmetic, Algebra, Geometry, Trigonometry, and Matrices.",
    },
    "Physics": {
        "keywords": ["newton", "force", "motion", "velocity", "acceleration", "gravity", "energy", "work", "power", "light", "lens", "mirror", "electricity", "ohm", "current", "voltage", "wave", "sound", "heat", "density", "pressure"],
        "concepts": {
            "newton": (
                "**Newton's Three Laws of Motion**\n\n"
                "1. **First Law (Law of Inertia):** An object remains at rest or in uniform motion in a straight line unless acted upon by an external net force.\n"
                "2. **Second Law ($F = ma$):** The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass:\n"
                "   $$F = m \\times a$$\n"
                "3. **Third Law:** To every action, there is always an equal and opposite reaction."
            ),
            "ohm": (
                "**Ohm's Law**\n\n"
                "The electric current ($I$) flowing through a metallic conductor is directly proportional to the potential difference ($V$) across its ends, provided temperature remains constant:\n\n"
                "$$V = I \\times R$$\n\n"
                "- **$V$:** Voltage in Volts ($\\text{V}$)\n"
                "- **$I$:** Current in Amperes ($\\text{A}$)\n"
                "- **$R$:** Resistance in Ohms ($\\Omega$)"
            ),
            "energy": (
                "**Kinetic & Potential Energy**\n\n"
                "- **Kinetic Energy ($K.E.$):** Energy due to motion:\n"
                "  $$K.E. = \\frac{1}{2}mv^2$$\n"
                "- **Gravitational Potential Energy ($P.E.$):** Energy due to position/height:\n"
                "  $$P.E. = mgh$$\n"
                "- **Law of Conservation of Energy:** Energy can neither be created nor destroyed; it only transforms from one form to another."
            ),
        },
        "overview": "Physics explains matter, energy, motion, forces, electricity, waves, and the fundamental laws of the universe.",
    },
    "Chemistry": {
        "keywords": ["atom", "molecule", "element", "compound", "periodic", "acid", "base", "salt", "ph", "bond", "ionic", "covalent", "reaction", "mole", "valency", "electron", "proton", "neutron", "solution"],
        "concepts": {
            "atom": (
                "**Structure of an Atom**\n\n"
                "An atom is the smallest particle of an element that takes part in a chemical reaction. It consists of three fundamental subatomic particles:\n"
                "- **Proton ($p^+$):** Positively charged, located inside the nucleus.\n"
                "- **Neutron ($n^0$):** Neutral (no charge), located inside the nucleus.\n"
                "- **Electron ($e^-$):** Negatively charged, revolves around the nucleus in fixed energy shells ($K, L, M, N$)."
            ),
            "acid": (
                "**Acids, Bases, and the pH Scale**\n\n"
                "- **Acids:** Release hydrogen ions ($H^+$) in aqueous solution, taste sour, and turn blue litmus red (e.g., $\\text{HCl}, \\text{H}_2\\text{SO}_4$).\n"
                "- **Bases:** Release hydroxide ions ($OH^-$) in aqueous solution, feel soapy, and turn red litmus blue (e.g., $\\text{NaOH}$).\n"
                "- **pH Scale ($0 - 14$):** $\\text{pH} < 7$ is acidic, $\\text{pH} = 7$ is neutral (pure water), and $\\text{pH} > 7$ is basic/alkaline."
            ),
            "bond": (
                "**Chemical Bonding (Ionic vs. Covalent)**\n\n"
                "1. **Ionic Bond:** Formed by complete transfer of electrons from a metal to a non-metal (e.g., $\\text{NaCl}$).\n"
                "2. **Covalent Bond:** Formed by mutual sharing of electrons between non-metal atoms (e.g., $\\text{H}_2\\text{O}, \\text{CH}_4$)."
            ),
        },
        "overview": "Chemistry explores the composition, structure, properties, and reactions of matter.",
    },
    "Biology": {
        "keywords": ["cell", "mitochondria", "photosynthesis", "respiration", "heart", "blood", "digestive", "nervous", "dna", "gene", "ecosystem", "plant", "animal", "bacteria", "virus", "enzyme", "tissue", "organ"],
        "concepts": {
            "cell": (
                "**The Cell — Basic Unit of Life**\n\n"
                "Every living organism is made of cells. Key organelles include:\n"
                "- **Nucleus:** Control center of the cell containing genetic material (DNA).\n"
                "- **Mitochondria:** Powerhouse of the cell; produces energy in the form of **ATP**.\n"
                "- **Ribosomes:** Sites of protein synthesis.\n"
                "- **Chloroplast (Plants only):** Contains chlorophyll for photosynthesis.\n"
                "- **Cell Wall (Plants only):** Rigid outer layer made of cellulose for structural support."
            ),
            "photosynthesis": (
                "**Photosynthesis in Green Plants**\n\n"
                "Photosynthesis is the process by which green plants convert light energy into chemical energy (glucose) using carbon dioxide and water:\n\n"
                "$$6\\text{CO}_2 + 6\\text{H}_2\\text{O} \\xrightarrow{\\text{Sunlight & Chlorophyll}} \\text{C}_6\\text{H}_{12}\\text{O}_6 + 6\\text{O}_2$$\n\n"
                "- **Reactants:** Carbon dioxide & Water\n"
                "- **Products:** Glucose & Oxygen"
            ),
            "heart": (
                "**Human Heart & Blood Circulation**\n\n"
                "The human heart has **four chambers**:\n"
                "1. **Right Atrium:** Receives deoxygenated blood from the body.\n"
                "2. **Right Ventricle:** Pumps deoxygenated blood to the lungs for oxygenation.\n"
                "3. **Left Atrium:** Receives oxygenated blood from the lungs.\n"
                "4. **Left Ventricle:** Pumps oxygenated blood to the entire body via the **Aorta**."
            ),
        },
        "overview": "Biology studies living organisms, cellular processes, human anatomy, genetics, and ecology.",
    },
    "Computer Science": {
        "keywords": ["computer", "cpu", "ram", "rom", "software", "hardware", "algorithm", "flowchart", "python", "html", "network", "internet", "binary", "data", "database", "loop", "variable", "ai", "operating system"],
        "concepts": {
            "cpu": (
                "**Central Processing Unit (CPU)**\n\n"
                "The CPU is the brain of the computer that executes instructions. Its three main components are:\n"
                "1. **ALU (Arithmetic Logic Unit):** Performs mathematical calculations and logical comparisons.\n"
                "2. **CU (Control Unit):** Directs the flow of data and instructions between memory and I/O devices.\n"
                "3. **Registers:** Ultra-fast temporary storage locations inside the processor."
            ),
            "binary": (
                "**Binary Number System**\n\n"
                "Computers process all data in **Binary (Base-2)** using only two digits: `0` and `1` (bits).\n"
                "- **8 Bits = 1 Byte**\n"
                "- **1024 Bytes = 1 Kilobyte (KB)**\n"
                "- **Example Conversion:** Decimal `13` in binary is `1101` ($8 + 4 + 0 + 1 = 13$)."
            ),
            "algorithm": (
                "**Algorithms & Flowcharts**\n\n"
                "- **Algorithm:** A finite, step-by-step sequence of unambiguous instructions used to solve a specific problem.\n"
                "- **Flowchart:** A visual diagram representing an algorithm using standard symbols (Oval for Start/Stop, Parallelogram for Input/Output, Rectangle for Processing, Diamond for Decision)."
            ),
        },
        "overview": "Computer Science covers hardware, software, programming logic, algorithms, networks, and problem-solving.",
    },
    "English": {
        "keywords": ["grammar", "tense", "noun", "verb", "adjective", "adverb", "essay", "letter", "application", "active", "passive", "direct", "indirect", "preposition", "pronoun", "story", "summary", "comprehension"],
        "concepts": {
            "tense": (
                "**English Tenses Quick Reference**\n\n"
                "Tenses show the time of an action (**Present, Past, Future**) across four aspects:\n"
                "1. **Indefinite (Simple):** *She writes a letter.* / *She wrote a letter.* / *She will write a letter.*\n"
                "2. **Continuous:** *She is writing.* / *She was writing.* / *She will be writing.*\n"
                "3. **Perfect:** *She has written.* / *She had written.* / *She will have written.*\n"
                "4. **Perfect Continuous:** *She has been writing since morning.*"
            ),
            "parts of speech": (
                "**The 8 Parts of Speech**\n\n"
                "1. **Noun:** Name of a person, place, thing, or idea (*Lahore, book, honesty*).\n"
                "2. **Pronoun:** Replaces a noun (*he, she, they, it*).\n"
                "3. **Verb:** Expresses action or state (*run, study, is*).\n"
                "4. **Adjective:** Describes a noun (*intelligent, blue, tall*).\n"
                "5. **Adverb:** Modifies a verb, adjective, or adverb (*quickly, very*).\n"
                "6. **Preposition:** Shows relation (*in, on, under, beside*).\n"
                "7. **Conjunction:** Joins words or clauses (*and, but, because*).\n"
                "8. **Interjection:** Expresses sudden emotion (*Hurrah!, Alas!*)."
            ),
        },
        "overview": "English develops reading comprehension, grammar accuracy, creative essay writing, and formal communication.",
    },
    "Urdu": {
        "keywords": ["urdu", "ghazal", "nazm", "ism", "fail", "harf", "mazmoon", "darkhwast", "khat", "tashreeh", "muhawara", "wahid", "jama", "mutazad"],
        "concepts": {
            "ism": (
                "**کلمہ کی اقسام (Parts of Speech in Urdu)**\n\n"
                "بامعنی لفظ کو **کلمہ** کہتے ہیں، جس کی تین بنیادی اقسام ہیں:\n"
                "1. **اسم (Noun):** وہ کلمہ جو کسی شخص، جگہ یا چیز کا نام ہو (مثلاً: لاہور، کتاب، عبداللہ)۔\n"
                "2. **فعل (Verb):** وہ کلمہ جس میں کسی کام کا کرنا یا ہونا زمانے کے ساتھ پایا جائے (مثلاً: پڑھتا ہے، لکھا، جائے گا)۔\n"
                "3. **حرف (Preposition/Conjunction):** وہ کلمہ جو اکیلا پورا معنی نہ دے بلکہ اسموں اور فعلوں کو آپس میں ملائے (مثلاً: میں، پر، سے، اور)۔"
            ),
        },
        "overview": "Urdu literature and grammar strengthen expression, poetry appreciation (نظم و غزل), and formal writing.",
    },
    "Islamic Studies": {
        "keywords": ["islam", "quran", "hadith", "pillar", "arkan", "namaz", "salah", "zakat", "roza", "fasting", "hajj", "tauheed", "prophet", "seerah", "caliph", "khulafa"],
        "concepts": {
            "pillar": (
                "**Five Pillars of Islam (ارکانِ اسلام)**\n\n"
                "1. **Shahadah (توحید و رسالت):** Declaring that there is no god worthy of worship except Allah, and Muhammad (ﷺ) is His final Messenger.\n"
                "2. **Salah (نماز):** Offering the five obligatory daily prayers.\n"
                "3. **Zakat (زکوٰۃ):** Giving 2.5% of eligible annual savings to the poor and needy.\n"
                "4. **Sawm (روزہ):** Fasting during the blessed month of Ramadan from dawn until sunset.\n"
                "5. **Hajj (حج):** Pilgrimage to Makkah at least once in a lifetime for those physically and financially able."
            ),
        },
        "overview": "Islamic Studies teaches Quranic guidance, Hadith, Seerah of the Holy Prophet (ﷺ), and Islamic ethics.",
    },
    "Pakistan Studies": {
        "keywords": ["pakistan", "quaid", "iqbal", "1947", "1940", "resolution", "ideology", "indus", "river", "province", "constitution", "1973", "mountain", "k2", "karakoram", "sir syed"],
        "concepts": {
            "resolution": (
                "**Lahore Resolution (Pakistan Resolution — 23 March 1940)**\n\n"
                "- **Date & Venue:** Passed on **23rd March 1940** at Minto Park (now Iqbal Park), Lahore, during the annual session of the All-India Muslim League.\n"
                "- **Presided by:** Quaid-e-Azam Muhammad Ali Jinnah.\n"
                "- **Moved by:** Sher-e-Bengal A.K. Fazlul Huq.\n"
                "- **Significance:** It formally demanded independent states for the Muslims of Northwestern and Eastern zones of India, laying the foundation for the creation of Pakistan on **14 August 1947**."
            ),
            "constitution": (
                "**Constitution of Pakistan (1973)**\n\n"
                "- Enacted on **14 August 1973**.\n"
                "- Established a **Federal Parliamentary System** of government.\n"
                "- Declared **Islam** as the State Religion and named the country the **Islamic Republic of Pakistan**.\n"
                "- Bicameral legislature (**Majlis-e-Shoora**) consisting of the National Assembly and the Senate."
            ),
        },
        "overview": "Pakistan Studies covers the Pakistan Movement, Ideology, Geography, Climate, Resources, and Constitutional History.",
    },
    "General Knowledge": {
        "keywords": ["capital", "planet", "solar", "continent", "ocean", "currency", "invention", "science", "world", "earth", "sun", "moon", "quiz", "fact"],
        "concepts": {
            "solar": (
                "**Our Solar System**\n\n"
                "The Solar System consists of the Sun and **8 planets** orbiting around it in order from closest to farthest:\n"
                "1. **Mercury** (Smallest & closest to the Sun)\n"
                "2. **Venus** (Hottest planet)\n"
                "3. **Earth** (Our home planet with liquid water & life)\n"
                "4. **Mars** (The Red Planet)\n"
                "5. **Jupiter** (Largest planet)\n"
                "6. **Saturn** (Famous for its prominent ring system)\n"
                "7. **Uranus** (Ice giant tilted on its side)\n"
                "8. **Neptune** (Farthest planet with supersonic winds)"
            ),
        },
        "overview": "General Knowledge expands curiosity across world geography, space, inventions, current awareness, and everyday science.",
    },
}


def check_conversational_intent(prompt: str, selected_class: str, selected_subject: str) -> Optional[str]:
    """
    Handles starting greetings (Hello, Hi, Assalam-o-Alaikum, Kya hal hai, Kaisi ho)
    and ending farewells (Bye, Allah Hafiz, Shukriya, Thank you) naturally.
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

    # 1. Check Farewell / Ending Messages
    if any(phrase in clean for phrase in farewell_triggers) and len(words) <= 6:
        if any(t in clean for t in ["shukriya", "thank", "thx", "jazakallah"]):
            return (
                f"You're very welcome, **{student_name}**! 😊✨\n\n"
                f"Mujhe aapki madad karke bohat khushi hui. Agar **{selected_subject}** ({selected_class}) ya kisi aur subject mein koi aur sawal ho to zaroor poochein.\n\n"
                f"**Allah Hafiz & Best of Luck with your studies!** 🎓📚"
            )
        return (
            f"**Allah Hafiz, {student_name}!** 👋🌟\n\n"
            f"Apna bohat khayal rakhiyega aur dil laga kar parhai kijiyega. Jab bhi aapko **{selected_class}** ke kisi bhi subject mein madad chahiye ho, main yahan hazir hoon.\n\n"
            f"**See you in our next study session!** 🎓"
        )

    # 2. Check Starting Greetings + "Kya hal hai / Kaisi ho"
    has_greeting = (clean in greeting_triggers) or any(w in greeting_triggers for w in words[:3])
    has_wellbeing = any(phrase in clean for phrase in wellbeing_triggers)

    if (has_greeting or has_wellbeing) and len(words) <= 8:
        if has_wellbeing:
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
    """Safely evaluates straightforward arithmetic queries like 'solve 25 * 4 + 10'."""
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
                    f"- **Order of Operations (BODMAS / PEMDAS):** Brackets $\\rightarrow$ Orders $\\rightarrow$ Division/Multiplication $\\rightarrow$ Addition/Subtraction\n"
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
    # 0. Check for starting greetings ("Hello", "Hi", "Kya hal hai", "Kaisi ho") or ending ("Bye", "Allah Hafiz", "Thanks")
    conversational_reply = check_conversational_intent(user_prompt, selected_class, selected_subject)
    if conversational_reply:
        return conversational_reply

    prompt_lower = user_prompt.strip().lower()
    grade_level_label = get_grade_pedagogy_note(selected_class)
    subject_icon = SUBJECTS.get(selected_subject, "📚")

    # 1. Check direct arithmetic expressions
    if selected_subject in ["Mathematics", "Physics", "General Knowledge"]:
        math_solution = try_evaluate_math_expression(user_prompt)
        if math_solution:
            return (
                f"### {subject_icon} {selected_subject} • {selected_class}\n"
                f"*{grade_level_label}*\n\n"
                f"{math_solution}\n\n"
                f"💡 **Study Tip:** Always double-check signs and brackets when solving multi-step problems."
            )

    # 2. Search selected subject's curriculum knowledge base
    subject_data = CURRICULUM_KB.get(selected_subject, CURRICULUM_KB["General Knowledge"])
    matched_concept = None

    for key, explanation in subject_data["concepts"].items():
        if key in prompt_lower:
            matched_concept = explanation
            break

    # 3. Cross-check all subjects if user asked a specific topic under a broader subject
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

    # 4. Structured Academic Tutor Response for any custom topic/question
    grade_num = int(selected_class.split()[-1])
    if grade_num <= 5:
        explanation_body = (
            f"#### 1. Simple Meaning\n"
            f"In **{selected_subject}** for **{selected_class}**, **\"{user_prompt}\"** is an important topic that helps us understand how things work in our daily life.\n\n"
            f"#### 2. Key Points to Remember\n"
            f"- **Core Idea:** Focus on the main definition and real-world examples first.\n"
            f"- **Observation:** Look for patterns, keywords, and rules connected to this topic in your textbook.\n"
            f"- **Practice:** Write down 3 short sentences or solve 2 basic examples in your notebook.\n\n"
            f"#### 3. Quick Check Question\n"
            f"Can you tell me one example of **{user_prompt}** from your daily life or textbook?"
        )
    else:
        explanation_body = (
            f"#### 1. Concept Overview\n"
            f"Within **{selected_subject}** ({selected_class} curriculum), **\"{user_prompt}\"** requires understanding both theoretical definitions and practical applications.\n\n"
            f"#### 2. Structured Study Breakdown\n"
            f"- **Definition & Scope:** Identify the core principle, formula, or historical/scientific rule governing this topic.\n"
            f"- **Key Mechanism / Reasoning:** Break the problem into *Given Data / Premise*, *Core Rule*, and *Conclusion*.\n"
            f"- **Board Exam Approach:** Present answers with clear headings, labeled diagrams/equations where applicable, and concise bullet points.\n\n"
            f"#### 3. Recommended Next Step\n"
            f"Share the exact textbook question, numerical values, or paragraph you are studying, and I will walk you through the complete step-by-step solution."
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
        st.session_state.student_name = "Abdullah Student"

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
# 6. LOGIN SCREEN (PASSWORD-ONLY WITH VISIBILITY TOGGLE)
# ==============================================================================
def render_login_page():
    col_left, col_center, col_right = st.columns([1, 1.35, 1])
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
                "Student Name (Optional)",
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

        st.markdown(
            f"""
            <div class="custom-footer">
                © {datetime.datetime.now().year} {APP_TITLE} • Secure Student Portal
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==============================================================================
# 7. SIDEBAR (CHATGPT-STYLE NAVIGATION, SEARCH, HISTORY, CLASS/SUBJECT, USAGE)
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
                placeholder="Filter by title, subject, or message...",
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

        if query:
            filtered_chats = []
            for c in chat_items:
                in_title = query in c.get("title", "").lower()
                in_subj = query in c.get("subject", "").lower()
                in_msgs = any(query in m.get("content", "").lower() for m in c.get("messages", []))
                if in_title or in_subj or in_msgs:
                    filtered_chats.append(c)
        else:
            filtered_chats = chat_items

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
                    if st.button(label, key=f"open_chat_{cid}", use_container_width=True, help=f"{raw_title} ({chat.get('class')} • {chat.get('subject')})"):
                        st.session_state.current_chat_id = cid
                        st.session_state.selected_class = chat.get("class", st.session_state.selected_class)
                        st.session_state.selected_subject = chat.get("subject", st.session_state.selected_subject)
                        st.session_state.active_view = "chat"
                        st.rerun()
                with c_del:
                    if st.button("🗑️", key=f"del_chat_{cid}", use_container_width=True, help="Delete chat"):
                        delete_chat(cid)
                        st.rerun()

        st.markdown("---")

        st.markdown("##### ⚡ Account Usage")
        remaining = max(0, FREE_MESSAGE_LIMIT - st.session_state.messages_used)
        progress_val = min(1.0, st.session_state.messages_used / FREE_MESSAGE_LIMIT)

        if st.session_state.is_premium:
            st.markdown(
                f"""
                <div class="sidebar-card">
                    <div style="font-size: 0.82rem; font-weight: 700; color: #6ee7b7;">👑 Premium Active</div>
                    <div style="font-size: 0.75rem; color: #cbd5e1; margin-top: 2px;">Plan: {st.session_state.subscription_plan_name}</div>
                    <div style="font-size: 0.72rem; color: #94a3b8;">Expires: {st.session_state.subscription_expiry}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="sidebar-card">
                    <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:4px;">
                        <span style="color:#cbd5e1; font-weight:600;">Free Plan</span>
                        <span style="color:#c084fc; font-weight:700;">{remaining} / {FREE_MESSAGE_LIMIT} left</span>
                    </div>
                    <div style="font-size:0.72rem; color:#94a3b8;">
                        Used {st.session_state.messages_used} of {FREE_MESSAGE_LIMIT} free messages
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.progress(progress_val)

        if st.button("🎁 Claim Offer / Upgrade", use_container_width=True, type="primary", key="sb_claim_offer_btn"):
            st.session_state.active_view = "subscription"
            st.rerun()

        st.markdown("---")

        st.markdown(
            f"""
            <div class="sidebar-card" style="display:flex; align-items:center; gap:10px;">
                <div style="width:36px; height:36px; border-radius:50%; background:linear-gradient(135deg,#7c3aed,#2563eb);
                            display:flex; align-items:center; justify-content:center; font-weight:700; color:white;">
                    {st.session_state.student_name[0].upper()}
                </div>
                <div>
                    <div style="font-size:0.85rem; font-weight:700; color:#f8fafc;">{st.session_state.student_name}</div>
                    <div style="font-size:0.72rem; color:#94a3b8;">{st.session_state.selected_class} • Verified Student</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("🚪 Logout", use_container_width=True, key="sb_logout_btn"):
            st.session_state.authenticated = False
            st.rerun()


# ==============================================================================
# 8. JAZZCASH PAYMENT SECTION & PREMIUM SUBSCRIPTION VIEW
# ==============================================================================
def render_payment_section():
    st.markdown("---")
    st.markdown("## 💳 JazzCash Payment")

    st.info(
        "Choose your plan and contact the administrator "
        "for manual payment verification."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Weekly Plan")
        st.subheader("PKR 200")
        st.caption("7 Days Access")

    with col2:
        st.markdown("### Monthly Plan")
        st.subheader("PKR 500")
        st.caption("30 Days Access")

    st.divider()

    st.markdown("### 📱 Payment Details")

    # Replace these placeholders only with guardian-approved details.
    payment_number = JAZZCASH_NUMBER
    account_name = JAZZCASH_ACCOUNT_NAME

    st.write("**JazzCash Number:**", payment_number)
    st.write("**Account Name:**", account_name)

    st.warning(
        "Payment ke baad administrator se contact karein. "
        "Premium access sirf payment verify hone ke baad activate hoga."
    )

    st.caption(
        "Automatic payment gateway abhi connected nahi hai. "
        "Is app mein payment automatically process nahi hoti."
    )


def render_subscription_page(limit_reached: bool = False):
    if limit_reached:
        st.markdown(
            """
            <div class="welcome-card" style="border-color: rgba(244, 63, 94, 0.55); text-align: center;">
                <div style="font-size: 2.6rem; margin-bottom: 8px;">⏳</div>
                <h2 style="color: #fda4af; font-weight: 800; margin-bottom: 6px;">
                    You've reached your free usage limit.
                </h2>
                <p style="color: #cbd5e1; max-width: 620px; margin: 0 auto 14px auto; font-size: 0.96rem;">
                    You have used all <strong>10 free AI tutor messages</strong>. Claim our student offer below to unlock uninterrupted study assistance across all 10 subjects for Class 1 to Class 10.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="welcome-card" style="text-align: center;">
                <span class="popular-ribbon">🎁 Student Special Offer</span>
                <h2 class="welcome-title">Upgrade to Muhammad Abdullah School AI Pro</h2>
                <p style="color: #cbd5e1; max-width: 640px; margin: 0 auto; font-size: 0.95rem;">
                    Choose a flexible study pass tailored for school exams, daily homework help, and board preparation.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    status_col1, status_col2, status_col3 = st.columns(3)
    with status_col1:
        st.metric("Account Status", "Premium" if st.session_state.is_premium else "Free Tier")
    with status_col2:
        st.metric("Payment Status", "Verified" if st.session_state.is_premium else "Manual Verification Required")
    with status_col3:
        st.metric(
            "Subscription Expiry",
            st.session_state.subscription_expiry if st.session_state.subscription_expiry else "N/A (Free Limit: 10 Msgs)",
        )

    st.markdown("### 💎 Available Subscription Plans")
    col_weekly, col_monthly = st.columns(2, gap="large")

    with col_weekly:
        plan_w = SUBSCRIPTION_PLANS["weekly"]
        features_w_html = "".join([f"<li style='margin-bottom:8px; color:#cbd5e1;'>✅ {f}</li>" for f in plan_w["features"]])
        st.markdown(
            f"""
            <div class="pricing-card">
                <div style="font-size:0.8rem; color:#94a3b8; font-weight:700; text-transform:uppercase;">Starter Pass</div>
                <h3 style="margin:6px 0 0 0; color:#f8fafc; font-weight:700;">{plan_w['name']}</h3>
                <div class="price-tag">{plan_w['price']}</div>
                <div class="price-duration">🗓️ {plan_w['duration']}</div>
                <ul style="list-style:none; padding-left:0; margin-top:16px; font-size:0.9rem;">
                    {features_w_html}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Choose Weekly Plan (PKR 200)", use_container_width=True, key="choose_weekly_plan_btn"):
            st.session_state.pending_plan_choice = "Weekly Plan — PKR 200 (7 Days Access)"

    with col_monthly:
        plan_m = SUBSCRIPTION_PLANS["monthly"]
        features_m_html = "".join([f"<li style='margin-bottom:8px; color:#e2e8f0;'>✅ {f}</li>" for f in plan_m["features"]])
        st.markdown(
            f"""
            <div class="pricing-card-popular">
                <span class="popular-ribbon">⭐ Popular Plan</span>
                <h3 style="margin:4px 0 0 0; color:#ffffff; font-weight:800;">{plan_m['name']}</h3>
                <div class="price-tag">{plan_m['price']}</div>
                <div class="price-duration">🗓️ {plan_m['duration']} • Best Value</div>
                <ul style="list-style:none; padding-left:0; margin-top:16px; font-size:0.9rem;">
                    {features_m_html}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Choose Monthly Plan (PKR 500)", type="primary", use_container_width=True, key="choose_monthly_plan_btn"):
            st.session_state.pending_plan_choice = "Monthly Plan — PKR 500 (30 Days Access)"

    if st.session_state.pending_plan_choice:
        st.success(f"✅ **Selected Plan:** {st.session_state.pending_plan_choice} — Neeche diye gaye JazzCash details par payment bhej kar administrator se verify karwayein.")

    # Merged JazzCash Payment Section
    render_payment_section()

    st.markdown("<br>", unsafe_allow_html=True)
    if not limit_reached:
        if st.button("⬅️ Back to Study Chat", key="back_to_chat_from_sub_btn"):
            st.session_state.active_view = "chat"
            st.rerun()


# ==============================================================================
# 9. STUDENT DASHBOARD VIEW
# ==============================================================================
def render_student_dashboard():
    st.markdown(
        f"""
        <div class="welcome-card">
            <h2 class="welcome-title">📊 Student Learning Dashboard</h2>
            <p style="color:#cbd5e1; margin:0;">
                Welcome back, <strong>{st.session_state.student_name}</strong>! Track your study sessions, active grade level, and account status.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    total_chats = len(st.session_state.chats)
    total_messages = sum(len(c.get("messages", [])) for c in st.session_state.chats.values())
    remaining = max(0, FREE_MESSAGE_LIMIT - st.session_state.messages_used)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Active Class", st.session_state.selected_class)
    with m2:
        st.metric("Saved Study Chats", total_chats)
    with m3:
        st.metric("Total Messages Exchanged", total_messages)
    with m4:
        st.metric("Free Messages Remaining", "Unlimited" if st.session_state.is_premium else f"{remaining} / {FREE_MESSAGE_LIMIT}")

    st.markdown("### 📚 Curriculum Subjects Overview")
    cols = st.columns(5)
    for idx, (subj, icon) in enumerate(SUBJECTS.items()):
        with cols[idx % 5]:
            st.markdown(
                f"""
                <div class="sidebar-card" style="text-align:center; padding:16px 10px;">
                    <div style="font-size:1.7rem;">{icon}</div>
                    <div style="font-size:0.85rem; font-weight:700; color:#f1f5f9; margin-top:6px;">{subj}</div>
                    <div style="font-size:0.72rem; color:#94a3b8;">Class 1 – 10</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if st.button("💬 Return to AI Tutor Chat", type="primary", key="dash_return_chat_btn"):
        st.session_state.active_view = "chat"
        st.rerun()


# ==============================================================================
# 10. MAIN CHATBOT INTERFACE
# ==============================================================================
def render_chat_interface():
    if (not st.session_state.is_premium) and (st.session_state.messages_used >= FREE_MESSAGE_LIMIT):
        render_subscription_page(limit_reached=True)
        return

    current_chat = st.session_state.chats.get(st.session_state.current_chat_id)
    if not current_chat:
        create_new_chat(switch=True)
        current_chat = st.session_state.chats[st.session_state.current_chat_id]

    subj_icon = SUBJECTS.get(st.session_state.selected_subject, "📚")
    remaining = max(0, FREE_MESSAGE_LIMIT - st.session_state.messages_used)

    top_col1, top_col2 = st.columns([3.5, 1.2])
    with top_col1:
        st.markdown(
            f"""
            <div class="context-banner">
                <div>
                    <span class="badge-pill badge-class">🎓 {st.session_state.selected_class}</span>
                    <span class="badge-pill badge-subject">{subj_icon} {st.session_state.selected_subject}</span>
                    <span class="badge-pill badge-status">● AI Tutor Online</span>
                </div>
                <div style="font-size:0.8rem; color:#94a3b8;">
                    Free Credits Left: <strong style="color:#c084fc;">{remaining}/{FREE_MESSAGE_LIMIT}</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_col2:
        act_c1, act_c2 = st.columns(2)
        with act_c1:
            if st.button("🧹 Clear", use_container_width=True, help="Clear current conversation", key="clear_current_chat_btn"):
                current_chat["messages"] = []
                current_chat["title"] = "New Study Session"
                save_chats_to_disk(st.session_state.chats)
                st.rerun()
        with act_c2:
            if st.button("➕ New", use_container_width=True, help="Start fresh chat", key="top_new_chat_btn"):
                create_new_chat(switch=True)
                st.rerun()

    if not current_chat["messages"]:
        st.markdown(
            f"""
            <div class="welcome-card">
                <div class="welcome-title">Assalam-o-Alaikum, {st.session_state.student_name}! 👋</div>
                <p style="color:#cbd5e1; font-size:0.98rem; line-height:1.6; margin-bottom:16px;">
                    Welcome to <strong>{APP_TITLE}</strong>. You are currently studying
                    <strong>{subj_icon} {st.session_state.selected_subject}</strong> for <strong>{st.session_state.selected_class}</strong>.
                    Say <em>"Hello, kya hal hai?"</em> or ask any concept, homework problem, or exam question below!
                </p>
                <div style="font-size:0.82rem; color:#93c5fd; font-weight:600;">
                    ✨ Try a quick starter prompt below or type your own question at the bottom:
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        starter_prompts = {
            "Mathematics": ["Hello! Kya hal hai?", "Explain Pythagoras Theorem with example", "Solve 25 * 4 + 18"],
            "Physics": ["Hi! Kaisi ho?", "State Newton's Three Laws of Motion", "Explain Ohm's Law (V = IR)"],
            "Chemistry": ["Hello! Kya hal hai?", "Describe the structure of an atom", "Explain Acids, Bases, and pH scale"],
            "Biology": ["Hi! Kaisi ho?", "Explain the structure of a Cell", "Write the equation of Photosynthesis"],
            "Computer Science": ["Hello! Kya hal hai?", "What are the main parts of a CPU?", "Explain Binary Number System"],
            "English": ["Hello! How are you?", "Explain the 8 Parts of Speech", "Give a quick guide to English Tenses"],
            "Urdu": ["السلام علیکم! کیا حال ہے؟", "کلمہ کی اقسام بیان کریں (اسم، فعل، حرف)", "مضمون نویسی کے اہم اصول کیا ہیں؟"],
            "Islamic Studies": ["Assalam-o-Alaikum! Kya hal hai?", "Explain the Five Pillars of Islam", "What is the significance of Zakat?"],
            "Pakistan Studies": ["Hello! Kya hal hai?", "Explain the Lahore Resolution 1940", "Key features of the 1973 Constitution"],
            "General Knowledge": ["Hi! Kaisi ho?", "List all 8 planets of our Solar System", "Important scientific inventions"],
        }
        suggestions = starter_prompts.get(st.session_state.selected_subject, starter_prompts["General Knowledge"])

        s_cols = st.columns(3)
        for i, suggestion in enumerate(suggestions):
            with s_cols[i]:
                if st.button(f"💡 {suggestion}", use_container_width=True, key=f"starter_prompt_{i}"):
                    process_user_message(suggestion, current_chat)
                    st.rerun()

    for idx, msg in enumerate(current_chat["messages"]):
        role = msg["role"]
        avatar = "🧑‍🎓" if role == "user" else "🤖"
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg["content"])
            if role == "assistant":
                c_time, c_copy = st.columns([4, 1])
                with c_time:
                    st.caption(f"🕒 {msg.get('timestamp', '')} • {msg.get('class', st.session_state.selected_class)} • {msg.get('subject', st.session_state.selected_subject)}")
                with c_copy:
                    if st.button("📋 Copy", key=f"copy_btn_{current_chat['id']}_{idx}", use_container_width=True):
                        st.session_state.copied_msg_id = f"{current_chat['id']}_{idx}"

                if st.session_state.copied_msg_id == f"{current_chat['id']}_{idx}":
                    st.code(msg["content"], language="markdown")

    user_input = st.chat_input(
        f"Say Hello or Ask {APP_TITLE} ({st.session_state.selected_class} • {st.session_state.selected_subject})..."
    )

    if user_input and user_input.strip():
        process_user_message(user_input.strip(), current_chat)
        st.rerun()


def process_user_message(prompt_text: str, current_chat: Dict[str, Any]):
    if (not st.session_state.is_premium) and (st.session_state.messages_used >= FREE_MESSAGE_LIMIT):
        st.session_state.active_view = "subscription"
        return

    now_str = datetime.datetime.now().strftime("%I:%M %p")

    if not current_chat["messages"]:
        clean_title = prompt_text[:38] + ("..." if len(prompt_text) > 38 else "")
        current_chat["title"] = clean_title

    current_chat["messages"].append(
        {
            "role": "user",
            "content": prompt_text,
            "timestamp": now_str,
            "class": st.session_state.selected_class,
            "subject": st.session_state.selected_subject,
        }
    )

    with st.spinner("🤖 Thinking & preparing your reply..."):
        time.sleep(0.35)
        ai_reply = generate_educational_response(
            user_prompt=prompt_text,
            selected_class=st.session_state.selected_class,
            selected_subject=st.session_state.selected_subject,
        )

    current_chat["messages"].append(
        {
            "role": "assistant",
            "content": ai_reply,
            "timestamp": now_str,
            "class": st.session_state.selected_class,
            "subject": st.session_state.selected_subject,
        }
    )

    current_chat["updated_at"] = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    st.session_state.messages_used += 1
    save_chats_to_disk(st.session_state.chats)


# ==============================================================================
# 11. MAIN ENTRY POINT
# ==============================================================================
def main():
    inject_custom_css()
    init_session_state()

    if not st.session_state.authenticated:
        render_login_page()
        return

    render_sidebar()

    if st.session_state.active_view == "subscription":
        limit_reached = (not st.session_state.is_premium) and (st.session_state.messages_used >= FREE_MESSAGE_LIMIT)
        render_subscription_page(limit_reached=limit_reached)
    elif st.session_state.active_view == "dashboard":
        render_student_dashboard()
    else:
        render_chat_interface()

    st.markdown(
        f"""
        <div class="custom-footer">
            <strong>{APP_TITLE}</strong> • Empowering Students from Class 1 to Class 10 across All Core Subjects • Built with Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
