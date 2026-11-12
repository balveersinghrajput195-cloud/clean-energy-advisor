import os
from uuid import uuid4

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from streamlit.errors import StreamlitSecretNotFoundError


load_dotenv()

st.set_page_config(
    page_title="Clean Energy Advisor",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #e8f4ec;
        --muted: #9bb5a4;
        --green: #41d98a;
        --green-bright: #83f0a8;
        --panel: rgba(15, 36, 27, 0.78);
        --line: rgba(172, 225, 190, 0.12);
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        color: var(--ink);
        background:
            radial-gradient(ellipse at 82% 4%, rgba(28, 111, 69, 0.22), transparent 34%),
            radial-gradient(ellipse at 8% 82%, rgba(24, 92, 63, 0.16), transparent 38%),
            #07130f;
    }

    [data-testid="stAppViewContainer"] {
        background: transparent;
    }

    [data-testid="stHeader"] {
        background: rgba(7, 19, 15, 0.74);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 28, 20, 0.98), rgba(7, 20, 15, 0.98));
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.35rem;
    }

    [data-testid="stMain"] .block-container {
        max-width: 1120px;
        padding: 2rem 2rem 7rem;
    }

    h1, h2, h3, .brand-name {
        font-family: 'Manrope', sans-serif;
        letter-spacing: -0.035em;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 0.15rem 0 1.65rem;
    }

    .brand-mark {
        display: grid;
        place-items: center;
        width: 43px;
        height: 43px;
        border: 1px solid rgba(131, 240, 168, 0.32);
        border-radius: 15px;
        background: linear-gradient(145deg, rgba(65, 217, 138, 0.2), rgba(31, 98, 63, 0.2));
        box-shadow: 0 8px 26px rgba(37, 197, 112, 0.12);
        font-size: 22px;
    }

    .brand-name {
        color: #effbf2;
        font-size: 15px;
        font-weight: 800;
        line-height: 1.2;
    }

    .brand-caption, .eyebrow {
        color: var(--muted);
        font-size: 11px;
        letter-spacing: 0.13em;
        text-transform: uppercase;
    }

    .sidebar-label {
        margin: 1.4rem 0 0.55rem;
        color: #789685;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .sidebar-copy {
        padding: 0.8rem 0.9rem;
        border: 1px solid var(--line);
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.025);
        color: #a9c1b2;
        font-size: 12px;
        line-height: 1.65;
    }

    [data-testid="stSidebar"] [data-testid="stButton"] > button {
        min-height: 2.45rem;
        padding: 0.55rem 0.8rem;
        border: 1px solid rgba(172, 225, 190, 0.11);
        border-radius: 11px;
        background: rgba(255, 255, 255, 0.035);
        color: #d6e8dc;
        font-size: 12px;
        text-align: left;
        transition: all 160ms ease;
    }

    [data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
        border-color: rgba(65, 217, 138, 0.42);
        background: rgba(65, 217, 138, 0.09);
        color: #f3fff6;
        transform: translateY(-1px);
    }

    [data-testid="stSidebar"] button[kind="primary"] {
        border: 1px solid rgba(106, 235, 155, 0.45);
        background: linear-gradient(135deg, #1d9e5e, #147748);
        color: white;
        font-weight: 700;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: clamp(1.7rem, 5vw, 3.4rem);
        border: 1px solid rgba(166, 231, 184, 0.16);
        border-radius: 26px;
        background:
            radial-gradient(circle at 84% 46%, rgba(80, 208, 126, 0.16), transparent 27%),
            linear-gradient(125deg, rgba(15, 43, 30, 0.94), rgba(11, 30, 23, 0.83));
        box-shadow: 0 24px 80px rgba(0, 0, 0, 0.2), inset 0 1px rgba(255, 255, 255, 0.035);
        animation: rise-in 500ms ease both;
    }

    .hero h1 {
        max-width: 640px;
        margin: 0.8rem 0 0.75rem;
        color: #f1fff5;
        font-size: clamp(2.15rem, 5vw, 3.7rem);
        font-weight: 800;
        line-height: 1.08;
    }

    .hero h1 span {
        color: var(--green-bright);
    }

    .hero p {
        max-width: 550px;
        margin: 0;
        color: #aec8b8;
        font-size: clamp(14px, 1.5vw, 17px);
        line-height: 1.7;
    }

    .hero-art {
        position: absolute;
        top: 50%;
        right: 7%;
        display: grid;
        width: 185px;
        height: 185px;
        place-items: center;
        border: 1px solid rgba(147, 235, 170, 0.17);
        border-radius: 50%;
        background: radial-gradient(circle, rgba(67, 195, 115, 0.18), rgba(36, 105, 68, 0.04) 67%);
        transform: translateY(-50%);
        font-size: 74px;
        filter: drop-shadow(0 10px 24px rgba(81, 224, 134, 0.18));
    }

    .hero-art::before, .hero-art::after {
        position: absolute;
        border: 1px solid rgba(154, 231, 171, 0.13);
        border-radius: 50%;
        content: "";
    }

    .hero-art::before { inset: -18px; }
    .hero-art::after { inset: 20px; }

    .section-heading {
        margin: 2rem 0 0.25rem;
        color: #e9f7ed;
        font-family: 'Manrope', sans-serif;
        font-size: 19px;
        font-weight: 700;
        letter-spacing: -0.03em;
    }

    .section-subtitle {
        margin: 0 0 0.9rem;
        color: #92ae9d;
        font-size: 13px;
    }

    [data-testid="stMain"] [data-testid="stButton"] > button {
        min-height: 104px;
        padding: 1rem 1.1rem;
        border: 1px solid rgba(164, 222, 181, 0.15);
        border-radius: 17px;
        background:
            linear-gradient(145deg, rgba(20, 49, 34, 0.8), rgba(12, 31, 23, 0.88));
        color: #eaf8ee;
        font-size: 14px;
        font-weight: 700;
        line-height: 1.65;
        text-align: left;
        white-space: pre-wrap;
        transition: transform 180ms ease, border-color 180ms ease, background 180ms ease, box-shadow 180ms ease;
    }

    [data-testid="stMain"] [data-testid="stButton"] > button:hover {
        transform: translateY(-3px);
        border-color: rgba(93, 227, 144, 0.48);
        background: linear-gradient(145deg, rgba(27, 72, 46, 0.9), rgba(14, 42, 29, 0.95));
        box-shadow: 0 12px 30px rgba(21, 143, 78, 0.12);
        color: #f5fff7;
    }

    [data-testid="stChatMessage"] {
        margin: 0.65rem 0;
        padding: 1rem 1.15rem;
        border: 1px solid var(--line);
        border-radius: 18px;
        background: rgba(13, 33, 24, 0.72);
        animation: rise-in 260ms ease both;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        border-color: rgba(77, 177, 127, 0.19);
        background: rgba(18, 53, 36, 0.72);
    }

    [data-testid="stChatInput"] {
        border: 1px solid rgba(127, 216, 154, 0.2);
        border-radius: 18px;
        background: rgba(11, 29, 21, 0.96);
        box-shadow: 0 14px 40px rgba(0, 0, 0, 0.28);
    }

    [data-testid="stChatInput"] textarea {
        color: #effaf2;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #799987;
    }

    [data-testid="stChatInput"] button {
        color: #8bf0ad !important;
    }

    .fine-print {
        margin-top: 0.6rem;
        color: #708c7b;
        font-size: 11px;
        text-align: center;
    }

    @keyframes rise-in {
        from { opacity: 0; transform: translateY(9px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @media (max-width: 760px) {
        [data-testid="stMain"] .block-container {
            padding: 1rem 1rem 6.5rem;
        }

        .hero {
            border-radius: 21px;
        }

        .hero-art {
            top: 20px;
            right: 12px;
            width: 80px;
            height: 80px;
            opacity: 0.65;
            transform: none;
            font-size: 38px;
        }

        .hero h1 {
            max-width: 82%;
            font-size: clamp(2rem, 9vw, 3rem);
        }

        [data-testid="stMain"] [data-testid="stButton"] > button {
            min-height: 84px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_api_key() -> str | None:
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key

    try:
        return st.secrets.get("GEMINI_API_KEY")
    except StreamlitSecretNotFoundError:
        return None


def start_new_chat() -> None:
    chat_id = uuid4().hex
    st.session_state.chats[chat_id] = {"title": "New conversation", "messages": [], "error": None}
    st.session_state.active_chat_id = chat_id


if "chats" not in st.session_state:
    initial_chat_id = uuid4().hex
    st.session_state.chats = {
        initial_chat_id: {"title": "New conversation", "messages": [], "error": None}
    }
    st.session_state.active_chat_id = initial_chat_id

sidebar_prompt = None

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">🌱</div>
            <div>
                <div class="brand-name">Clean Energy<br>Advisor</div>
                <div class="brand-caption">Intelligence for a greener world</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("＋  New chat", type="primary", use_container_width=True):
        start_new_chat()

    st.markdown('<div class="sidebar-label">Your conversations</div>', unsafe_allow_html=True)
    for chat_id, chat_data in reversed(list(st.session_state.chats.items())):
        title = chat_data["title"]
        if st.button(f"◌  {title}", key=f"history-{chat_id}", use_container_width=True):
            st.session_state.active_chat_id = chat_id

    active_chat = st.session_state.chats[st.session_state.active_chat_id]
    if st.button("⌫  Clear current chat", use_container_width=True):
        active_chat["messages"] = []
        active_chat["title"] = "New conversation"
        active_chat["error"] = None

    st.markdown('<div class="sidebar-label">Explore clean energy</div>', unsafe_allow_html=True)
    topics = [
        ("☀️  Solar energy", "How can I choose the right solar energy system for my home?"),
        ("🌬️  Wind power", "How does wind energy work, and where is it most effective?"),
        ("🚗  Electric vehicles", "What should I know before switching to an electric vehicle?"),
        ("🌍  Sustainability", "How can I measure and reduce my personal carbon footprint?"),
    ]
    for label, question in topics:
        if st.button(label, key=f"topic-{label}", use_container_width=True):
            sidebar_prompt = question

    st.markdown('<div class="sidebar-label">About</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-copy">A thoughtful AI companion for practical renewable energy, '
        'efficiency, and sustainable-living decisions. Powered by Google Gemini.</div>',
        unsafe_allow_html=True,
    )

active_chat = st.session_state.chats[st.session_state.active_chat_id]
api_key = load_api_key()
client = genai.Client(api_key=api_key) if api_key else None

if not active_chat["messages"]:
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">A brighter future starts with a better question</div>
            <h1>Your Personal<br><span>Clean Energy Assistant</span></h1>
            <p>Explore smarter ways to build a sustainable future. Get clear, practical guidance
            for the energy choices that matter to you.</p>
            <div class="hero-art" aria-hidden="true">🌿</div>
        </div>
        <div class="section-heading">Explore a topic</div>
        <div class="section-subtitle">Choose a starting point or ask your own question below.</div>
        """,
        unsafe_allow_html=True,
    )
    suggestions = [
        ("☀️  Solar Energy\nUnderstand panels, savings & incentives",
         "How can I choose the right solar energy system for my home?"),
        ("🌬️  Wind Energy\nDiscover clean power from the wind",
         "How does wind energy work, and where is it most effective?"),
        ("🚗  Electric Vehicles\nCompare charging, range & ownership",
         "What should I know before switching to an electric vehicle?"),
        ("🌍  Sustainability & Carbon Footprint\nFind practical ways to make an impact",
         "How can I measure and reduce my personal carbon footprint?"),
    ]
    suggestion_columns = st.columns(4)
    card_prompt = None
    for column, (label, question), index in zip(
        suggestion_columns, suggestions, range(len(suggestions))
    ):
        with column:
            if st.button(label, key=f"suggestion-{index}", use_container_width=True):
                card_prompt = question
else:
    card_prompt = None

user_question = st.chat_input("Ask anything about clean energy...")
user_question = sidebar_prompt or card_prompt or user_question

if user_question:
    active_chat["error"] = None
    active_chat["messages"].append({"role": "user", "content": user_question})
    if active_chat["title"] == "New conversation":
        active_chat["title"] = user_question.strip().replace("\n", " ")[:36]
        if len(user_question.strip()) > 36:
            active_chat["title"] += "…"

    if client is None:
        active_chat["error"] = "Configure GEMINI_API_KEY in Streamlit Cloud Secrets or your local .env file."
    else:
        with st.spinner("Finding a thoughtful answer..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=user_question,
                    config=types.GenerateContentConfig(
                        system_instruction=(
                            "You are Clean Energy Advisor, an expert AI guide dedicated to renewable energy, "
                            "energy efficiency, energy conservation, and sustainable choices. "
                            "Answer questions clearly, accurately, and helpfully."
                        )
                    ),
                )
                if not response.text:
                    raise ValueError("Gemini returned an empty response.")
                active_chat["messages"].append(
                    {"role": "assistant", "content": response.text}
                )
            except Exception as error:
                active_chat["error"] = f"Error generating response: {error}"
    st.rerun()

for message in active_chat["messages"]:
    avatar = "🧑" if message["role"] == "user" else "🌱"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if active_chat["error"]:
    st.error(active_chat["error"])

if not api_key:
    st.markdown(
        '<div class="fine-print">Add GEMINI_API_KEY to Streamlit Cloud Secrets or a local .env file to start chatting.</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="fine-print">AI can make mistakes. Verify important energy, financial, and safety decisions.</div>',
        unsafe_allow_html=True,
    )
