from dash import dcc, html, register_page
import plotly.express as px
import pandas as pd
import json

register_page(__name__, path='/de-be')

colors = {"background": "#FFFFFF", "text": "#101010", "warning-text": "#FF4136"}

# Bar - symptoms
df_symptoms = pd.read_csv("data/de/symptoms.csv")

symptom_fig = px.bar(
    df_symptoms,
    x="frequentie",
    y="symptom",
    orientation="h",
    labels={"frequentie": "Frequenz (%)", "symptom": "Symptome"},
    color="frequentie",
    color_continuous_scale="pinkyl",
    template="plotly_white",
    height=600
)

symptom_fig.update_layout(yaxis={"categoryorder": "total ascending"})



# Trendline - flu-like symptoms
df_flulike = pd.read_csv("data/de/flulike.csv")

trendline_flu_fig = px.line(
    df_flulike,
    x="week",
    y="incidentie",
    color="year",
    labels={"incidentie": "Inzidenz pro 1000 Teilnehmer", "week": "Woche", "year": "Jahr"},
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
df_covidlike = pd.read_csv("data/de/covidlike.csv")

trendline_covid_fig = px.line(
    df_covidlike,
    x="week",
    y="incidentie",
    color="year",
    labels={"incidentie": "Inzidenz pro 1000 Teilnehmer", "week": "Woche", "year": "Jahr"},
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

df_provinces = pd.read_csv("data/de/provinces.csv")

map_fig = px.choropleth(
    df_provinces,
    geojson=provinces,
    locations="province",
    featureidkey="properties.name-german",
    labels={"deelnemersper1000": "Teilnehmer pro 1000 Einwohner", "province": "Provinz"},
    basemap_visible=False,
    color="deelnemersper1000",
    color_continuous_scale="pinkyl",
    fitbounds="locations",
    projection="mercator",
    height=600,
)

map_fig.update_layout(margin={"r": 10, "t": 0, "l": 10, "b": 0}, dragmode=False)



# Bar - sex and age group
df_sexage = pd.read_csv("data/de/sexage.csv")

# y-axis = age groups, x-axis = count, double sided with gender, bar chart
sexage_fig = px.bar(
    df_sexage,
    x="count",
    y="age",
    orientation="h",
    color="sex",
    labels={"count": "Anzahl der Teilnehmer", "age": "Altersgruppe", "sex": "Sex"},
    template="plotly_white",
)

layout = html.Div(
    children=[
        html.Div(children=[
            html.P(
                children="Diese Seite wurde zum letzten Mal angepasst am 26.Jun.2024 10:00.",
                style={"textAlign": "left", "color": colors["warning-text"]},
            ),
            html.P(
                children="""
                    Mit den Daten, die wir jede Woche von unseren Teilnehmern erhalten, können wir die Verbreitung von Grippe, COVID-19, anderen Infektionen und Gesundheitsbeschwerden kartieren. Wir danken den Teilnehmern für ihre wöchentlichen Beiträge. Gemeinsam können wir die Situation in Belgien schnell und frühzeitig erfassen.
                """,
                style={"textAlign": "left", "color": colors["text"]},
            )]
        ),
        html.Div(
            children=[
                html.H2(
                    children="Symptome und gesundheitliche Beschwerden",
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                html.P(
                    children="""
                        Unsere Teilnehmer berichten jede Woche, ob sie eines oder mehrere Symptome hatten. In der vergangenen Woche erhielten wir 733 ausgefüllte Fragebögen. In 84.0 % der ausgefüllten Fragebögen wurden keine Symptome angegeben. Diese Grafik zeigt den Prozentsatz der Teilnehmer, die ein bestimmtes Symptom melden. Eine Kombination aus Symptomen kann auf eine bestimmte Infektionskrankheit wie Grippe, Corona, RSV oder andere Erkrankungen hinweisen.
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
                    children="Trendlinie grippeähnliche Symptome",
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                html.P(
                    children="""
                        Diese Grafik zeigt die Anzahl der Teilnehmer pro 1000 mit grippeähnlichen Symptomen im Laufe der Zeit.
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
                    children="Trendlinie COVID-19-ähnliche Beschwerden",
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                html.P(
                    children="""
                        Diese Grafik zeigt die Anzahl der Teilnehmer pro 1000 mit COVID-19-ähnlichen Beschwerden im Laufe der Zeit.
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
                    children="Unsere Teilnehmer",
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                html.P(
                    children="""
                        Diese Diagramme zeigen das Alter, das Geschlecht und den Wohnort unserer Teilnehmer. Es gibt 2227 Teilnehmer, davon 40.2 % Männer und 59.4 % Frauen. Die Karte zeigt die Anzahl der Teilnehmer pro 1000 Einwohner pro belgischer Provinz. Eine dunklere Farbe bedeutet eine höhere Beteiligung von Einwohnern der jeweiligen Provinz. Sie sind noch kein Teilnehmer? Melden Sie sich an und helfen Sie mit, Infektionskrankheiten im Auge zu behalten.
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