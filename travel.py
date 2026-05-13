import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Europe Tourism Analytics 2025",
    page_icon="🌍",
    layout="wide"
)
df = pd.read_csv("tourism_data.csv")

# CREATE RANK

df["Rank"] = df["Tourism_Nights_Millions"].rank(
    ascending=False,
    method="dense"
).astype(int)

# SIDEBAR

st.sidebar.title("Filters")

selected_country = st.sidebar.selectbox(
    "Choose a European country",
    sorted(df["Country"].unique())
)

min_tourism = st.sidebar.slider(
    "Minimum tourism nights (millions)",
    min_value=int(df["Tourism_Nights_Millions"].min()),
    max_value=int(df["Tourism_Nights_Millions"].max()),
    value=10
)

# Filter dataframe
filtered_df = df[
    df["Tourism_Nights_Millions"] >= min_tourism
]

# TITLE
st.title(" Europe Tourism Analytics 2025")

st.markdown("""
Interactive tourism dashboard for European countries using map charts and data visualization.
""")

# SELECTED COUNTRY DATA

country_data = df[
    df["Country"] == selected_country
].iloc[0]

# KPI SECTION

st.subheader(f"📌 {selected_country} Statistics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Tourism Nights",
    f"{country_data['Tourism_Nights_Millions']} M"
)

col2.metric(
    "European Rank",
    f"#{country_data['Rank']}"
)

# Tourism category
if country_data["Tourism_Nights_Millions"] > 300:
    category = "Very High"
elif country_data["Tourism_Nights_Millions"] > 100:
    category = "High"
elif country_data["Tourism_Nights_Millions"] > 40:
    category = "Medium"
else:
    category = "Low"

col3.metric(
    "Tourism Level",
    category
)

# COUNTRY INFO

st.info(
    f"{selected_country} recorded approximately "
    f"{country_data['Tourism_Nights_Millions']} million "
    f"tourism nights in 2025."
)

# MAP CHART

st.subheader(" Europe Tourism Map")

map_fig = px.choropleth(
    filtered_df,
    locations="ISO_Code",
    color="Tourism_Nights_Millions",
    hover_name="Country",
    color_continuous_scale="Viridis",
    scope="europe",
    labels={
        "Tourism_Nights_Millions": "Tourism Nights (Millions)"
    }
)

map_fig.update_layout(
    height=650
)

st.plotly_chart(
    map_fig,
    use_container_width=True
)

# TOP 10 COUNTRIES

st.subheader(" Top European Tourist Destinations")

top10 = df.sort_values(
    by="Tourism_Nights_Millions",
    ascending=False
).head(10)

bar_fig = px.bar(
    top10,
    x="Country",
    y="Tourism_Nights_Millions",
    text="Tourism_Nights_Millions",
    color="Tourism_Nights_Millions"
)

bar_fig.update_layout(
    xaxis_title="Country",
    yaxis_title="Tourism Nights (Millions)",
    height=500
)

st.plotly_chart(
    bar_fig,
    use_container_width=True
)

# FULL TABLE

st.subheader(" Full Dataset")

st.dataframe(
    df.sort_values(
        by="Rank"
    ),
    use_container_width=True
)


# AUTOMATIC INSIGHTS

st.subheader("📈 Tourism Insights")

most_visited = df.sort_values(
    by="Tourism_Nights_Millions",
    ascending=False
).iloc[0]

least_visited = df.sort_values(
    by="Tourism_Nights_Millions",
    ascending=True
).iloc[0]

average = round(
    df["Tourism_Nights_Millions"].mean(),
    2
)

st.success(
    f"{most_visited['Country']} is the most visited "
    f"country in Europe with "
    f"{most_visited['Tourism_Nights_Millions']} million tourism nights."
)

st.warning(
    f"{least_visited['Country']} has the lowest tourism activity "
    f"with only {least_visited['Tourism_Nights_Millions']} million tourism nights."
)

st.write(
    f"The average number of tourism nights in Europe is "
    f"{average} million."
)

# FOOTER
st.markdown("---")

st.caption(
    "Data inspired by Eurostat tourism statistics."
)
