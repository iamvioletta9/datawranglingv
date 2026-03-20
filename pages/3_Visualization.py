import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

df = st.session_state.df

st.title("📊 Visualization Builder")

num_cols = df.select_dtypes(include=np.number).columns
cat_cols = df.select_dtypes(include="object").columns

chart = st.selectbox("Chart type",
                     ["Histogram","Scatter","Line","Bar","Box","Heatmap"])

if chart == "Histogram":
    col = st.selectbox("Column", num_cols)

    fig, ax = plt.subplots()
    ax.hist(df[col])
    st.pyplot(fig)

elif chart == "Scatter":
    x = st.selectbox("X", num_cols)
    y = st.selectbox("Y", num_cols)
    st.plotly_chart(px.scatter(df, x=x, y=y))

elif chart == "Line":
    x = st.selectbox("X", df.columns)
    y = st.selectbox("Y", num_cols)
    st.plotly_chart(px.line(df, x=x, y=y))

elif chart == "Bar":
    cat = st.selectbox("Category", cat_cols)
    num = st.selectbox("Value", num_cols)
    grouped = df.groupby(cat)[num].mean().reset_index()
    st.plotly_chart(px.bar(grouped, x=cat, y=num))

elif chart == "Box":
    col = st.selectbox("Column", num_cols)
    st.plotly_chart(px.box(df, y=col))

elif chart == "Heatmap":
    st.plotly_chart(px.imshow(df[num_cols].corr()))
