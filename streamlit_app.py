import streamlit as st
import time

st.set_page_config(page_title="Data Wrangler & Visualizer", layout="wide")

# SESSION INIT
if "intro_done" not in st.session_state:
    st.session_state.intro_done = False
if "history" not in st.session_state:
    st.session_state.history = []   # for undo

# STYLE
st.markdown("""
<style>
.fullscreen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: black;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    z-index: 999999;
    text-align: center;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# INTRO
if not st.session_state.intro_done:
    st.markdown("""
    <div class="fullscreen">
        <h1>AI Data Wrangler & Visualizer</h1>
        <h3>Developed by</h3>
        <h2>00017592 & 00018555</h2>
    </div>
    """, unsafe_allow_html=True)

    st.balloons()
    time.sleep(4)
    st.session_state.intro_done = True
    st.rerun()

# MAIN
st.title("AI-Assisted Data Wrangler & Visualizer")

st.markdown("""
This application simulates a **real-world data preparation pipeline**:

- Upload → Profile → Clean → Transform → Visualize → Export  
- Fully interactive  
- Reproducible workflow via transformation logs  

Use sidebar to navigate.
""")

st.info("Coursework Project – Data Wrangling & Visualization")
