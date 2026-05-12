import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# CONFIGURARE PAGINA
st.set_page_config(
    page_title="Tourism Map Dashboard",
    layout="wide"
)

# TITLU
st.title("🌍 Tourism Map Charts Dashboard")
st.markdown("Explore tourism statistics around the world")

# INCARCARE DATE
@st.cache_data

def load_data():
    return pd.read_csv("tourism_data.csv")


df = load_data()

# SELECTARE TARA

countries = sorted(df['country'].unique())

selected_country = st.sidebar.selectbox(
    "Select a country",
    countries
)

# FILTRARE DATE
country_df = df[df['country'] == selected_country]

# STATISTICI

total_visitors = country_df['visitors'].sum()
avg_rating = country_df['rating'].mean()
total_cities = country_df['city'].count()
# CARDS
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Tourists", f"{total_visitors:,}")

with col2:
    st.metric("Average Rating", round(avg_rating, 2))

with col3:
    st.metric("Popular Cities", total_cities)

# HARTA
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
        'rating': True,
        'lat': False,
        'lon': False
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

# TABEL
st.subheader("🏙️ Most Visited Cities")

cities_table = country_df[[
    'city',
    'visitors',
    'rating'
]].sort_values(by='visitors', ascending=False)

st.dataframe(cities_table, use_container_width=True)

# BAR CHART
st.subheader("📊 Visitors by City")

fig_bar = px.bar(
    country_df.sort_values(by='visitors', ascending=False),
    x='city',
    y='visitors',
    color='rating',
    text='visitors'
)

fig_bar.update_traces(textposition='outside')

st.plotly_chart(fig_bar, use_container_width=True)

# PIE CHART
st.subheader("🥧 Tourist Distribution")

fig_pie = px.pie(
    country_df,
    names='city',
    values='visitors'
)

st.plotly_chart(fig_pie, use_container_width=True)

# TOP DESTINATII GLOBALE
st.subheader("🌟 Top Global Destinations")

best_destinations = df.sort_values(
    by='visitors',
    ascending=False
).head(10)

st.dataframe(
    best_destinations[[
        'country',
        'city',
        'visitors',
        'rating'
    ]],
    use_container_width=True
)

# TOP CITIES (GLOBAL)
st.subheader("🏆 Top Most Visited Cities (Global)")

top_cities = df.sort_values(by='visitors', ascending=False).head(10)

fig_top_cities = px.bar(
    top_cities,
    x='city',
    y='visitors',
    color='country',
    text='visitors'
)
fig_top_cities.update_traces(textposition='outside')

st.plotly_chart(fig_top_cities, use_container_width=True)

st.dataframe(
    top_cities[[
        'country',
        'city',
        'visitors',
        'rating'
    ]],
    use_container_width=True
)

# FOOTER
st.markdown("---")
st.markdown("Created with Python, Streamlit and Plotly")
