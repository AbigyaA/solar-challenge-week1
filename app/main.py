import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Solar Data Dashboard", layout="wide")

st.title("☀️ Solar Irradiance Dashboard")
st.markdown("Compare solar metrics across Benin, Togo, and Sierra Leone")

# Load data
@st.cache_data
def load_data():
    benin = pd.read_csv('app/benin_clean.csv')
    togo = pd.read_csv('app/togo_clean.csv')
    sierra = pd.read_csv('app/sierraleone_clean.csv')

    benin["Country"] = "Benin"
    togo["Country"] = "Togo"
    sierra["Country"] = "Sierra Leone"

    return pd.concat([benin, togo, sierra], ignore_index=True)

df = load_data()

# Sidebar filters
country_options = st.sidebar.multiselect("Select Countries", df["Country"].unique(), default=df["Country"].unique())
metric = st.sidebar.selectbox("Select Metric", ["GHI", "DNI", "DHI"])

filtered_df = df[df["Country"].isin(country_options)]

# Boxplot
st.subheader(f"{metric} Comparison")
fig, ax = plt.subplots()
sns.boxplot(data=filtered_df, x="Country", y=metric, ax=ax)
st.pyplot(fig)

# Mean table
st.subheader(f"Mean {metric} by Country")
st.dataframe(filtered_df.groupby("Country")[metric].mean().round(2).reset_index())

# Bar Chart
st.subheader(f"Average {metric} (Bar Chart)")
avg_metric = filtered_df.groupby("Country")[metric].mean()
st.bar_chart(avg_metric)
