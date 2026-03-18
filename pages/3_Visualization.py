import streamlit as st
import plotly.express as px
import pandas as pd

# ===============================
# 🔹 SESSION STATE
# ===============================
if "df" not in st.session_state:
    st.session_state.df = None

st.title("📊 Advanced Visualization Builder")

if st.session_state.df is None:
    st.warning("Upload data first")
    st.stop()

df = st.session_state.df.copy()

# ===============================
# 🔥 FILTERS
# ===============================
st.subheader("Filters")

filter_col = st.selectbox("Filter column", df.columns)
unique_vals = df[filter_col].astype(str).dropna().unique()

selected_vals = st.multiselect("Select values", unique_vals)

if selected_vals:
    df = df[df[filter_col].astype(str).isin(selected_vals)]

# Safety check
if df.empty:
    st.warning("No data available after filtering")
    st.stop()

# ===============================
# 🔥 PRE-BUILT INSIGHTS (DYNAMIC)
# ===============================
st.subheader("📌 Key Insights from Dataset")

categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
numeric_cols = df.select_dtypes(include="number").columns.tolist()

insight = st.selectbox(
    "Choose an insight",
    [
        "Most frequent category",
        "Distribution of numeric variable",
        "Top categories by numeric value",
        "Correlation heatmap"
    ]
)

# 1️⃣ MOST FREQUENT CATEGORY
if insight == "Most frequent category":

    if len(categorical_cols) == 0:
        st.warning("No categorical columns available")
    else:
        col = st.selectbox("Select column", categorical_cols)

        counts = df[col].value_counts().reset_index()
        counts.columns = [col, "Count"]

        fig = px.bar(counts, x=col, y="Count",
                     title=f"Most Frequent Values in {col}")
        st.plotly_chart(fig)

# 2️⃣ NUMERIC DISTRIBUTION
elif insight == "Distribution of numeric variable":

    if len(numeric_cols) == 0:
        st.warning("No numeric columns available")
    else:
        col = st.selectbox("Select column", numeric_cols)

        fig = px.histogram(df, x=col,
                           title=f"Distribution of {col}")
        st.plotly_chart(fig)

# 3️⃣ TOP CATEGORY VS NUMERIC
elif insight == "Top categories by numeric value":

    if len(categorical_cols) == 0 or len(numeric_cols) == 0:
        st.warning("Need both categorical and numeric columns")
    else:
        cat = st.selectbox("Category", categorical_cols)
        num = st.selectbox("Numeric value", numeric_cols)

        grouped = df.groupby(cat)[num].mean().reset_index()

        fig = px.bar(grouped, x=cat, y=num,
                     title=f"{num} by {cat}")
        st.plotly_chart(fig)

# 4️⃣ HEATMAP
elif insight == "Correlation heatmap":

    if len(numeric_cols) < 2:
        st.warning("Not enough numeric columns for heatmap")
    else:
        corr = df[numeric_cols].corr()

        fig = px.imshow(corr, title="Correlation Matrix")
        st.plotly_chart(fig)

# ===============================
# 🔧 CUSTOM BUILDER
# ===============================
st.markdown("---")
st.subheader("🔧 Custom Visualization Builder")

chart = st.selectbox(
    "Chart Type",
    ["Histogram", "Scatter", "Box", "Line", "Bar", "Heatmap"]
)

agg = st.selectbox("Aggregation", ["None", "Mean", "Sum", "Count"])

# --- BAR ---
if chart == "Bar":

    if len(categorical_cols) == 0 or len(numeric_cols) == 0:
        st.warning("Need categorical and numeric columns")
        st.stop()

    x = st.selectbox("Category", categorical_cols)
    y = st.selectbox("Value", numeric_cols)

    top_n = st.slider("Top N", 5, 50, 10)

    grouped = df.groupby(x)[y]

    if agg == "Mean":
        grouped = grouped.mean()
    elif agg == "Sum":
        grouped = grouped.sum()
    elif agg == "Count":
        grouped = grouped.count()
    else:
        grouped = grouped.mean()

    grouped = grouped.nlargest(top_n).reset_index()

    fig = px.bar(grouped, x=x, y=y, title=f"{y} by {x}")
    st.plotly_chart(fig)

# --- SCATTER ---
elif chart == "Scatter":

    if len(numeric_cols) < 2:
        st.warning("Need at least 2 numeric columns")
        st.stop()

    x = st.selectbox("X", numeric_cols)
    y = st.selectbox("Y", numeric_cols)
    color = st.selectbox("Color (optional)", [None] + list(df.columns))

    fig = px.scatter(df, x=x, y=y, color=color,
                     title=f"{y} vs {x}")
    st.plotly_chart(fig)

# --- HISTOGRAM ---
elif chart == "Histogram":

    col = st.selectbox("Column", df.columns)

    fig = px.histogram(df, x=col,
                       title=f"{col} Distribution")
    st.plotly_chart(fig)

# --- BOX ---
elif chart == "Box":

    if len(numeric_cols) == 0:
        st.warning("No numeric columns available")
        st.stop()

    col = st.selectbox("Column", numeric_cols)

    fig = px.box(df, y=col,
                 title=f"{col} Boxplot")
    st.plotly_chart(fig)

# --- LINE ---
elif chart == "Line":

    if len(numeric_cols) == 0:
        st.warning("No numeric columns available")
        st.stop()

    x = st.selectbox("X", df.columns)
    y = st.selectbox("Y", numeric_cols)

    fig = px.line(df, x=x, y=y,
                  title=f"{y} over {x}")
    st.plotly_chart(fig)

# --- HEATMAP ---
elif chart == "Heatmap":

    if len(numeric_cols) < 2:
        st.warning("Not enough numeric columns for correlation heatmap")
        st.stop()

    corr = df[numeric_cols].corr()

    fig = px.imshow(corr,
                    title="Correlation Matrix")
    st.plotly_chart(fig)
