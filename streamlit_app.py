import streamlit as st
import time

# Page config must be first
st.set_page_config(
    page_title="DataWrangler Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SESSION STATE INITIALIZATION
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
# SPLASH SCREEN (WITH CONFETTI - 3 SECONDS)
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
            
            .splash-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 99999;
                animation: fadeOut 0.6s ease-in-out 2.8s forwards;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            @keyframes fadeOut {
                to {
                    opacity: 0;
                    visibility: hidden;
                }
            }
            
            .splash-content {
                text-align: center;
                animation: slideUp 0.8s ease-out;
            }
            
            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(50px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .logo-icon {
                font-size: 100px;
                animation: bounce 1s ease-in-out;
                margin-bottom: 20px;
                display: inline-block;
            }
            
            @keyframes bounce {
                0%, 100% {
                    transform: translateY(0);
                }
                50% {
                    transform: translateY(-20px);
                }
            }
            
            h1 {
                color: white;
                font-size: 48px;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                font-weight: 700;
            }
            
            .subtitle {
                color: rgba(255,255,255,0.9);
                font-size: 18px;
                margin-bottom: 30px;
                letter-spacing: 1px;
            }
            
            .loader {
                width: 50px;
                height: 50px;
                margin: 20px auto;
                border: 4px solid rgba(255,255,255,0.3);
                border-radius: 50%;
                border-top-color: white;
                animation: spin 1s ease-in-out infinite;
            }
            
            @keyframes spin {
                to {
                    transform: rotate(360deg);
                }
            }
            
            .tagline {
                color: rgba(255,255,255,0.7);
                font-size: 12px;
                margin-top: 30px;
                letter-spacing: 2px;
            }
        </style>
    </head>
    <body>
        <div class="splash-container" id="splash">
            <div class="splash-content">
                <div class="logo-icon">✨</div>
                <h1>DataWrangler Pro</h1>
                <div class="subtitle">Where Data Meets Intelligence</div>
                <div class="loader"></div>
                <div class="tagline">Precision • Insight • Excellence</div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1"></script>
        <script>
            (function() {
                let duration = 2500;
                let end = Date.now() + duration;
                
                function randomInRange(min, max) {
                    return Math.random() * (max - min) + min;
                }
                
                (function frame() {
                    confetti({
                        particleCount: 3,
                        angle: randomInRange(55, 125),
                        spread: randomInRange(50, 70),
                        origin: { x: randomInRange(0, 1), y: randomInRange(0, 0.5) },
                        colors: ['#ffffff', '#ffd700', '#ff69b4', '#00ff00', '#ff6b6b']
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
# CUSTOM CSS (With proper text contrast and consistent icon sizes)
# ============================================================================
def load_css():
    if st.session_state.dark_mode:
        return """
        <style>
        /* DARK MODE - PREMIUM WITH CLEAR TEXT */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif !important;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        }
        
        /* ALL TEXT - HIGH CONTRAST */
        h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown, div, .stText {
            color: #f1f5f9 !important;
        }
        
        .stMarkdown p, .stMarkdown li, .stMarkdown div {
            color: #e2e8f0 !important;
        }
        
        /* Metric Cards */
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 20px !important;
            transition: all 0.2s;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            border-color: #6366f1;
        }
        
        [data-testid="stMetricLabel"] {
            color: #94a3b8 !important;
            font-size: 13px !important;
            font-weight: 500 !important;
        }
        
        [data-testid="stMetricValue"] {
            color: #facc15 !important;
            font-size: 28px !important;
            font-weight: 700 !important;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white !important;
            border: none;
            border-radius: 12px;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(99,102,241,0.4);
        }
        
        /* Download Buttons */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white !important;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a, #1e1b4b);
            border-right: 1px solid #334155;
        }
        
        [data-testid="stSidebar"] * {
            color: #f1f5f9 !important;
        }
        
        /* Sidebar buttons */
        [data-testid="stSidebar"] .stButton > button {
            background: transparent;
            border: 1px solid #334155;
            color: #e2e8f0 !important;
        }
        
        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(99,102,241,0.2);
            border-color: #6366f1;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background: #1e293b;
            border-radius: 12px;
            color: #f1f5f9 !important;
        }
        
        /* Dataframe */
        .stDataFrame {
            background: #1e293b;
            border-radius: 12px;
        }
        
        /* Alerts */
        .stAlert {
            background: #1e293b;
            border-left: 4px solid #6366f1;
        }
        
        hr {
            border-color: #334155;
        }
        
        /* Consistent icon sizes */
        .feature-icon {
            font-size: 48px;
            display: inline-block;
            margin-bottom: 12px;
        }
        
        .sidebar-logo-icon {
            font-size: 48px;
            display: inline-block;
        }
        </style>
        """
    else:
        return """
        <style>
        /* LIGHT MODE - PREMIUM WITH CLEAR TEXT */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif !important;
        }
        
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #eff6ff 100%);
        }
        
        /* ALL TEXT - DARK AND READABLE */
        h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown, div, .stText {
            color: #0f172a !important;
        }
        
        .stMarkdown p, .stMarkdown li, .stMarkdown div {
            color: #1e293b !important;
        }
        
        /* Metric Cards */
        [data-testid="stMetric"] {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 20px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: all 0.2s;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
            border-color: #6366f1;
        }
        
        [data-testid="stMetricLabel"] {
            color: #475569 !important;
            font-size: 13px !important;
            font-weight: 500 !important;
        }
        
        [data-testid="stMetricValue"] {
            color: #6366f1 !important;
            font-size: 28px !important;
            font-weight: 700 !important;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white !important;
            border: none;
            border-radius: 12px;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(99,102,241,0.4);
        }
        
        /* Download Buttons */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white !important;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff, #f8fafc);
            border-right: 1px solid #e2e8f0;
        }
        
        [data-testid="stSidebar"] * {
            color: #0f172a !important;
        }
        
        /* Sidebar buttons */
        [data-testid="stSidebar"] .stButton > button {
            background: transparent;
            border: 1px solid #e2e8f0;
            color: #0f172a !important;
        }
        
        [data-testid="stSidebar"] .stButton > button:hover {
            background: #f1f5f9;
            border-color: #6366f1;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background: #f1f5f9;
            border-radius: 12px;
            color: #0f172a !important;
        }
        
        /* Dataframe */
        .stDataFrame {
            background: white;
            border-radius: 12px;
        }
        
        /* Alerts */
        .stAlert {
            background: #fef9e3;
            border-left: 4px solid #f59e0b;
        }
        
        /* Consistent icon sizes */
        .feature-icon {
            font-size: 48px;
            display: inline-block;
            margin-bottom: 12px;
        }
        
        .sidebar-logo-icon {
            font-size: 48px;
            display: inline-block;
        }
        </style>
        """

st.markdown(load_css(), unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    # Logo section - consistent icon size
    st.markdown("""
    <div style="text-align: center; padding: 16px 0 8px 0;">
        <div style="font-size: 48px; line-height: 1;">✨</div>
        <div style="font-size: 18px; font-weight: 600; margin-top: 8px;">DataWrangler Pro</div>
        <div style="font-size: 11px; opacity: 0.6;">v2.0</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Dark mode toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Theme**")
    with col2:
        theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
        if st.button(theme_icon, help="Toggle theme", use_container_width=True, key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    st.markdown("---")
    
    # Navigation - consistent button styling
    st.markdown("### Navigation")
    
    pages = {
        "📂 Upload & Profile": "pages/01_Upload_Profile.py",
        "🧹 Cleaning Studio": "pages/02_Cleaning_Studio.py",
        "📊 Visualization": "pages/03_Visualization.py",
        "📤 Export & Report": "pages/04_Export_Report.py"
    }
    
    for page_name, page_path in pages.items():
        if st.button(page_name, use_container_width=True, key=page_path):
            st.switch_page(page_path)
    
    st.markdown("---")
    
    # Session info
    if st.session_state.df_working is not None:
        st.success(f"✅ {len(st.session_state.df_working):,} rows • {len(st.session_state.df_working.columns)} cols")
        
        if st.button("🔄 Reset Session", use_container_width=True, key="reset_session"):
            if st.session_state.df_original is not None:
                st.session_state.df_working = st.session_state.df_original.copy()
            st.session_state.transformation_log = []
            st.rerun()
    else:
        st.info("📁 No dataset loaded")
    
    st.markdown("---")
    st.caption("Made with ✨ | IDs: 00017592 & 00018555")

# ============================================================================
# MAIN CONTENT (Landing Page)
# ============================================================================
st.markdown("""
<div style="text-align: center; padding: 2rem 0 1rem;">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">DataWrangler Pro</h1>
    <p style="font-size: 1.1rem; opacity: 0.8;">Your AI-powered data preparation & visualization workspace</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Feature cards - CONSISTENT ICON SIZES (all 48px)
col1, col2, col3, col4 = st.columns(4)

# All icons have consistent styling with fixed font size
feature_style = """
<div style="background: {bg}; border-radius: 20px; padding: 1.5rem; text-align: center;
            border: 1px solid {border}; transition: transform 0.2s, box-shadow 0.2s;">
    <div style="font-size: 48px; margin-bottom: 12px; line-height: 1;">{icon}</div>
    <div style="font-size: 18px; font-weight: 600; margin-bottom: 8px;">{title}</div>
    <div style="font-size: 13px; opacity: 0.7;">{desc}</div>
</div>
"""

if st.session_state.dark_mode:
    cards = [
        ("📂", "Upload & Profile", "CSV · Excel · JSON"),
        ("🧹", "Clean & Prepare", "Missing · Duplicates · Scale"),
        ("📊", "Visualize", "8 chart types · Interactive"),
        ("📤", "Export", "CSV · Excel · Report")
    ]
    bg_color = "#1e293b"
    border_color = "#334155"
else:
    cards = [
        ("📂", "Upload & Profile", "CSV · Excel · JSON"),
        ("🧹", "Clean & Prepare", "Missing · Duplicates · Scale"),
        ("📊", "Visualize", "8 chart types · Interactive"),
        ("📤", "Export", "CSV · Excel · Report")
    ]
    bg_color = "white"
    border_color = "#e2e8f0"

for col, (icon, title, desc) in zip([col1, col2, col3, col4], cards):
    with col:
        st.markdown(
            feature_style.format(icon=icon, title=title, desc=desc, bg=bg_color, border=border_color),
            unsafe_allow_html=True
        )

st.markdown("---")

# Info section
st.info("👈 Use the sidebar to navigate. Start with **Upload & Profile** to load your dataset.")

st.markdown("---")
st.caption("DataWrangler Pro · Coursework Project — Data Wrangling & Visualization")
