import streamlit as st
import time

st.set_page_config(page_title="AI Data Wrangler", layout="wide")

# SESSION INIT
if "intro_done" not in st.session_state:
    st.session_state.intro_done = False

if "df" not in st.session_state:
    st.session_state.df = None

if "log" not in st.session_state:
    st.session_state.log = []

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
        <h1 style="font-size:70px;">🎉 Made by Violetta & Sohiba 🎉</h1>
        <h2>(Hope it is 90+ 😄)</h2>
    </div>
    """, unsafe_allow_html=True)

    st.balloons()
    time.sleep(0.5)
    st.balloons()
    time.sleep(0.5)

    st.session_state.intro_done = True
    st.rerun()

# MAIN
st.title("AI-Assisted Data Wrangler & Visualizer")

st.markdown("""
### About this application

Upload, clean, visualize, and export data interactively.

👉 Use the sidebar.
""")

st.success("Created by Violetta & Sohiba")
