import streamlit as st
import pandas as pd
import json
from datetime import datetime
from io import BytesIO

# ===============================
# 🔹 SESSION
# ===============================
if "df" not in st.session_state:
    st.session_state.df = None
if "log" not in st.session_state:
    st.session_state.log = []

st.title("📤 Export & Transformation Report")

if st.session_state.df is None:
    st.warning("No dataset available")
    st.stop()

df = st.session_state.df

# ===============================
# 🔹 PREVIEW
# ===============================
st.subheader("Dataset Preview")
st.dataframe(df.head())

# ===============================
# 🔹 DATA SUMMARY (NEW)
# ===============================
st.subheader("📊 Dataset Summary")

summary = {
    "Rows": df.shape[0],
    "Columns": df.shape[1],
    "Missing Values": int(df.isnull().sum().sum()),
    "Duplicate Rows": int(df.duplicated().sum())
}

st.write(summary)

# ===============================
# 🔹 FILE NAME
# ===============================
filename = st.text_input("File name (without extension)", "cleaned_data")

# ===============================
# 🔹 EXPORT FORMAT
# ===============================
st.subheader("Download Dataset")

format_choice = st.selectbox(
    "Select format",
    ["CSV", "Excel", "JSON"]
)

# --- CSV ---
if format_choice == "CSV":
    csv = df.to_csv(index=False).encode()
    st.download_button(
        "Download CSV",
        csv,
        f"{filename}.csv",
        mime="text/csv"
    )

# --- EXCEL ---
elif format_choice == "Excel":
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")

    st.download_button(
        "Download Excel",
        buffer.getvalue(),
        f"{filename}.xlsx",
        mime="application/vnd.ms-excel"
    )

# --- JSON ---
elif format_choice == "JSON":
    json_data = df.to_json(orient="records", indent=2)

    st.download_button(
        "Download JSON",
        json_data,
        f"{filename}.json",
        mime="application/json"
    )

# ===============================
# 🔹 TRANSFORMATION REPORT
# ===============================
st.markdown("---")
st.subheader("📝 Transformation Report")

report = {
    "timestamp": str(datetime.now()),
    "dataset_summary": summary,
    "steps": st.session_state.log
}

# Display nicely
st.write("### Steps Applied")
st.write(st.session_state.log if st.session_state.log else "No transformations applied")

# Download report
st.download_button(
    "Download Report (JSON)",
    json.dumps(report, indent=2),
    f"{filename}_report.json",
    mime="application/json"
)
