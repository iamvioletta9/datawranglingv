import streamlit as st
import time

st.set_page_config(
    page_title="DataWrangler Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SESSION STATE
# ============================================================================
if "splash_shown" not in st.session_state:
    st.session_state.splash_shown = False
if "df_original" not in st.session_state:
    st.session_state.df_original = None
if "df_working" not in st.session_state:
    st.session_state.df_working = None
if "transformation_log" not in st.session_state:
    st.session_state.transformation_log = []
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "file_name" not in st.session_state:
    st.session_state.file_name = None

# ============================================================================
# SPLASH SCREEN WITH CONFETTI (3 SECONDS)
# ============================================================================
if not st.session_state.splash_shown:
    import streamlit.components.v1 as components
    
    splash_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            .splash {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 999999;
                animation: fadeOut 0.5s ease 2.5s forwards;
                font-family: system-ui, -apple-system, sans-serif;
            }
            @keyframes fadeOut {
                to {
                    opacity: 0;
                    visibility: hidden;
                }
            }
            .content {
                text-align: center;
                animation: slideUp 0.6s ease-out;
            }
            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            .logo {
                font-size: 80px;
                margin-bottom: 16px;
                animation: bounce 0.8s ease;
            }
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-15px); }
            }
            h1 {
                color: white;
                font-size: 36px;
                font-weight: 700;
                margin-bottom: 8px;
            }
            .sub {
                color: rgba(255,255,255,0.9);
                font-size: 16px;
                margin-bottom: 24px;
            }
            .loader {
                width: 40px;
                height: 40px;
                margin: 16px auto;
                border: 3px solid rgba(255,255,255,0.3);
                border-radius: 50%;
                border-top-color: white;
                animation: spin 0.8s linear infinite;
            }
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="splash">
            <div class="content">
                <div class="logo">✨</div>
                <h1>DataWrangler Pro</h1>
                <div class="sub">Your AI-powered data preparation workspace</div>
                <div class="loader"></div>
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1"></script>
        <script>
            (function() {
                let duration = 2500;
                let end = Date.now() + duration;
                function random(min, max) {
                    return Math.random() * (max - min) + min;
                }
                (function frame() {
                    confetti({
                        particleCount: 2,
                        angle: random(60, 120),
                        spread: random(50, 80),
                        origin: { x: random(0, 1), y: random(0, 0.5) },
                        colors: ['#ffffff', '#ffd700', '#ff69b4', '#00ff00']
                    });
                    if (Date.now() < end) {
                        requestAnimationFrame(frame);
                    }
                }());
            })();
        </script>
    </body>
    </html>
    """
    
    components.html(splash_html, height=0, width=0)
    time.sleep(3)
    st.session_state.splash_shown = True
    st.rerun()

# ============================================================================
# CSS - FIXED TOP BAR (make it visible)
# ============================================================================
if st.session_state.dark_mode:
    st.markdown("""
    <style>
    /* Fix top bar - make it visible */
    header {
        background: #1e293b !important;
        border-bottom: 1px solid #334155 !important;
    }
    header * {
        color: #ffffff !important;
    }
    [data-testid="stToolbar"] {
        color: #ffffff !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    h1, h2, h3, h4, p, label, div, span {
        color: #ffffff !important;
    }
    
    [data-testid="stMetric"] {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 16px;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #facc15 !important;
    }
    
    .stButton > button {
        background: #6366f1;
        color: white !important;
        border-radius: 10px;
    }
    
    .stButton > button:hover {
        background: #8b5cf6;
    }
    
    [data-testid="stSidebar"] {
        background: #0f172a;
        border-right: 1px solid #334155;
    }
    
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    .stAlert {
        background: #1e293b;
        border-left: 4px solid #6366f1;
    }
    
    hr {
        border-color: #334155;
    }
    
    /* Remove extra spacing */
    .block-container {
        padding-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    /* Fix top bar - make it visible */
    header {
        background: #ffffff !important;
        border-bottom: 1px solid #e2e8f0 !important;
    }
    header * {
        color: #0f172a !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
    }
    
    h1, h2, h3, h4, p, label, div, span {
        color: #0f172a !important;
    }
    
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    [data-testid="stMetricLabel"] {
        color: #475569 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #6366f1 !important;
    }
    
    .stButton > button {
        background: #6366f1;
        color: white !important;
        border-radius: 10px;
    }
    
    .stButton > button:hover {
        background: #8b5cf6;
    }
    
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] * {
        color: #0f172a !important;
    }
    
    .stAlert {
        background: #fef9e3;
        border-left: 4px solid #f59e0b;
    }
    
    /* Remove extra spacing */
    .block-container {
        padding-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0;">
        <div style="font-size: 48px;">✨</div>
        <div style="font-size: 18px; font-weight: 600;">DataWrangler Pro</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Theme toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Theme**")
    with col2:
        if st.button("🌙" if not st.session_state.dark_mode else "☀️", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    st.markdown("---")
    
    # Navigation - icons only
    if st.button("📂 Upload & Profile", use_container_width=True):
        st.switch_page("pages/01_Upload_Profile.py")
    
    if st.button("🧹 Cleaning Studio", use_container_width=True):
        st.switch_page("pages/02_Cleaning_Studio.py")
    
    if st.button("📊 Visualization", use_container_width=True):
        st.switch_page("pages/03_Visualization.py")
    
    if st.button("📤 Export & Report", use_container_width=True):
        st.switch_page("pages/04_Export_Report.py")
    
    st.markdown("---")
    
    if st.session_state.df_working is not None:
        st.success(f"✅ {len(st.session_state.df_working):,} rows")
        if st.button("🔄 Reset", use_container_width=True):
            if st.session_state.df_original is not None:
                st.session_state.df_working = st.session_state.df_original.copy()
            st.session_state.transformation_log = []
            st.rerun()
    
    st.markdown("---")
    st.caption("IDs: 00017592 & 00018555")

# ============================================================================
# MAIN CONTENT - ICONS ONLY (clean, no repetition)
# ============================================================================
st.markdown("""
<div style="text-align: center; padding: 20px 0 10px;">
    <h1 style="font-size: 42px;">DataWrangler Pro</h1>
    <p style="font-size: 16px;">Your AI-powered data preparation & visualization workspace</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Feature cards - only icons, clean design
col1, col2, col3, col4 = st.columns(4)

bg_color = "#1e293b" if st.session_state.dark_mode else "white"
border_color = "#334155" if st.session_state.dark_mode else "#e2e8f0"

with col1:
    st.markdown(f"""
    <div style="background: {bg_color}; border: 1px solid {border_color}; border-radius: 20px; padding: 24px 16px; text-align: center; transition: all 0.2s;">
        <div style="font-size: 56px; margin-bottom: 12px;">📂</div>
        <div style="font-size: 16px; font-weight: 600;">Upload & Profile</div>
        <div style="font-size: 12px; opacity: 0.7;">CSV · Excel · JSON</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: {bg_color}; border: 1px solid {border_color}; border-radius: 20px; padding: 24px 16px; text-align: center; transition: all 0.2s;">
        <div style="font-size: 56px; margin-bottom: 12px;">🧹</div>
        <div style="font-size: 16px; font-weight: 600;">Clean & Prepare</div>
        <div style="font-size: 12px; opacity: 0.7;">Missing · Duplicates · Scale</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: {bg_color}; border: 1px solid {border_color}; border-radius: 20px; padding: 24px 16px; text-align: center; transition: all 0.2s;">
        <div style="font-size: 56px; margin-bottom: 12px;">📊</div>
        <div style="font-size: 16px; font-weight: 600;">Visualize</div>
        <div style="font-size: 12px; opacity: 0.7;">8 chart types · Interactive</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background: {bg_color}; border: 1px solid {border_color}; border-radius: 20px; padding: 24px 16px; text-align: center; transition: all 0.2s;">
        <div style="font-size: 56px; margin-bottom: 12px;">📤</div>
        <div style="font-size: 16px; font-weight: 600;">Export</div>
        <div style="font-size: 12px; opacity: 0.7;">CSV · Excel · Report</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.info("👈 Use the sidebar to navigate. Start with **Upload & Profile** to load your dataset.")
st.caption("DataWrangler Pro · Coursework Project — Data Wrangling & Visualization")
