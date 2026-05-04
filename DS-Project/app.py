import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================
# PAGE SETTINGS
# ==============================
st.set_page_config(page_title="India Census Dashboard", layout="wide")

st.title("📊 India Census 2011 Dashboard")
st.write("Data Cleaning & Visualization Project")

# ==============================
# LOAD DATA
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("Table_2A_State_Uts.csv")
    df.columns = ['Category', 'Region', 'Population', 'Growth_Rate', 'Density']
    return df

df = load_data()

# ==============================
# DATA CLEANING
# ==============================
df.drop_duplicates(inplace=True)

df['Population'].fillna(df['Population'].median(), inplace=True)
df['Growth_Rate'].fillna(df['Growth_Rate'].mean(), inplace=True)
df['Density'].fillna(df['Density'].median(), inplace=True)

# ==============================
# SIDEBAR FILTER
# ==============================
st.sidebar.header("Filter Data")
category = st.sidebar.selectbox("Select Category", ["All", "State", "Union Territory"])

if category != "All":
    df = df[df['Category'] == category]

# ==============================
# METRICS
# ==============================
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Total Regions", len(df))
col2.metric("Avg Growth Rate", f"{df['Growth_Rate'].mean():.2f}%")
col3.metric("Avg Density", f"{df['Density'].mean():.2f}")

# ==============================
# TOP 10 POPULATION
# ==============================
st.subheader("🏆 Top 10 Regions by Population")

top10 = df.sort_values(by='Population', ascending=False).head(10)

fig1, ax1 = plt.subplots()
sns.barplot(x='Population', y='Region', data=top10, ax=ax1)
st.pyplot(fig1)

# ==============================
# GROWTH RATE DISTRIBUTION
# ==============================
st.subheader("📈 Growth Rate Distribution")

fig2, ax2 = plt.subplots()
sns.histplot(df['Growth_Rate'], bins=10, ax=ax2)
st.pyplot(fig2)

# ==============================
# SCATTER PLOT
# ==============================
st.subheader("🔵 Growth Rate vs Density")

fig3, ax3 = plt.subplots()
sns.scatterplot(x='Growth_Rate', y='Density', size='Population', data=df, ax=ax3)
st.pyplot(fig3)

# ==============================
# HEATMAP
# ==============================
st.subheader("🔥 Correlation Heatmap")

corr = df[['Population', 'Growth_Rate', 'Density']].corr()

fig4, ax4 = plt.subplots()
sns.heatmap(corr, annot=True, ax=ax4)
st.pyplot(fig4)

# ==============================
# INSIGHTS
# ==============================
st.subheader("🧠 Key Insights")

st.write(f"Most populous region: {df.loc[df['Population'].idxmax(), 'Region']}")
st.write(f"Fastest growth: {df.loc[df['Growth_Rate'].idxmax(), 'Region']}")
st.write(f"Highest density: {df.loc[df['Density'].idxmax(), 'Region']}")

# ==============================
# DATA TABLE
# ==============================
st.subheader("📄 Data Table")
st.dataframe(df)
