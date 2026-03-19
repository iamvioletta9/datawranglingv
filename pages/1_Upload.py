import streamlit as st
import pandas as pd
import numpy as np

# --- SESSION INIT ---
if "df" not in st.session_state:
    st.session_state.df = None
if "log" not in st.session_state:
    st.session_state.log = []

st.title("📂 Upload & Data Profiling")

file = st.file_uploader("Upload CSV / Excel / JSON", type=["csv", "xlsx", "json"])

# --- FILE LOAD ---
if file is not None:
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)

        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)

        elif file.name.endswith(".json"):
            df = pd.read_json(file)

        else:
            st.error("Unsupported file type")
            st.stop()

        st.session_state.df = df
        st.success("✅ File uploaded successfully!")

    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
        st.stop()

# --- DISPLAY DATA ---
if st.session_state.df is not None:
    df = st.session_state.df

    st.subheader("📊 Dataset Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Duplicates", df.duplicated().sum())

    # =========================
    # 🔹 COLUMN TYPE GROUPING
    # =========================
    st.write("### 🧩 Column Categories")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()
    datetime_cols = df.select_dtypes(include="datetime").columns.tolist()

    st.write(f"**Numeric ({len(numeric_cols)}):**", numeric_cols)
    st.write(f"**Categorical ({len(categorical_cols)}):**", categorical_cols)
    st.write(f"**Datetime ({len(datetime_cols)}):**", datetime_cols)

    # =========================
    # 🔹 MISSING VALUES (COUNT + %)
    # =========================
    st.write("### ⚠️ Missing Values Analysis")

    missing_count = df.isnull().sum()
    missing_percent = (missing_count / len(df)) * 100

    missing_df = pd.DataFrame({
        "Missing Count": missing_count,
        "Missing %": missing_percent.round(2)
    })

    st.dataframe(missing_df[missing_df["Missing Count"] > 0])

    # =========================
    # 🔹 OUTLIERS (IQR METHOD)
    # =========================
    st.write("### 📈 Outlier Detection (Numeric Columns)")

    outlier_counts = {}

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower) | (df[col] > upper)]
        outlier_counts[col] = len(outliers)

    outlier_df = pd.DataFrame.from_dict(outlier_counts, orient="index", columns=["Outliers"])
    st.dataframe(outlier_df[outlier_df["Outliers"] > 0])

    # =========================
    # 🔹 PREVIEW
    # =========================
    st.write("### 🔍 Data Preview")
    st.dataframe(df.head())

    # =========================
    # 🔹 RESET
    # =========================
    if st.button("Reset Session"):
        st.session_state.df = None
        st.session_state.log = []
        st.rerun()
