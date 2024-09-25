from dash import dcc, html, register_page
import plotly.express as px
import pandas as pd
import json

register_page(__name__, path='/nl-be')

colors = {"background": "#FFFFFF", "text": "#101010", "warning-text": "#FF4136"}

# Bar - symptoms
df_symptoms = pd.read_csv("data/nl/symptoms.csv")

symptom_fig = px.bar(
    df_symptoms,
    x="frequentie",
    y="symptom",
    orientation="h",
    labels={"frequentie": "Frequentie (%)", "symptom": "Symptoom"},
    color="frequentie",
    color_continuous_scale="pinkyl",
    template="plotly_white",
    height=600
)

symptom_fig.update_layout(yaxis={"categoryorder": "total ascending"})



# Trendline - flu-like symptoms
df_flulike = pd.read_csv("data/nl/flulike.csv")


trendline_flu_fig = px.line(
    df_flulike,
    x="week",
    y="incidentie",
    color="year",
    labels={"incidentie": "Incidentie per 1000 deelnemers", "week": "Week", "year": "Jaar"},
    markers=True,
    template="plotly_white",
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
df_covidlike = pd.read_csv("data/nl/covidlike.csv")

trendline_covid_fig = px.line(
    df_covidlike,
    x="week",
    y="incidentie",
    color="year",
    labels={"incidentie": "Incidentie per 1000 deelnemers", "week": "Week", "year": "Jaar"},
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

df_provinces = pd.read_csv("data/nl/provinces.csv")

map_fig = px.choropleth(
    df_provinces,
    geojson=provinces,
    locations="province",
    featureidkey="properties.name-dutch",
    labels={"deelnemersper1000": "Deelnemers per 1000 inwoners", "province": "Provincie"},
    basemap_visible=False,
    color="deelnemersper1000",
    color_continuous_scale="pinkyl",
    fitbounds="locations",
    projection="mercator",
    height=600,
)

map_fig.update_layout(margin={"r": 10, "t": 0, "l": 10, "b": 0}, dragmode=False)



# Bar - sex and age group
df_sexage = pd.read_csv("data/nl/sexage.csv")

# y-axis = age groups, x-axis = count, double sided with gender, bar chart
sexage_fig = px.bar(
    df_sexage,
    x="count",
    y="age",
    orientation="h",
    color="sex",
    labels={"count": "Aantal deelnemers", "age": "Leeftijdsgroep", "sex": "Geslacht"},
    template="plotly_white",
)

layout = html.Div(
    children=[
        html.Div(children=[
            html.P(
                children="Deze pagina is voor het laatst aangepast op 26.Jun.2024 10:00.",
                style={"textAlign": "left", "color": colors["warning-text"]},
            ),
            html.P(
                children="""
                Met de gegevens die we iedere week via onze deelnemers verkrijgen, kunnen we de verspreiding van griep, COVID-19, andere infecties en gezondheidsklachten in kaart brengen. We danken de deelnemers voor hun wekelijkse bijdragen. Samen kunnen we snel en vroegtijdig de situatie in België in kaart brengen.
                """,
                style={"textAlign": "left", "color": colors["text"]},
            )]
        ),
        html.Div(
            children=[
                html.H2(
                    children="Symptomen en gezondheidsklachten",
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                html.P(
                    children="""
                    Onze deelnemers melden iedere week of ze één of meerdere klachten hadden. De afgelopen week ontvingen we 733 ingevulde vragenlijsten. In 84.0% van de ingevulde vragenlijsten werden geen symptomen gerapporteerd. In deze grafiek zie je het percentage deelnemers dat een bepaalde klacht rapporteert. Een combinatie van symptomen kan wijzen op een specifieke infectieziekte zoals griep, COVID-19, RSV of een andere.
                    """,
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                dcc.Graph(id="symptoms", figure=symptom_fig)
            ],
            style={"paddingTop": "1rem"}
        ),
        html.Div(
            children=[
                html.H2(
                    children="Trendlijn griepachtige klachten",
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                html.P(
                    children="""
                    Deze grafiek toont het aantal deelnemers per 1000 met griepachtige klachten door de tijd.
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
                    children="Trendlijn COVID-19 achtige klachten",
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                html.P(
                    children="""
                    Deze grafiek toont het aantal deelnemers per 1000 met COVID-19 achtige klachten door de tijd.
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
                    children="Onze deelnemers",
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                html.P(
                    children="""
                    Deze grafieken tonen de leeftijd, geslacht en woonplaats van onze deelnemers. We hebben 2227 deelnemers, met 40.2% mannen en 59.4% vrouwen. De kaart toont het aantal deelnemers op 1000 inwoners per provincie. Een donkerdere kleur wijst op een grotere deelname van inwoners uit die provincie. Ben je nog geen deelnemer? Meld je aan en help mee om infectieziekten in de gaten te houden.
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
