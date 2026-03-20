import streamlit as st
import pandas as pd
import numpy as np

# --- SESSION INIT ---
if "df" not in st.session_state:
    st.session_state.df = None
if "log" not in st.session_state:
    st.session_state.log = []
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🧹 Data Cleaning")

if st.session_state.df is None:
    st.warning("Please upload data first")
    st.stop()

df = st.session_state.df.copy()

# ===============================
# 🔹 UNDO (ADDED)
# ===============================
if st.button("↩ Undo last step"):
    if len(st.session_state.history) > 1:
        st.session_state.history.pop()
        st.session_state.df = st.session_state.history[-1]
        st.rerun()

# ===============================
# 🔹 PREVIEW
# ===============================
st.subheader("Dataset Preview")
st.dataframe(df.head())

# ===============================
# 🔹 MISSING VALUES
# ===============================
st.subheader("Missing Values Handling")

col = st.selectbox("Select column", df.columns)
col_type = df[col].dtype

st.info(f"Column type: {col_type}")

if col_type == "object":
    method = st.selectbox("Method", ["Drop rows", "Mode", "Constant", "Forward Fill", "Backward Fill"])
else:
    method = st.selectbox("Method", ["Drop rows", "Mean", "Median", "Mode", "Forward Fill", "Backward Fill"])

if method == "Constant":
    const_value = st.text_input("Enter constant value")

if st.button("Apply Missing Handling"):

    st.session_state.history.append(df.copy())

    before = df[col].isnull().sum()

    try:
        if method == "Drop rows":
            df = df.dropna(subset=[col])

        elif method == "Mean":
            df[col] = df[col].fillna(df[col].mean())

        elif method == "Median":
            df[col] = df[col].fillna(df[col].median())

        elif method == "Mode":
            df[col] = df[col].fillna(df[col].mode()[0])

        elif method == "Constant":
            df[col] = df[col].fillna(const_value)

        elif method == "Forward Fill":
            df[col] = df[col].fillna(method="ffill")

        elif method == "Backward Fill":
            df[col] = df[col].fillna(method="bfill")

        after = df[col].isnull().sum()

        st.session_state.df = df
        st.session_state.log.append(f"Handled missing in '{col}' using {method}")

        st.success(f"{before - after} missing values handled")

    except Exception as e:
        st.error(f"Error: {e}")

# ===============================
# 🔹 SCALING (ADDED)
# ===============================
st.subheader("Scaling / Normalization")

num_cols = df.select_dtypes(include=np.number).columns

if len(num_cols) > 0:
    col_scale = st.selectbox("Column to scale", num_cols)

    method_scale = st.selectbox("Scaling method", ["Min-Max", "Z-score"])

    if st.button("Apply Scaling"):
        st.session_state.history.append(df.copy())

        if method_scale == "Min-Max":
            df[col_scale] = (df[col_scale] - df[col_scale].min()) / (df[col_scale].max() - df[col_scale].min())
        else:
            df[col_scale] = (df[col_scale] - df[col_scale].mean()) / df[col_scale].std()

        st.session_state.df = df
        st.session_state.log.append(f"Scaled '{col_scale}'")

        st.success("Scaling applied")

# ===============================
# 🔹 FINAL PREVIEW
# ===============================
st.subheader("Updated Dataset")
st.dataframe(st.session_state.df.head())
