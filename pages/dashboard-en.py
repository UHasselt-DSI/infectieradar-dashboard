from dash import dcc, html, register_page
import plotly.express as px
import pandas as pd
import json

register_page(__name__, path='/en')

colors = {"background": "#FFFFFF", "text": "#101010", "warning-text": "#FF4136"}

# Bar - symptoms
df_symptoms = pd.read_csv("data/en/symptoms.csv")

symptom_fig = px.bar(
    df_symptoms,
    x="frequentie",
    y="symptom",
    orientation="h",
    labels={"frequentie": "Frequency (%)", "symptom": "Symptom"},
    color="frequentie",
    color_continuous_scale="pinkyl",
    template="plotly_white",
    height=600
)

symptom_fig.update_layout(yaxis={"categoryorder": "total ascending"})

weeks = ([x for x in range(25, 53)] + [x for  x in range(1, 25)])


# If actual data is available, read in dataframe and append missing weeks
# Trendline - flu-like symptoms
df_flulike = pd.read_csv("data/en/flulike.csv")

df_flulike["week"] = df_flulike["week"].astype(str)


trendline_flu_fig = px.line(
    df_flulike,
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

# Trendline - covid-like symptoms
df_covidlike = pd.read_csv("data/en/covidlike.csv")

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

# Map - provinces
provinces = json.load(open("data/provinces.geojson"))

df_provinces = pd.read_csv("data/en/provinces.csv")

map_fig = px.choropleth(
    df_provinces,
    geojson=provinces,
    locations="province",
    featureidkey="properties.name-english",
    labels={"deelnemersper1000": "Participants per 1000 residents", "province": "Province"},
    basemap_visible=False,
    color="deelnemersper1000",
    color_continuous_scale="pinkyl",
    fitbounds="locations",
    projection="mercator",
    height=600,
)

map_fig.update_layout(margin={"r": 10, "t": 0, "l": 10, "b": 0}, dragmode=False)



# Bar - sex and age group
df_sexage = pd.read_csv("data/en/sexage.csv")

# y-axis = age groups, x-axis = count, double sided with gender, bar chart
sexage_fig = px.bar(
    df_sexage,
    x="count",
    y="age",
    orientation="h",
    color="sex",
    labels={"count": "# of participants", "age": "Age group", "sex": "Sex"},
    template="plotly_white",
)

layout = html.Div(
    children=[
        html.Div(children=[
            html.P(
                children="This page has been last updated at 26.Jun.2024 10:00.",
                style={"textAlign": "left", "color": colors["warning-text"]},
            ),
            html.P(
                children="""
                    With the data that we receive from our participants every week, we can map the spread of flu, COVID-19, other infections and health complaints. We thank the participants for their weekly contributions. Together we can map out the situation in Belgium quickly and at an early stage.
                """,
                style={"textAlign": "left", "color": colors["text"]},
            )]
        ),
        html.Div(
            children=[
                html.H2(
                    children="Symptoms and health complaints",
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                html.P(
                    children="""
                        Our participants report every week whether they had one or more symptoms. In the past week we received 733 completed questionnaires. No symptoms were reported in 84.0% of the completed questionnaires. This graph shows the percentage of participants reporting a specific symptom. A combination of symptoms may indicate a specific infectious disease such as flu, COVID-19, RSV, or others.
                    """,
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                dcc.Loading(
                    [dcc.Graph(id="symptoms", figure=symptom_fig)],
                    overlay_style={"visibility":"visible", "filter": "blur(2px)"},
                    type="circle"
                )
            ],
            style={"paddingTop": "1rem"}
        ),
        html.Div(
            children=[
                html.H2(
                    children="Trend line flu-like symptoms",
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                html.P(
                    children="""
                        This graph shows the number of participants per 1000 with flu-like symptoms over time.
                    """,
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                dcc.Graph(id="trendline_flu", figure=trendline_flu_fig)
            ],
            style={"paddingTop": "1rem"}
        ),
        html.Div(
            children=[
                html.H2(
                    children="Trend line COVID-19 like symptoms",
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                html.P(
                    children="""
                        This graph shows the number of participants per 1000 with COVID-19-like symptoms over time.
                    """,
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                dcc.Graph(id="trendline_covid", figure=trendline_covid_fig)
            ],
            style={"paddingTop": "1rem"}
        ),
        html.Div(
            children=[
                html.H2(
                    children="Our participants",
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                html.P(
                    children="""
                        These graphs show the age, gender and place of residence of our participants. We have 2227 participants, with 40.2% men and 59.4% women. The map shows the number of participants per 1000 inhabitants per province. A darker color indicates a higher participation from residents of the respective province. Not yet a participant? Sign up and help keep an eye on infectious diseases.
                    """,
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                dcc.Graph(id="province-map", figure=map_fig, style={"margin": "auto", "width": "100%"}),
                dcc.Graph(id="sexage", figure=sexage_fig),
            ],  
            style={"paddingTop": "1rem"}
        )
    ],
)