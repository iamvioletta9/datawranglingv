import streamlit as st
import pandas as pd
import numpy as np

# ===============================
# 🔹 SESSION
# ===============================
if "df" not in st.session_state or st.session_state.df is None:
    st.warning("Please upload dataset first")
    st.stop()

if "log" not in st.session_state:
    st.session_state.log = []

if "history" not in st.session_state:
    st.session_state.history = []

df = st.session_state.df.copy()

st.title("🤖 AI Assistant")

st.info("Type instructions like: 'fill missing in price with median and lowercase category'")

# ===============================
# 🔹 INPUT
# ===============================
user_input = st.text_area("Enter your instruction")

# ===============================
# 🔹 SIMPLE RULE-BASED AI
# ===============================
def parse_command(text, df):

    text = text.lower()
    actions = []

    # Missing values
    if "missing" in text:
        for col in df.columns:
            if col.lower() in text:
                if "mean" in text:
                    actions.append(("mean", col))
                elif "median" in text:
                    actions.append(("median", col))
                elif "mode" in text:
                    actions.append(("mode", col))

    # Lowercase
    if "lowercase" in text:
        for col in df.select_dtypes(include="object").columns:
            if col.lower() in text:
                actions.append(("lowercase", col))

    # Scaling
    if "scale" in text:
        for col in df.select_dtypes(include=np.number).columns:
            if col.lower() in text:
                actions.append(("scale", col))

    # Remove duplicates
    if "duplicate" in text:
        actions.append(("drop_duplicates", None))

    return actions


# ===============================
# 🔹 APPLY ACTIONS
# ===============================
def apply_actions(df, actions):

    for action, col in actions:

        if action == "mean":
            df[col] = df[col].fillna(df[col].mean())

        elif action == "median":
            df[col] = df[col].fillna(df[col].median())

        elif action == "mode":
            df[col] = df[col].fillna(df[col].mode()[0])

        elif action == "lowercase":
            df[col] = df[col].str.lower()

        elif action == "scale":
            df[col] = (df[col] - df[col].mean()) / df[col].std()

        elif action == "drop_duplicates":
            df = df.drop_duplicates()

    return df


# ===============================
# 🔹 RUN AI
# ===============================
if st.button("🔍 Analyze Instruction"):

    actions = parse_command(user_input, df)

    if not actions:
        st.warning("No valid actions detected")
    else:
        st.subheader("Suggested Actions")
        for a in actions:
            st.write(f"- {a}")

        if st.button("✅ Apply Suggested Actions"):

            st.session_state.history.append(df.copy())

            df = apply_actions(df, actions)

            st.session_state.df = df

            for a in actions:
                st.session_state.log.append(f"AI action: {a}")

            st.success("Actions applied successfully")
            st.rerun()

# ===============================
# 🔹 PREVIEW
# ===============================
st.markdown("---")
st.subheader("Preview After AI")

st.dataframe(df.head())
