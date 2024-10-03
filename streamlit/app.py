import streamlit as st
import pandas as pd
import json
import plotly.express as px
import altair as alt

# Enable wide page mode
st.set_page_config(layout="wide")

# Add iframe resizer child, kind of hacky but it works and no graceful way to do it in Streamlit apparently
st.markdown("""<script src="https://cdn.jsdelivr.net/npm/@iframe-resizer/child"></script>""", unsafe_allow_html=True)

# Last updated and introduction
st.markdown("""
            :red[**This page has been last updated at 26.Jun.2024 10:00.**]
            
            With the data that we receive from our participants every week, we can map the spread of flu, COVID-19, other infections and health complaints. We thank the participants for their weekly contributions. Together we can map out the situation in Belgium quickly and at an early stage.
            """)

# Symptoms and health complaints
st.markdown("""
            ## Symptoms and health complaints

            Our participants report every week whether they had one or more symptoms. In the past week we received 733 completed questionnaires. No symptoms were reported in 84.0% of the completed questionnaires. This graph shows the percentage of participants reporting a specific symptom. A combination of symptoms may indicate a specific infectious disease such as flu, COVID-19, RSV, or others.
            """)

df_symptoms = pd.read_csv("../data/en/symptoms.csv")
df_symptoms = df_symptoms[df_symptoms["week"] == "2024/06/19"]

st.altair_chart(
    alt.Chart(df_symptoms).mark_bar().encode(
        x='frequentie',
        y=alt.Y('symptom', sort='-x'),
    ).properties(
        height=500
    ),
    use_container_width=True
)


# Trend line flu-like symptoms
st.markdown("""
            ## Trend line flu-like symptoms

            This graph shows the number of participants per 1000 with flu-like symptoms over time.
            """)

df_flu = pd.read_csv("../data/en/flulike.csv")

df_flu["week"] = df_flu["week"].astype(str)

trendline_flu_fig = px.line(
    df_flu,
    x="week",
    y="incidentie",
    line_group="year",
    color="year",
    labels={"incidentie": "Incidence per 1000 participants", "week": "Week", "year": "Year"},
    markers=True,
    template="plotly_white",
)

trendline_flu_fig.update_traces(
    connectgaps=False
)

trendline_flu_fig.update_traces(
    line=dict(dash="dash"),
    selector=dict(name="2022-2023")
)
trendline_flu_fig.update_traces(
    line=dict(dash="dash"),
    selector=dict(name="2021-2022")
)

st.plotly_chart(trendline_flu_fig)


# Trendline - covid-like symptoms
st.markdown("""
            ## Trend line COVID-like symptoms

            This graph shows the number of participants per 1000 with COVID-like symptoms over time.
            """)

df_covidlike = pd.read_csv("../data/en/covidlike.csv")

trendline_covid_fig = px.line(
    df_covidlike,
    x="week",
    y="incidentie",
    color="year",
    labels={"incidentie": "Incidence per 1000 participants", "week": "Week", "year": "Year"},
    markers=True,
    template="plotly_white",
) 

trendline_covid_fig.update_traces(
    line=dict(dash="dash"),
    selector=dict(name="2022-2023")
)
trendline_covid_fig.update_traces(
    line=dict(dash="dash"),
    selector=dict(name="2021-2022")
)

st.plotly_chart(trendline_covid_fig)

# Map - provinces
st.markdown("""
            ## Our participants

            These graphs show the age, gender and place of residence of our participants. We have 2227 participants, with 40.2% men and 59.4% women. The map shows the number of participants per 1000 inhabitants per province. A darker color indicates a higher participation from residents of the respective province. Not yet a participant? Sign up and help keep an eye on infectious diseases.
            """)
provinces = json.load(open("../data/provinces.geojson"))

df_provinces = pd.read_csv("../data/en/provinces.csv")

map_fig = px.choropleth(
    df_provinces,
    geojson=provinces,
    locations="province",
    featureidkey="properties.name-english",
    labels={"deelnemersper1000": "Participants per 1000 residents", "province": "Province"},
    basemap_visible=False,
    color="deelnemersper1000",
    #color_continuous_scale="pinkyl",
    fitbounds="locations",
    projection="mercator",
    height=600,
)

map_fig.update_layout(margin={"r": 10, "t": 0, "l": 10, "b": 0}, dragmode=False)

st.plotly_chart(map_fig)