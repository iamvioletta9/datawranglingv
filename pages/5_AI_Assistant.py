import streamlit as st
import pandas as pd
import re

# ===============================
# SESSION
# ===============================
if "df" not in st.session_state:
    st.warning("Upload data first")
    st.stop()

if "log" not in st.session_state:
    st.session_state.log = []

if "history" not in st.session_state:
    st.session_state.history = []

df = st.session_state.df.copy()

st.title("🤖 AI Data Assistant")

st.info("Type a command like: 'fill missing price with median and lowercase category'")

user_input = st.text_area("Enter instruction")

# ===============================
# SIMPLE NLP PARSER (RULE-BASED)
# ===============================
def parse_command(text, df):

    actions = []

    text = text.lower()

    # ---- Missing values ----
    if "fill" in text and "missing" in text:
        for col in df.columns:
            if col.lower() in text:

                if "mean" in text:
                    actions.append(("fill_mean", col))
                elif "median" in text:
                    actions.append(("fill_median", col))
                elif "mode" in text:
                    actions.append(("fill_mode", col))

    # ---- Lowercase categorical ----
    if "lowercase" in text:
        for col in df.select_dtypes(include="object").columns:
            if col.lower() in text:
                actions.append(("lowercase", col))

    # ---- Drop duplicates ----
    if "remove duplicates" in text:
        actions.append(("drop_duplicates", None))

    # ---- Scaling ----
    if "scale" in text:
        for col in df.select_dtypes(include="number").columns:
            if col.lower() in text:
                actions.append(("scale", col))

    return actions


# ===============================
# APPLY ACTIONS
# ===============================
def apply_actions(df, actions):

    for action, col in actions:

        if action == "fill_mean":
            df[col] = df[col].fillna(df[col].mean())

        elif action == "fill_median":
            df[col] = df[col].fillna(df[col].median())

        elif action == "fill_mode":
            df[col] = df[col].fillna(df[col].mode()[0])

        elif action == "lowercase":
            df[col] = df[col].str.lower()

        elif action == "drop_duplicates":
            df = df.drop_duplicates()

        elif action == "scale":
            df[col] = (df[col] - df[col].mean()) / df[col].std()

    return df


# ===============================
# RUN AI
# ===============================
if st.button("Analyze Command"):

    actions = parse_command(user_input, df)

    if not actions:
        st.warning("No valid actions detected")
    else:
        st.write("### Suggested Actions:")
        for a in actions:
            st.write(f"- {a}")

        # CONFIRMATION (VERY IMPORTANT FOR MARKS)
        if st.button("Apply Actions"):

            st.session_state.history.append(df.copy())

            df = apply_actions(df, actions)

            st.session_state.df = df

            for a in actions:
                st.session_state.log.append(f"AI: {a}")

            st.success("Actions applied successfully")
            st.rerun()

# ===============================
# PREVIEW
# ===============================
st.subheader("Preview")
st.dataframe(df.head())
