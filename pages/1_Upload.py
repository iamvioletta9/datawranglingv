# ================= UPLOAD PAGE =================
import streamlit as st
import pandas as pd
import numpy as np
import io

# ── FILE UPLOAD ───────────────────────────────────────────────────────────────
file = st.file_uploader("📁 Upload your dataset", type=["csv", "xlsx", "json"],
                         help="CSV, Excel (.xlsx), or JSON")

if file is not None:
    try:
        b = file.read()
        if file.name.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(b))
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(b))
        elif file.name.endswith(".json"):
            df = pd.read_json(io.BytesIO(b))
        else:
            st.error("Unsupported file type")
            st.stop()

        st.session_state.df = df
        st.session_state.last_file = file.name

        st.success(f"✅ **{file.name}** — {df.shape[0]:,} rows x {df.shape[1]} columns")

    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

if "df" not in st.session_state or st.session_state.df is None:
    st.info("💡 Upload a file above or try one of the sample datasets from the `sample_data/` folder.")
    st.stop()

# ── OVERVIEW ──────────────────────────────────────────────────────────────────
df = st.session_state.df
st.subheader("📊 Dataset Overview")

total_missing = int(df.isnull().sum().sum())
total_cells   = df.shape[0] * df.shape[1]
missing_pct   = round(total_missing / total_cells * 100, 2) if total_cells > 0 else 0

dupes         = int(df.duplicated().sum())
dupes_pct     = round(dupes / df.shape[0] * 100, 2) if df.shape[0] > 0 else 0

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Rows",          f"{df.shape[0]:,}")
m2.metric("Columns",       df.shape[1])
m3.metric("Duplicates",    f"{dupes:,} ({dupes_pct:.2f}%)")
m4.metric("Missing Cells", f"{total_missing:,}")
m5.metric("Missing %",     f"{missing_pct:.2f}%")

# ── Missing Values by Column ─────────────────────────────────────────────────
st.markdown("---")
st.write("### Missing Values by Column")
mv = pd.DataFrame({
    "Missing Count": df.isnull().sum(),
    "Missing %": (df.isnull().sum() / len(df) * 100)
})
mv["Missing %"] = mv["Missing %"].map(lambda x: round(x, 2))
mv_f = mv[mv["Missing Count"] > 0]
if mv_f.empty:
    st.success("No missing values found!")
else:
    st.dataframe(mv_f.style.background_gradient(cmap="Reds", subset=["Missing %"])
                 .format({"Missing %": "{:.2f}"}), use_container_width=True)

# ── Column Info ───────────────────────────────────────────────────────────────
st.markdown("---")
st.write("### Column Info")
info_df = pd.DataFrame({
    "Column":   df.columns,
    "Type":     df.dtypes.astype(str).values,
    "Non-Null": df.notnull().sum().values,
    "Unique":   [df[c].nunique() for c in df.columns],
    "Sample":   [str(df[c].dropna().iloc[0]) if not df[c].dropna().empty else "N/A" for c in df.columns]
}).reset_index(drop=True)
st.dataframe(info_df, use_container_width=True)

# ── Duplicates Preview ────────────────────────────────────────────────────────
if dupes > 0:
    st.markdown("---")
    st.write("### Duplicate Rows Preview")
    st.dataframe(df[df.duplicated()].head(10), use_container_width=True)

# ── Summary Statistics ─────────────────────────────────────────────────────────
st.markdown("---")
st.write("### Summary Statistics")
num_cols_list = df.select_dtypes(include=np.number).columns.tolist()
cat_cols_list = df.select_dtypes(include=["object","category"]).columns.tolist()

if num_cols_list:
    st.markdown("**Numeric Columns**")
    num_desc = df[num_cols_list].describe().T
    num_desc.insert(0, "unique", [df[c].nunique() for c in num_cols_list])
    num_desc.insert(0, "missing", [int(df[c].isnull().sum()) for c in num_cols_list])
    st.dataframe(num_desc.style.format(precision=4), use_container_width=True)

if cat_cols_list:
    st.markdown("**Categorical Columns**")
    cat_rows = []
    for c in cat_cols_list:
        vc = df[c].value_counts()
        cat_rows.append({
            "column": c,
            "count": int(df[c].notnull().sum()),
            "missing": int(df[c].isnull().sum()),
            "unique": int(df[c].nunique()),
            "top": str(vc.index[0]) if len(vc) > 0 else "N/A",
            "freq": int(vc.iloc[0]) if len(vc) > 0 else 0,
            "freq %": round(vc.iloc[0] / len(df) * 100, 2) if len(vc) > 0 else 0,
        })
    st.dataframe(pd.DataFrame(cat_rows).set_index("column"), use_container_width=True)

# ── Data Preview ──────────────────────────────────────────────────────────────
st.markdown("---")
st.write("### Data Preview")
n_rows = st.slider("Rows to preview", 5, 50, 10)
st.dataframe(df.head(n_rows), use_container_width=True)
