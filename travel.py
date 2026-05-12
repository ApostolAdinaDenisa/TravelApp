import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURARE PAGINA
st.set_page_config(
    page_title="Tourism Map Dashboard",
    layout="wide"
)

st.title("🌍 Tourism Map Charts Dashboard")
st.markdown("Explore tourism statistics around the world")

# LOAD DATA
@st.cache_data
def load_data():
    return pd.read_csv("tourism_data.csv")

df = load_data()

# 🎯 SELECT YEAR
years = sorted(df['year'].unique())
selected_year = st.sidebar.selectbox("Select year", years)

df = df[df['year'] == selected_year]

# 🎯 SELECT COUNTRY
countries = sorted(df['country'].unique())
selected_country = st.sidebar.selectbox("Select a country", countries)

country_df = df[df['country'] == selected_country]

# STATISTICS
total_visitors = country_df['visitors'].sum()
avg_rating = country_df['rating'].mean()
total_cities = country_df['city'].nunique()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Tourists", f"{total_visitors:,}")

with col2:
    st.metric("Average Rating", round(avg_rating, 2))

with col3:
    st.metric("Cities", total_cities)

# 🗺️ MAP
st.subheader("🗺️ Tourism Map")

fig_map = px.scatter_mapbox(
    country_df,
    lat="lat",
    lon="lon",
    size="visitors",
    color="rating",
    hover_name="city",
    hover_data={
        'visitors': True,
        'rating': True
    },
    zoom=3,
    height=600,
    size_max=40
)

fig_map.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0,"t":0,"l":0,"b":0}
)

st.plotly_chart(fig_map, use_container_width=True)

# 📊 TOP 3 CITIES (IMPORTANT UPGRADE)
st.subheader("🏆 Top 3 Cities in Selected Country")

top_3 = country_df.sort_values(by='visitors', ascending=False).head(3)

fig_top3 = px.bar(
    top_3,
    x='city',
    y='visitors',
    color='rating',
    text='visitors',
    title=f"Top 3 Cities in {selected_country} ({selected_year})"
)

fig_top3.update_traces(textposition='outside')

st.plotly_chart(fig_top3, use_container_width=True)

st.dataframe(top_3[['city', 'visitors', 'rating']], use_container_width=True)

# 🏙️ ALL CITIES TABLE
st.subheader("🏙️ All Cities")

cities_table = country_df.sort_values(by='visitors', ascending=False)

st.dataframe(cities_table[['city', 'visitors', 'rating']], use_container_width=True)

# 🥧 PIE CHART
st.subheader("🥧 Tourist Distribution")

fig_pie = px.pie(
    country_df,
    names='city',
    values='visitors'
)

st.plotly_chart(fig_pie, use_container_width=True)

# 🌟 GLOBAL TOP
st.subheader("🌟 Top Global Destinations (Filtered by Year)")

global_top = df.sort_values(by='visitors', ascending=False).head(10)

st.dataframe(global_top[['country','city','visitors','rating']], use_container_width=True)

# 📊 GLOBAL BAR
st.subheader("🏆 Global Top Cities")

fig_global = px.bar(
    global_top,
    x='city',
    y='visitors',
    color='country',
    text='visitors'
)

fig_global.update_traces(textposition='outside')

st.plotly_chart(fig_global, use_container_width=True)

st.markdown("---")
st.markdown("Created with Python, Streamlit and Plotly")
