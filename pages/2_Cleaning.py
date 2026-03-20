import streamlit as st
import pandas as pd
import numpy as np

if "df" not in st.session_state:
    st.stop()

df = st.session_state.df.copy()

st.title("🧹 Cleaning Studio")

# SAVE STATE FOR UNDO
def save_state():
    st.session_state.history.append(df.copy())

# =====================
# UNDO
# =====================
if st.button("Undo last step"):
    if len(st.session_state.history) > 1:
        st.session_state.history.pop()
        st.session_state.df = st.session_state.history[-1]
        st.rerun()

# =====================
# MISSING VALUES
# =====================
st.subheader("Missing Values")

col = st.selectbox("Column", df.columns)
method = st.selectbox("Method", ["Mean","Median","Mode","Forward Fill","Drop"])

if st.button("Apply Missing"):
    save_state()

    if method == "Mean":
        df[col] = df[col].fillna(df[col].mean())
    elif method == "Median":
        df[col] = df[col].fillna(df[col].median())
    elif method == "Mode":
        df[col] = df[col].fillna(df[col].mode()[0])
    elif method == "Forward Fill":
        df[col] = df[col].fillna(method="ffill")
    elif method == "Drop":
        df = df.dropna(subset=[col])

    st.session_state.df = df
    st.session_state.log.append(f"Missing handled: {col}")

# =====================
# CATEGORICAL TOOLS
# =====================
st.subheader("Categorical Cleaning")

cat_cols = df.select_dtypes(include="object").columns

if len(cat_cols):
    c = st.selectbox("Categorical column", cat_cols)

    if st.button("Lowercase"):
        save_state()
        df[c] = df[c].str.lower()

    if st.button("Trim spaces"):
        save_state()
        df[c] = df[c].str.strip()

# =====================
# SCALING (REQUIRED)
# =====================
st.subheader("Scaling")

num_cols = df.select_dtypes(include=np.number).columns

if len(num_cols):
    col_s = st.selectbox("Column to scale", num_cols)
    method_s = st.selectbox("Scaling method", ["MinMax","Z-score"])

    if st.button("Apply Scaling"):
        save_state()

        if method_s == "MinMax":
            df[col_s] = (df[col_s] - df[col_s].min()) / (df[col_s].max() - df[col_s].min())
        else:
            df[col_s] = (df[col_s] - df[col_s].mean()) / df[col_s].std()

        st.session_state.df = df
        st.session_state.log.append(f"Scaled {col_s}")

# =====================
# VALIDATION RULES
# =====================
st.subheader("Validation")

if len(num_cols):
    col_v = st.selectbox("Validate column", num_cols)
    min_v = st.number_input("Min")
    max_v = st.number_input("Max")

    if st.button("Check violations"):
        violations = df[(df[col_v] < min_v) | (df[col_v] > max_v)]
        st.dataframe(violations)

# =====================
st.dataframe(df.head())
