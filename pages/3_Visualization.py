import streamlit as st
import plotly.express as px
import pandas as pd

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
# 🔥 PRE-BUILT INSIGHTS
# ===============================
st.subheader("📌 Key Insights from Dataset")

insight = st.selectbox(
    "Choose a question",
    [
        "Most used room",
        "Classes per day",
        "Credit distribution",
        "Most frequent course"
    ]
)

# 1️⃣ MOST USED ROOM
if insight == "Most used room":
    if "Room" in df.columns:
        room_counts = df["Room"].value_counts().reset_index()
        room_counts.columns = ["Room", "Count"]

        fig = px.bar(room_counts, x="Room", y="Count",
                     title="Most Used Rooms")
        st.plotly_chart(fig)
    else:
        st.warning("No 'Room' column found")

# 2️⃣ CLASSES PER DAY
elif insight == "Classes per day":
    if "Day" in df.columns:
        day_counts = df["Day"].value_counts().reset_index()
        day_counts.columns = ["Day", "Count"]

        fig = px.bar(day_counts, x="Day", y="Count",
                     title="Classes per Day")
        st.plotly_chart(fig)
    else:
        st.warning("No 'Day' column found")

# 3️⃣ CREDIT DISTRIBUTION
elif insight == "Credit distribution":
    if "Cred." in df.columns:
        cred = df["Cred."].astype(str).str.replace(",", ".")
        cred = pd.to_numeric(cred, errors="coerce")

        fig = px.histogram(cred, title="Credit Distribution")
        st.plotly_chart(fig)
    else:
        st.warning("No 'Cred.' column found")

# 4️⃣ MOST FREQUENT COURSE
elif insight == "Most frequent course":
    if "Code" in df.columns:
        course_counts = df["Code"].value_counts().reset_index()
        course_counts.columns = ["Course", "Count"]

        fig = px.bar(course_counts, x="Course", y="Count",
                     title="Most Frequent Courses")
        st.plotly_chart(fig)
    else:
        st.warning("No 'Code' column found")

# ===============================
# 🔧 CUSTOM BUILDER
# ===============================
st.markdown("---")
st.subheader("🔧 Custom Visualization Builder")

chart = st.selectbox(
    "Chart Type",
    ["Histogram", "Scatter", "Box", "Line", "Bar", "Heatmap"]
)

num = df.select_dtypes(include="number").columns

agg = st.selectbox("Aggregation", ["None", "Mean", "Sum", "Count"])

# --- BAR ---
if chart == "Bar":
    x = st.selectbox("Category", df.columns)
    y = st.selectbox("Value", num)

    if len(num) == 0:
        st.warning("No numeric columns available")
        st.stop()

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
    if len(num) < 2:
        st.warning("Need at least 2 numeric columns")
        st.stop()

    x = st.selectbox("X", num)
    y = st.selectbox("Y", num)
    color = st.selectbox("Color (optional)", [None] + list(df.columns))

    fig = px.scatter(df, x=x, y=y, color=color,
                     title=f"{y} vs {x}")
    st.plotly_chart(fig)

# --- HISTOGRAM (FIXED) ---
elif chart == "Histogram":
    col = st.selectbox("Column", df.columns)

    fig = px.histogram(df, x=col, title=f"{col} Distribution")
    st.plotly_chart(fig)

# --- BOX ---
elif chart == "Box":
    if len(num) == 0:
        st.warning("No numeric columns available")
        st.stop()

    col = st.selectbox("Column", num)

    fig = px.box(df, y=col, title=f"{col} Boxplot")
    st.plotly_chart(fig)

# --- LINE ---
elif chart == "Line":
    if len(num) == 0:
        st.warning("No numeric columns available")
        st.stop()

    x = st.selectbox("X", df.columns)
    y = st.selectbox("Y", num)

    fig = px.line(df, x=x, y=y, title=f"{y} over {x}")
    st.plotly_chart(fig)

# --- HEATMAP ---
elif chart == "Heatmap":

    num_df = df.select_dtypes(include="number")

    if num_df.shape[1] < 2:
        st.warning("Not enough numeric columns for correlation heatmap")
        st.stop()

    corr = num_df.corr()

    fig = px.imshow(corr, title="Correlation Matrix")
    st.plotly_chart(fig)
