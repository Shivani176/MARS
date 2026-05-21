"""
MARS - Memory-Augmented Research System
UI v4 — single column, logo always at top, warm palette
"""

import streamlit as st
import sys, os, time
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from main import execute_routed_query, memory_manager, chat_history
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.stop()

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MARS",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600&family=DM+Sans:wght@300;400;500&display=swap');

/* global background */
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #4a2e18 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="block-container"] {
    max-width: 860px !important;
    padding: 0 1.5rem 2rem !important;
}

/* hide chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
.stDeployButton { display: none !important; }

/* ── HEADER STRIP (always rendered) ── */
.mars-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 0 16px;
    border-bottom: 0.5px solid #2e1a0c;
    margin-bottom: 20px;
}
.mars-logo-left {
    display: flex;
    align-items: center;
    gap: 14px;
}
.planet-sm {
    width: 46px;
    height: 46px;
    border-radius: 50%;
    background: radial-gradient(circle at 37% 37%,
        #f5a862 0%, #c05828 50%, #5c1e08 87%);
    border: 2px solid #904020;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 22px rgba(190,75,20,0.45),
                0 0 8px rgba(245,140,60,0.2);
    flex-shrink: 0;
}
.planet-sm-m {
    font-family: 'Cinzel', serif;
    font-size: 20px;
    font-weight: 600;
    color: #feebd0;
    line-height: 1;
}
.mars-logo-text { line-height: 1; }
.mars-logo-name {
    font-family: 'Cinzel', serif;
    font-size: 20px;
    font-weight: 600;
    color: #f0a070;
    letter-spacing: 5px;
    display: block;
}
.mars-logo-sub {
    font-size: 13px;
    color: #f4c09a;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    display: block;
    margin-top: 3px;
}


/* ── WELCOME ── */
.welcome-big {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 0 32px;
    gap: 12px;
    text-align: center;
}
.planet-lg {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: radial-gradient(circle at 37% 37%,
        #f5a862 0%, #c05828 50%, #5c1e08 87%);
    border: 2px solid #904020;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 44px rgba(190,75,20,0.4),
                0 0 14px rgba(245,140,60,0.2);
    margin-bottom: 4px;
}
.planet-lg-m {
    font-family: 'Cinzel', serif;
    font-size: 34px;
    font-weight: 600;
    color: #feebd0;
}
.welcome-title {
    font-family: 'Cinzel', serif;
    font-size: 30px;
    font-weight: 600;
    color: #f0a070;
    letter-spacing: 8px;
}
.welcome-sub {
    font-size: 18px;
    color: #e8d5c0;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    margin-top: 2px;
}

.welcome-desc {
    font-size: 16px;
    color: #d4b090;
    line-height: 2;
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    margin-top: 8px;
    letter-spacing: 0.3px;
}
.chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 12px;
}
.chip {
    font-size: 11px;
    padding: 5px 14px;
    border-radius: 20px;
    background: #1a0e06;
    color: #8a5838;
    border: 0.5px solid #2e1a0c;
    font-family: 'DM Sans', sans-serif;
}

/* ── MESSAGES ── */
.day-divider {
    text-align: center;
    font-size: 10px;
    color: #3a2010;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 4px 0 12px;
    font-family: 'DM Sans', sans-serif;
}
.msg-user {
    display: flex;
    justify-content: flex-end;
    align-items: flex-start;
    gap: 9px;
    margin: 6px 0;
}
.msg-mars {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    gap: 9px;
    margin: 6px 0;
}
.bubble-user {
    background: #1c1008;
    color: #e0c0a0;
    border: 0.5px solid #2e1a0c;
    border-radius: 14px 4px 14px 14px;
    padding: 10px 14px;
    font-size: 13px;
    line-height: 1.6;
    max-width: 75%;
    white-space: pre-wrap;
    word-break: break-word;
    font-family: 'DM Sans', sans-serif;
}
.bubble-mars {
    background: #160c06;
    color: #b08060;
    border: 0.5px solid #241408;
    border-radius: 4px 14px 14px 14px;
    padding: 10px 14px;
    font-size: 13px;
    line-height: 1.7;
    max-width: 85%;
    white-space: pre-wrap;
    word-break: break-word;
    font-family: 'DM Sans', sans-serif;
}
.av {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 500;
    flex-shrink: 0;
    font-family: 'DM Sans', sans-serif;
}
.av-m { background:#1e0e06; color:#d07848; border:0.5px solid #4a2410; }
.av-u { background:#180e08; color:#6a4028; border:0.5px solid #2e1808; }
.qtag {
    display: inline-block;
    font-size: 9.5px;
    padding: 2px 8px;
    border-radius: 4px;
    margin-bottom: 6px;
    background: #1e0e06;
    color: #d07848;
    border: 0.5px solid #4a2410;
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 0.3px;
}

/* ── INPUT ── */
.stTextInput > div > div > input {
    background-color: #1c1008 !important;
    border: 0.5px solid #3a1e0c !important;
    border-radius: 10px !important;
    color: #e0c0a0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    caret-color: #d07848 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7a3a18 !important;
    box-shadow: 0 0 0 2px rgba(180,80,30,0.18) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder {
    color: #3a2010 !important;
}
.stFormSubmitButton > button {
    background: #7a4020 !important;
    color: #f4c09a !important;
    border: 0.5px solid #a05030 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    height: 42px !important;
}
.stFormSubmitButton > button:hover {
    background: #a05030 !important;
    border-color: #d07848 !important;
}

/* misc streamlit widgets */
.stSelectbox label,
.stCheckbox label { color: #5a3622 !important; font-size:12px !important; }
.stSelectbox > div > div {
    background: #1c1008 !important;
    border: 0.5px solid #3a1e0c !important;
    border-radius: 8px !important;
    color: #9a6848 !important;
}
.stButton > button {
    background: transparent !important;
    border: 0.5px solid #2e1a0c !important;
    color: #4a2e1a !important;
    font-size: 11px !important;
    border-radius: 8px !important;
}
.stButton > button:hover {
    background: #1a0e06 !important;
    color: #7a4828 !important;
}
.stProgress > div > div > div { background-color: #c06030 !important; }
div[data-testid="stAlert"] {
    background: #1a0e06 !important;
    border: 0.5px solid #4a2410 !important;
    border-radius: 8px !important;
}
div[data-testid="stAlert"] p { color: #9a6848 !important; }
[data-testid="stCaptionContainer"] p {
    color: #3a2010 !important;
    font-size: 11px !important;
}
hr { border-color: #2e1a0c !important; margin: 8px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for k, v in [("messages",[]),("action_log",[]),
             ("show_traces",False),("model_name","Claude 3.5 Sonnet")]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── STATS ─────────────────────────────────────────────────────────────────────
try:
    stats        = memory_manager.get_stats()
    papers_count = stats.get("papers", 0)
    convs_count  = stats.get("conversations", 0)
except:
    papers_count = 0
    convs_count  = 0

# ── QUERY TAG ─────────────────────────────────────────────────────────────────
def get_qtag(content):
    c = content.lower()
    if any(w in c for w in ["found","hybrid","arxiv","result","database"]): return "Database Search"
    if any(w in c for w in ["semantic","similarity","bridge","connection"]):  return "Semantic Analysis"
    if any(w in c for w in ["bibtex","exported",".bib"]):                    return "BibTeX Export"
    if any(w in c for w in ["literature review","synthesis","section"]):     return "Literature Review"
    if any(w in c for w in ["saved","written","file"]):                      return "File Save"
    return "MARS"

# ════════════════════════════════════════════════════════════════════════════════
#  HEADER — always rendered first, never disappears
# ════════════════════════════════════════════════════════════════════════════════
current_topic = "Ready to explore"
for msg in reversed(st.session_state.messages):
    if msg["role"] == "user":
        q = msg["content"]
        current_topic = q[:54] + ("…" if len(q) > 54 else "")
        break

st.markdown(f"""
<div class="mars-header">
    <div class="mars-logo-left">
        <div class="planet-sm">
            <span class="planet-sm-m">M</span>
        </div>
        <div class="mars-logo-text">
            <span class="mars-logo-name">MARS</span>
            <span class="mars-logo-sub">Memory-Augmented Research System</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
#  WELCOME or CHAT
# ════════════════════════════════════════════════════════════════════════════════
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="welcome-big">
        <div class="planet-lg">
            <span class="planet-lg-m">M</span>
        </div>
        <div class="welcome-title">MARS</div>
        <div class="welcome-sub">Memory-Augmented Research System</div>
        <div class="welcome-desc">
            Your intelligent research companion.<br>
            Search papers, map connections, generate reviews.
        </div>
        <div class="chips">
            <span class="chip">Search papers</span>
            <span class="chip">Semantic connections</span>
            <span class="chip">Research bridges</span>
            <span class="chip">Literature review</span>
            <span class="chip">Export BibTeX</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div class="day-divider">Today</div>', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        safe = (msg["content"]
                .replace("&","&amp;")
                .replace("<","&lt;")
                .replace(">","&gt;"))
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-user">
                <div class="bubble-user">{safe}</div>
                <div class="av av-u">S</div>
            </div>""", unsafe_allow_html=True)
        else:
            tag = get_qtag(msg["content"])
            st.markdown(f"""
            <div class="msg-mars">
                <div class="av av-m">M</div>
                <div class="bubble-mars">
                    <span class="qtag">{tag}</span><br>{safe}
                </div>
            </div>""", unsafe_allow_html=True)

    if st.session_state.show_traces and st.session_state.action_log:
        with st.expander("Traces", expanded=False):
            for t in st.session_state.action_log[-5:]:
                st.code(t, language=None)

# ── INPUT ─────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    c1, c2 = st.columns([6, 1])
    with c1:
        user_input = st.text_input(
            "msg",
            placeholder="Ask MARS anything about your research…",
            label_visibility="collapsed"
        )
    with c2:
        submit = st.form_submit_button("Send →", use_container_width=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
f1, f2, f3 = st.columns(3)
with f1: st.caption(f"Papers: {papers_count}")
with f2: st.caption(f"Model: {st.session_state.model_name}")
with f3: st.caption(datetime.now().strftime("%b %d, %Y"))

# ── PROCESS ───────────────────────────────────────────────────────────────────
if submit and user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.action_log.append(f"[{ts}] User: {user_input[:60]}")

    ph = st.empty()
    pb = st.progress(0)
    u  = user_input.lower()

    if any(w in u for w in ["literature review","synthesis"]):
        ph.info("Generating literature review — may take 30–60 s."); pb.progress(10)
    elif any(w in u for w in ["semantic","bridge","connection"]):
        ph.info("Running semantic analysis…"); pb.progress(15)
    elif any(w in u for w in ["export","bibtex"]):
        ph.info("Preparing BibTeX export…"); pb.progress(20)
    elif any(w in u for w in ["search","find","papers"]):
        ph.info("Searching papers…"); pb.progress(25)
    else:
        ph.info("Processing…"); pb.progress(30)

    try:
        pb.progress(50)
        response = execute_routed_query(user_input)
        pb.progress(100)
        ph.success("Done"); time.sleep(0.35); ph.empty(); pb.empty()

        if isinstance(response, dict):
            reply = response.get("output","")
            if isinstance(reply, list):
                parts = [item.get("text", item.get("content",""))
                         for item in reply if isinstance(item, dict)]
                reply = "\n\n".join(parts) if parts else str(reply)
            if not reply:
                reply = str(response)
        else:
            reply = str(response)

        if len(reply) > 10000:
            reply = reply[:10000] + "\n\n… (truncated — full output in terminal)"

        st.session_state.messages.append({"role":"assistant","content":reply})
        st.session_state.action_log.append(f"[{ts}] Assistant: {len(reply)} chars")

    except Exception as e:
        err = f"Error: {str(e)}"
        st.session_state.messages.append({"role":"assistant","content":err})
        st.session_state.action_log.append(f"[{ts}] Error: {str(e)}")
        ph.empty(); pb.empty()

    st.rerun()

























# """
# Streamlit UI for Research Assistant
# Clean, modern interface matching the design mockup
# """

# import streamlit as st
# import sys
# import os
# from datetime import datetime

# # Add project directory to path (works from any location)
# current_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, current_dir)

# # Import your existing system
# try:
#     from main import execute_routed_query, memory_manager, chat_history
# except ImportError as e:
#     st.error(f"❌ Import Error: {e}")
#     st.error("Make sure app_ui.py is in the same directory as main.py, tools.py, and memory_manager.py")
#     st.stop()

# # ============ PAGE CONFIG ============
# st.set_page_config(
#     page_title="Research Assistant",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded",
#     menu_items=None
# )

# # ============ CUSTOM CSS ============
# st.markdown("""
# <style>
#     /* Modern Blue Theme - Main App */
#     .stApp {
#         background: linear-gradient(135deg, #e8f4ff 0%, #d6eaff 100%);
#     }
    
#     /* Sidebar - Clean Blue */
#     section[data-testid="stSidebar"] {
#         background: linear-gradient(180deg, #2563eb 0%, #1e40af 100%);
#         padding: 1.5rem 1rem;
#     }
    
#     section[data-testid="stSidebar"] > div {
#         background: transparent;
#     }
    
#     /* Sidebar text - Force white */
#     section[data-testid="stSidebar"] * {
#         color: white !important;
#     }
    
#     section[data-testid="stSidebar"] h1,
#     section[data-testid="stSidebar"] h2, 
#     section[data-testid="stSidebar"] h3 {
#         color: #93c5fd !important;
#     }
    
#     /* User messages - Light Blue (RIGHT) */
#     .user-message {
#         background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
#         padding: 14px 18px;
#         border-radius: 20px;
#         margin: 10px 0;
#         max-width: 70%;
#         float: right;
#         clear: both;
#         color: #1e3a8a;
#         box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
#     }
    
#     /* Assistant messages - Blue (LEFT) */
#     .assistant-message {
#         background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
#         padding: 14px 18px;
#         border-radius: 20px;
#         margin: 10px 0;
#         max-width: 70%;
#         float: left;
#         clear: both;
#         color: white;
#         box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
#     }
    
#     .message-container::after {
#         content: "";
#         display: table;
#         clear: both;
#     }
    
#     /* Input and buttons */
#     .stTextInput input {
#         border: 2px solid #3b82f6;
#         border-radius: 10px;
#         padding: 10px;
#     }
    
#     .stButton button {
#         background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
#         color: white;
#         border: none;
#         border-radius: 10px;
#         padding: 10px 24px;
#         font-weight: 600;
#     }
    
#     .stButton button:hover {
#         background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
#         transform: translateY(-1px);
#     }
    
#     /* Progress indicators */
#     .stProgress > div > div {
#         background-color: #3b82f6;
#     }
    
#     /* Info/Success boxes */
#     .stInfo {
#         background-color: #dbeafe;
#         color: #1e40af;
#         border-left: 4px solid #3b82f6;
#     }
    
#     .stSuccess {
#         background-color: #dcfce7;
#         color: #166534;
#         border-left: 4px solid #22c55e;
#     }
    
#     /* Hide branding */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
            
    

    
#     /* Title */
#     .main-title {
#         text-align: center;
#         color: #1e3a8a;
#         font-size: 2.5rem;
#         font-weight: 700;
#         margin-bottom: 0.5rem;
#     }
    
#     .subtitle {
#         text-align: center;
#         color: #3b82f6;
#         font-size: 1.1rem;
#         margin-bottom: 2rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ============ SESSION STATE INITIALIZATION ============
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "action_log" not in st.session_state:
#     st.session_state.action_log = []

# if "show_traces" not in st.session_state:
#     st.session_state.show_traces = False

# if "model_name" not in st.session_state:
#     st.session_state.model_name = "Claude 3.5 Sonnet"

# # ============ SIDEBAR ============
# with st.sidebar:
#     st.title("⚙️ Settings")
    
#     st.write("---")
    
#     # Model selection
#     st.subheader("Model")
#     model_option = st.selectbox(
#         "Choose your model",
#         ["Claude 3.5 Sonnet", "Claude 3.5 Haiku", "Claude 3 Opus"]
#     )
#     st.session_state.model_name = model_option
    
#     st.write("---")
    
#     # Show traces
#     st.subheader("Debug")
#     show_traces = st.checkbox("Show Traces", value=st.session_state.show_traces)
#     st.session_state.show_traces = show_traces
    
#     st.write("---")
    
#     # Memory stats
#     st.subheader("📊 Memory Stats")
#     try:
#         stats = memory_manager.get_stats()
#         st.write(f"**Papers:** {stats.get('papers', 0)}")
#         st.write(f"**Conversations:** {stats.get('conversations', 0)}")
#     except:
#         st.write("Stats unavailable")
    
#     st.write("---")
    
#     # Clear button
#     if st.button("🗑️ Clear Chat", use_container_width=True):
#         st.session_state.messages = []
#         st.session_state.action_log = []
#         st.rerun()
    
#     st.write("")
#     st.write("")
#     st.caption("Research Assistant v1.0")

# # ============ MAIN CHAT AREA ============
# st.markdown('<div class="main-title">🤖 Research Assistant</div>', unsafe_allow_html=True)
# st.markdown('<div class="subtitle">Interactive AI Assistant for Academic Research</div>', unsafe_allow_html=True)

# # Chat container
# chat_container = st.container()

# with chat_container:
#     # Display chat history
#     for message in st.session_state.messages:
#         role = message["role"]
#         content = message["content"]
        
#         if role == "user":
#             st.markdown(
#                 f'<div class="message-container"><div class="user-message">{content}</div></div>',
#                 unsafe_allow_html=True
#             )
#         else:
#             st.markdown(
#                 f'<div class="message-container"><div class="assistant-message">{content}</div></div>',
#                 unsafe_allow_html=True
#             )
    
#     # Show traces if enabled
#     if st.session_state.show_traces and st.session_state.action_log:
#         with st.expander("🔍 Recent Traces", expanded=False):
#             for trace in st.session_state.action_log[-5:]:
#                 st.code(trace, language=None)

# # ============ INPUT AREA ============
# st.markdown("---")

# # Create input form at bottom
# with st.form(key="chat_form", clear_on_submit=True):
#     col1, col2 = st.columns([6, 1])
    
#     with col1:
#         user_input = st.text_input(
#             "message",
#             placeholder="Type your message...",
#             label_visibility="collapsed"
#         )
    
#     with col2:
#         submit_button = st.form_submit_button("Send", use_container_width=True)

# # ============ PROCESS INPUT ============
# if submit_button and user_input:
#     # Add user message
#     st.session_state.messages.append({
#         "role": "user",
#         "content": user_input
#     })
    
#     # Log action
#     timestamp = datetime.now().strftime("%H:%M:%S")
#     st.session_state.action_log.append(f"[{timestamp}] User: {user_input[:50]}...")
    
#     # Get response from your existing system with progress indicators
#     status_placeholder = st.empty()
#     progress_bar = st.progress(0)
    
#     try:
#         # Show appropriate status message based on query type
#         if "literature review" in user_input.lower() or "synthesis" in user_input.lower() or "generate" in user_input.lower():
#             status_placeholder.info("📚 Generating literature review... This may take 30-60 seconds.")
#             progress_bar.progress(10)
#         elif "find" in user_input.lower() and "connection" in user_input.lower():
#             status_placeholder.info("🔍 Analyzing paper connections... This may take 10-20 seconds.")
#             progress_bar.progress(15)
#         elif "semantic" in user_input.lower() or "bridge" in user_input.lower():
#             status_placeholder.info("🧬 Performing semantic analysis... This may take 15-30 seconds.")
#             progress_bar.progress(15)
#         elif "export" in user_input.lower() or "bibtex" in user_input.lower():
#             status_placeholder.info("📎 Preparing BibTeX export...")
#             progress_bar.progress(20)
#         elif "search" in user_input.lower() or "find" in user_input.lower():
#             status_placeholder.info("🔍 Searching for papers...")
#             progress_bar.progress(25)
#         else:
#             status_placeholder.info("🤔 Processing your request...")
#             progress_bar.progress(30)
        
#         progress_bar.progress(50)  # Halfway through
#         response = execute_routed_query(user_input)
#         progress_bar.progress(100)  # Complete
        
#         status_placeholder.success("✅ Response generated!")
#         import time
#         time.sleep(0.5)  # Show success briefly
#         status_placeholder.empty()  # Clear status message
#         progress_bar.empty()  # Clear progress bar
        
#         # Extract clean output from various response formats
#         if isinstance(response, dict):
#             # Try to get output field
#             assistant_reply = response.get('output', None)
            
#             # If output is a list of dicts (LangChain format)
#             if isinstance(assistant_reply, list):
#                 # Extract text from list of response objects
#                 text_parts = []
#                 for item in assistant_reply:
#                     if isinstance(item, dict):
#                         if 'text' in item:
#                             text_parts.append(item['text'])
#                         elif 'content' in item:
#                             text_parts.append(item['content'])
#                 assistant_reply = '\n\n'.join(text_parts) if text_parts else str(assistant_reply)
            
#             # If still no good output, stringify the whole response
#             if not assistant_reply or assistant_reply == '':
#                 assistant_reply = str(response)
#         else:
#             assistant_reply = str(response)
        
#         # Truncate very long responses for UI display
#         if len(assistant_reply) > 10000:
#             assistant_reply = assistant_reply[:10000] + "\n\n... (Response truncated for display. Full output in terminal.)"
        
#         # Add assistant message
#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": assistant_reply
#         })
        
#         # Log action
#         st.session_state.action_log.append(f"[{timestamp}] Assistant: Response generated ({len(assistant_reply)} chars)")
        
#     except Exception as e:
#         error_msg = f"Error: {str(e)}"
#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": error_msg
#         })
#         st.session_state.action_log.append(f"[{timestamp}] Error: {str(e)}")
#         status_placeholder.empty()
#         progress_bar.empty()
    
#     # Rerun to update chat display
#     st.rerun()

# # ============ WELCOME MESSAGE ============
# if len(st.session_state.messages) == 0:
#     st.markdown("""
#     <div style='text-align: center; color: #666; padding: 3rem;'>
#         <p>👋 Welcome! I'm your research assistant.</p>
#         <p>I can help you with:</p>
#         <ul style='list-style: none; padding: 0;'>
#             <li>🔍 <strong>Search Papers:</strong> ArXiv, OpenAlex, or your local database</li>
#             <li>🧬 <strong>Analyze Connections:</strong> Find semantic links between papers</li>
#             <li>🌉 <strong>Discover Bridges:</strong> Identify cross-domain research opportunities</li>
#             <li>📝 <strong>Generate Reviews:</strong> Citation-enforced literature synthesis</li>
#             <li>📎 <strong>Export Citations:</strong> BibTeX format for LaTeX/reference managers</li>
#             <li>💾 <strong>Save Results:</strong> Export findings to files</li>
#         </ul>
#         <p><strong>Try asking:</strong></p>
#         <p style='font-size: 0.9rem; color: #888;'>
#             "Find new papers about transformers"<br>
#             "What papers do I have about BERT?"<br>
#             "Find semantic connections in my papers"<br>
#             "Generate a literature review on attention mechanisms"<br>
#             "Export papers to BibTeX"
#         </p>
#     </div>
#     """, unsafe_allow_html=True)

# # ============ FOOTER INFO ============
# st.markdown("---")
# col1, col2 = st.columns(2)
# with col1:
#     st.caption(f"📊 Papers in DB: {memory_manager.get_stats().get('papers', 0)}")
# with col2:
#     st.caption(f"🧠 Model: {st.session_state.model_name}")




