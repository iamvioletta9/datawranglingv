import streamlit as st
import pandas as pd
import numpy as np

# CACHING (REQUIRED)
@st.cache_data
def load_csv(file):
    return pd.read_csv(file)

@st.cache_data
def load_excel(file):
    return pd.read_excel(file)

@st.cache_data
def load_json(file):
    return pd.read_json(file)

# SESSION
if "df" not in st.session_state:
    st.session_state.df = None
if "log" not in st.session_state:
    st.session_state.log = []
if "history" not in st.session_state:
    st.session_state.history = []

st.title("📂 Upload & Profiling")

# GOOGLE SHEETS (BONUS)
sheet_url = st.text_input("Optional: Google Sheets URL")

if sheet_url:
    try:
        df = pd.read_csv(sheet_url.replace("/edit#gid=", "/export?format=csv&gid="))
        st.session_state.df = df
        st.success("Loaded from Google Sheets")
    except:
        st.error("Invalid Google Sheets link")

# FILE UPLOAD
file = st.file_uploader("Upload CSV / Excel / JSON", type=["csv", "xlsx", "json"])

if file:
    try:
        if file.name.endswith(".csv"):
            df = load_csv(file)
        elif file.name.endswith(".xlsx"):
            df = load_excel(file)
        elif file.name.endswith(".json"):
            df = load_json(file)

        st.session_state.df = df
        st.session_state.history.append(df.copy())
        st.session_state.log.append("Dataset uploaded")

        st.success("File uploaded")

    except Exception as e:
        st.error(e)

# DISPLAY
if st.session_state.df is not None:
    df = st.session_state.df

    st.metric("Rows", df.shape[0])
    st.metric("Columns", df.shape[1])
    st.metric("Duplicates", df.duplicated().sum())

    st.dataframe(df.describe(include="all"))
    st.dataframe(df.isnull().sum())

    if st.button("Reset Session"):
        st.session_state.df = None
        st.session_state.log = []
        st.session_state.history = []
        st.rerun()
