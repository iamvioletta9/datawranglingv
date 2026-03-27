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
# CSS (ТВОЙ — НЕ МЕНЯЮ)
# =============================================================================
# ВАЖНО: вставь сюда свой LIGHT_CSS и DARK_CSS без изменений

st.markdown(DARK_CSS if st.session_state.dark_mode else LIGHT_CSS, unsafe_allow_html=True)

# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:

    st.markdown("### 🔬 DataWrangler Pro")

    dm_label = "☀️ Light mode" if st.session_state.dark_mode else "🌙 Dark mode"
    if st.button(dm_label):
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
# CONFETTI (3 seconds)
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
# INTRO SCREEN (ONCE)
# =============================================================================
if not st.session_state.intro_done:

    st.markdown("""
    <div style="text-align:center; padding:5rem 2rem 3rem;">
      <div style="font-size:64px;">🔬</div>
      <h1>DataWrangler Pro</h1>
      <p>Your AI-powered data preparation workspace</p>
      <div style="margin-top:20px;">
        📂 Upload · 🧹 Clean · 📊 Visualize · 📤 Export
      </div>
    </div>
    """, unsafe_allow_html=True)

    bar = st.progress(0, text="Initializing...")

    for pct in [20, 50, 80, 100]:
        time.sleep(0.4)
        bar.progress(pct)

    time.sleep(0.3)
    bar.empty()

    st.session_state.intro_done = True
    st.rerun()

# =============================================================================
# HOME PAGE (ONLY UI — NO UPLOAD HERE)
# =============================================================================
if page == "Home":

    st.markdown("## 🔬 DataWrangler Pro")
    st.caption("AI-powered data preparation & visualization workspace")

    st.markdown("---")

    if st.session_state.dark_mode:
        cards = [
            ("#1e3a5f", "#93c5fd", "📂", "Upload & Profile", "CSV · Excel · JSON"),
            ("#14532d", "#86efac", "🧹", "Clean & Prepare", "Missing · Duplicates"),
            ("#3b0764", "#d8b4fe", "📊", "Visualize", "Charts · Filters"),
            ("#431407", "#fdba74", "📤", "Export", "CSV · Report"),
        ]
    else:
        cards = [
            ("#eff6ff", "#1e40af", "📂", "Upload & Profile", "CSV · Excel · JSON"),
            ("#f0fdf4", "#166534", "🧹", "Clean & Prepare", "Missing · Duplicates"),
            ("#fdf4ff", "#6b21a8", "📊", "Visualize", "Charts · Filters"),
            ("#fff7ed", "#9a3412", "📤", "Export", "CSV · Report"),
        ]

    cols = st.columns(4)

    for col, (bg, color, icon, title, sub) in zip(cols, cards):
        with col:
            st.markdown(f"""
            <div style="background:{bg}; padding:20px; border-radius:12px;">
                <div style="font-size:30px">{icon}</div>
                <div style="font-weight:600; color:{color}">{title}</div>
                <div style="font-size:12px; color:{color}">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("👈 Use the sidebar to start with Upload section")

# =============================================================================
# PLACEHOLDER PAGES (CW STRUCTURE)
# =============================================================================
elif page == "Upload & Overview":
    st.title("📂 Upload & Overview")
    st.warning("Move your upload logic here (separate file recommended)")

elif page == "Cleaning":
    st.title("🧹 Cleaning Studio")
    st.warning("Cleaning logic goes here")

elif page == "Visualization":
    st.title("📊 Visualization Builder")
    st.warning("Charts logic goes here")

elif page == "Export":
    st.title("📤 Export & Report")
    st.warning("Export logic goes here")

elif page == "AI":
    st.title("🤖 AI Assistant")

    if st.session_state.df is None:
        st.warning("Upload data first")
    else:
        st.write("Basic dataset insights:")
        st.write(st.session_state.df.describe())

        query = st.text_input("Ask about your data")

        if st.button("Analyze"):
            st.info("Correlation matrix:")
            st.write(st.session_state.df.corr(numeric_only=True))
