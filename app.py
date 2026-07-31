import pandas as pd
import plotly.express as px
import streamlit as st

# Page Configuration
st.set_page_config(page_title="World Happiness Explorer", layout="wide")

# Load Dataset (2019 World Happiness Report)
df = pd.read_csv("2019.csv")

# Create Region Mapping for 2019 Dataset
region_map = {
    'Finland': 'Europe', 'Denmark': 'Europe', 'Norway': 'Europe', 'Iceland': 'Europe',
    'Netherlands': 'Europe', 'Switzerland': 'Europe', 'Sweden': 'Europe', 'New Zealand': 'Oceania',
    'Canada': 'Americas', 'Austria': 'Europe', 'Australia': 'Oceania', 'Costa Rica': 'Americas',
    'Israel': 'Middle East', 'Luxembourg': 'Europe', 'United Kingdom': 'Europe', 'Ireland': 'Europe',
    'Germany': 'Europe', 'Belgium': 'Europe', 'United States': 'Americas', 'Czech Republic': 'Europe',
    'United Arab Emirates': 'Middle East', 'Malta': 'Europe', 'Mexico': 'Americas', 'France': 'Europe',
    'Taiwan': 'Asia', 'Slovakia': 'Europe', 'Saudi Arabia': 'Middle East', 'Guatemala': 'Americas',
    'Spain': 'Europe', 'Panama': 'Americas', 'Brazil': 'Americas', 'Uruguay': 'Americas',
    'Singapore': 'Asia', 'El Salvador': 'Americas', 'Italy': 'Europe', 'Bahrain': 'Middle East',
    'Lithuania': 'Europe', 'Trinidad & Tobago': 'Americas', 'Poland': 'Europe', 'Colombia': 'Americas',
    'Cyprus': 'Europe', 'Nicaragua': 'Americas', 'Kosovo': 'Europe', 'Argentina': 'Americas',
    'Romania': 'Europe', 'Latvia': 'Europe', 'South Korea': 'Asia', 'Japan': 'Asia',
    'Mauritius': 'Africa', 'Uzbekistan': 'Asia', 'Chile': 'Americas', 'Ecuador': 'Americas',
    'Estonia': 'Europe', 'Jamaica': 'Americas', 'Hungary': 'Europe'
}
df['Region'] = df['Country or region'].map(region_map).fillna('Other')

# App Title & Header
st.title("🌍 World Happiness Explorer (All 10 Insights)")
st.markdown("An interactive deep dive into all 10 key drivers of global happiness scores.")

# --- Sidebar Filter ---
st.sidebar.header("Filter Options")
all_regions = df["Region"].unique()
selected_regions = st.sidebar.multiselect("Filter by Region", options=all_regions, default=all_regions)

# Filter Dataset
filtered = df[df["Region"].isin(selected_regions)]

if filtered.empty:
    st.warning("Please select at least one region from the sidebar.")
else:
    # --- Top KPI Summary Metrics ---
    col1, col2, col3 = st.columns(3)
    happiest_country = filtered.loc[filtered["Score"].idxmax(), "Country or region"]
    avg_score = round(filtered["Score"].mean(), 2)
    country_count = len(filtered)

    col1.metric("Happiest Country", happiest_country)
    col2.metric("Average Score", avg_score)
    col3.metric("Countries Analyzed", country_count)

    st.markdown("---")

    # --- Q1: GDP vs Happiness ---
    st.subheader("1. How does GDP per capita impact Happiness?")
    fig1 = px.scatter(
        filtered, x="GDP per capita", y="Score", color="Region",
        hover_name="Country or region", size="Score",
        template="plotly_white", labels={"Score": "Happiness Score"}
    )
    st.plotly_chart(fig1, use_container_width="stretch")

    # --- Q2: Regional Distribution ---
    st.subheader("2. What is the distribution of Happiness Scores across Regions?")
    fig2 = px.box(
        filtered, x="Region", y="Score", color="Region",
        points="all", template="plotly_white", labels={"Score": "Happiness Score"}
    )
    st.plotly_chart(fig2, use_container_width="stretch")

    # --- Q3: Top 10 Countries ---
    st.subheader("3. Which are the Top 10 Happiest Countries?")
    top10 = filtered.nlargest(10, "Score")
    fig3 = px.bar(
        top10, x="Score", y="Country or region", orientation="h",
        color="Score", color_continuous_scale="Viridis", template="plotly_white"
    )
    fig3.update_layout(yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(fig3, use_container_width="stretch")

    # --- Q4: Social Support vs Happiness ---
    st.subheader("4. What role does Social Support play in overall Wellbeing?")
    fig4 = px.scatter(
        filtered, x="Social support", y="Score", color="Region",
        trendline="ols", hover_name="Country or region", template="plotly_white"
    )
    st.plotly_chart(fig4, use_container_width="stretch")

    # --- Q5: Healthy Life Expectancy vs Happiness ---
    st.subheader("5. How strong is the link between Health/Life Expectancy and Happiness?")
    fig5 = px.scatter(
        filtered, x="Healthy life expectancy", y="Score", color="Region",
        hover_name="Country or region", template="plotly_white"
    )
    st.plotly_chart(fig5, use_container_width="stretch")

    # --- Q6: Freedom vs Happiness ---
    st.subheader("6. Does Freedom to Make Life Choices correlate with Happiness?")
    fig6 = px.scatter(
        filtered, x="Freedom to make life choices", y="Score", color="Region",
        hover_name="Country or region", template="plotly_white"
    )
    st.plotly_chart(fig6, use_container_width="stretch")

    # --- Q7: Perceptions of Corruption vs Happiness ---
    st.subheader("7. How does Corruption Perception impact Happiness?")
    fig7 = px.scatter(
        filtered, x="Perceptions of corruption", y="Score", color="Region",
        hover_name="Country or region", template="plotly_white"
    )
    st.plotly_chart(fig7, use_container_width="stretch")

    # --- Q8: Generosity by Region ---
    st.subheader("8. Which regions report the highest levels of Generosity?")
    fig8 = px.bar(
        filtered.groupby("Region", as_index=False)["Generosity"].mean(),
        x="Region", y="Generosity", color="Region", template="plotly_white"
    )
    st.plotly_chart(fig8, use_container_width="stretch")

    # --- Q9: Bottom 10 Countries ---
    st.subheader("9. Which countries face the lowest Happiness Scores?")
    bottom10 = filtered.nsmallest(10, "Score")
    fig9 = px.bar(
        bottom10, x="Score", y="Country or region", orientation="h",
        color="Score", color_continuous_scale="Reds", template="plotly_white"
    )
    fig9.update_layout(yaxis=dict(categoryorder="total descending"))
    st.plotly_chart(fig9, use_container_width="stretch")

    # --- Q10: Top 5 Country Radar Factor Comparison ---
    st.subheader("10. Multidimensional Comparison: Top 5 Countries")
    top5 = filtered.nlargest(5, "Score")
    categories = ["GDP per capita", "Social support", "Healthy life expectancy", "Freedom to make life choices", "Generosity"]
    top5_melted = top5.melt(id_vars="Country or region", value_vars=categories, var_name="Factor", value_name="Value")
    fig10 = px.line_polar(
        top5_melted, r="Value", theta="Factor", color="Country or region",
        line_close=True, template="plotly_white"
    )
    st.plotly_chart(fig10, use_container_width="stretch")