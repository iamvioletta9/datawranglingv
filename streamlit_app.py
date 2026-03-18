import streamlit as st
import time

st.set_page_config(page_title="Data Wrangler & Visualizer", layout="wide")

# ===============================
# 🔹 SESSION INIT
# ===============================
if "intro_done" not in st.session_state:
    st.session_state.intro_done = False

# ===============================
# 🔹 FULLSCREEN + BACKGROUND STYLE
# ===============================
st.markdown("""
<style>
.fullscreen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    z-index: 999999;
    text-align: center;
    color: white;
    animation: fadeIn 1.5s ease-in-out;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# ===============================
# 🔹 INTRO SCREEN (3s + ANIMATION)
# ===============================
if not st.session_state.intro_done:

    st.markdown("""
    <div class="fullscreen">
        <h1 style="font-size:60px;">Data Wrangler & Visualizer</h1>
        <h3>Interactive Data Preparation Studio</h3>
        <p style="opacity:0.8;">Preparing your workspace...</p>
    </div>
    """, unsafe_allow_html=True)

    # 🎉 Animations
    st.balloons()
    st.snow()   # subtle sparkle effect

    time.sleep(3)

    st.session_state.intro_done = True
    st.rerun()

# ===============================
# 🔹 MAIN LANDING PAGE
# ===============================
st.title("AI-Assisted Data Wrangler & Visualizer")

st.markdown("""
### 📊 Project Overview

This application provides an interactive environment for data preparation, transformation, and visualization.  
It is designed to support users in exploring datasets efficiently and generating meaningful insights.

### ⚙️ Key Features

- Upload datasets (CSV, Excel, JSON)
- Perform data cleaning and preprocessing
- Handle missing values, duplicates, and outliers
- Transform and scale data
- Build interactive visualizations
- Export cleaned datasets and transformation reports

### 🎯 Objective

The goal of this application is to simulate a real-world data preparation workflow,  
combining usability, flexibility, and analytical capability in a single interface.

👉 Use the sidebar to navigate through the application.
""")

st.markdown("---")

st.info("Coursework Project – Data Wrangling & Visualization Module")
st.caption("Developed by Student IDs: 00017592 & 00018555")
