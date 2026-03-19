import streamlit as st
import pandas as pd

# ===============================
# 🔹 SESSION
# ===============================
if "df" not in st.session_state:
    st.session_state.df = None

st.title("🤖 AI Data Assistant (Smart Insights)")

if st.session_state.df is None:
    st.warning("Upload dataset first")
    st.stop()

df = st.session_state.df

# ===============================
# 🔹 BASIC ANALYSIS
# ===============================
numeric_cols = df.select_dtypes(include="number").columns
categorical_cols = df.select_dtypes(include=["object"]).columns

# ===============================
# 🔹 USER INPUT
# ===============================
question = st.text_input("Ask about your dataset")

# ===============================
# 🔹 RESPONSE ENGINE (NO API)
# ===============================
def generate_answer(q):
    q = q.lower()

    # 1️⃣ missing values
    if "missing" in q:
        missing = df.isnull().sum().sum()
        return f"There are {missing} missing values in the dataset."

    # 2️⃣ duplicates
    elif "duplicate" in q:
        dup = df.duplicated().sum()
        return f"There are {dup} duplicate rows."

    # 3️⃣ numeric summary
    elif "summary" in q or "describe" in q:
        return df.describe().to_string()

    # 4️⃣ correlations
    elif "correlation" in q and len(numeric_cols) > 1:
        corr = df[numeric_cols].corr()
        return "Correlation matrix:\n" + corr.to_string()

    # 5️⃣ most important column
    elif "important" in q or "impact" in q:
        if len(numeric_cols) > 0:
            return f"Column '{numeric_cols[0]}' may be important based on numeric analysis."
        else:
            return "No numeric columns to evaluate importance."

    # 6️⃣ outliers
    elif "outlier" in q:
        return "Outliers can be detected using IQR method in Cleaning section."

    # 7️⃣ general insights
    elif "insight" in q or "pattern" in q:
        return f"""
Dataset has {df.shape[0]} rows and {df.shape[1]} columns.
- Numeric columns: {len(numeric_cols)}
- Categorical columns: {len(categorical_cols)}
Look for trends in visualizations for deeper insights.
"""

    # fallback
    else:
        return "Try asking about: missing values, duplicates, summary, correlation, insights."

# ===============================
# 🔹 OUTPUT
# ===============================
if question:
    answer = generate_answer(question)

    st.subheader("📊 Answer")
    st.text(answer)

    # OPTIONAL LOGGING
    if "log" in st.session_state:
        st.session_state.log.append("AI assistant used")
