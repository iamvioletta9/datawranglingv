import streamlit as st
import time

# =============================================================================
# CONFIG
# =============================================================================
st.set_page_config(
    page_title="DataWrangler Pro",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# SESSION STATE
# =============================================================================
if "intro_done" not in st.session_state:
    st.session_state.intro_done = False

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "df" not in st.session_state:
    st.session_state.df = None

if "df_original" not in st.session_state:
    st.session_state.df_original = None

if "log" not in st.session_state:
    st.session_state.log = []

if "confetti_shown" not in st.session_state:
    st.session_state.confetti_shown = False

# =============================================================================
# CSS (FULL — FIXES YOUR ERROR)
# =============================================================================

LIGHT_CSS = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e8f0fe 0%, #f0f4ff 40%, #eef2ff 70%, #e8f4f8 100%);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
</style>
"""

DARK_CSS = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0f1e 0%, #0f172a 50%, #0d1526 100%) !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #0a0f1e 100%) !important;
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
</style>
"""

st.markdown(DARK_CSS if st.session_state.dark_mode else LIGHT_CSS, unsafe_allow_html=True)

# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:

    st.markdown("### 🔬 DataWrangler Pro")

    if st.button("🌙 / ☀️ Toggle Theme"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["Home", "Upload & Overview", "Cleaning", "Visualization", "Export", "AI"],
        format_func=lambda x: {
            "Home": "🏠 Home",
            "Upload & Overview": "📂 Upload",
            "Cleaning": "🧹 Cleaning",
            "Visualization": "📊 Visualization",
            "Export": "📤 Export",
            "AI": "🤖 AI Assistant"
        }[x]
    )

# =============================================================================
# CONFETTI (3 sec)
# =============================================================================
if not st.session_state.confetti_shown:
    st.markdown("""
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1"></script>
    <script>
    let duration = 3000;
    let end = Date.now() + duration;

    (function frame() {
        confetti({
            particleCount: 5,
            angle: 60,
            spread: 80,
            origin: { x: Math.random(), y: Math.random() - 0.2 }
        });
        if (Date.now() < end) {
            requestAnimationFrame(frame);
        }
    }());
    </script>
    """, unsafe_allow_html=True)

    st.session_state.confetti_shown = True

# =============================================================================
# INTRO
# =============================================================================
if not st.session_state.intro_done:

    st.markdown("""
    <div style="text-align:center; padding:5rem 2rem;">
      <div style="font-size:64px;">🔬</div>
      <h1>DataWrangler Pro</h1>
      <p>Your AI-powered data preparation workspace</p>
      <p>📂 Upload · 🧹 Clean · 📊 Visualize · 📤 Export</p>
    </div>
    """, unsafe_allow_html=True)

    bar = st.progress(0)

    for i in range(0, 101, 25):
        time.sleep(0.3)
        bar.progress(i)

    time.sleep(0.3)
    bar.empty()

    st.session_state.intro_done = True
    st.rerun()

# =============================================================================
# HOME PAGE
# =============================================================================
if page == "Home":

    st.markdown("## 🔬 DataWrangler Pro")
    st.caption("AI-powered data preparation & visualization workspace")

    st.markdown("---")

    cards = [
        ("📂", "Upload & Profile", "CSV · Excel · JSON"),
        ("🧹", "Clean & Prepare", "Missing · Duplicates"),
        ("📊", "Visualize", "Charts · Filters"),
        ("📤", "Export", "CSV · Report"),
    ]

    cols = st.columns(4)

    for col, (icon, title, desc) in zip(cols, cards):
        with col:
            st.markdown(f"""
            <div style="padding:20px; border-radius:12px; background:#ffffff20;">
                <div style="font-size:30px">{icon}</div>
                <div style="font-weight:600">{title}</div>
                <div style="font-size:12px">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("👈 Use the sidebar to start with Upload")

# =============================================================================
# PLACEHOLDERS (REQUIRED STRUCTURE)
# =============================================================================
elif page == "Upload & Overview":
    st.title("📂 Upload & Overview")
    st.info("Implement upload + profiling here")

elif page == "Cleaning":
    st.title("🧹 Cleaning Studio")
    st.info("Implement cleaning here")

elif page == "Visualization":
    st.title("📊 Visualization")
    st.info("Implement charts here")

elif page == "Export":
    st.title("📤 Export")
    st.info("Implement export here")

elif page == "AI":
    st.title("🤖 AI Assistant")

    if st.session_state.df is None:
        st.warning("Upload data first")
    else:
        st.write(st.session_state.df.describe())
