from dash import dcc, html, register_page
import plotly.express as px
import pandas as pd
import json

register_page(__name__, path='/fr-be')

colors = {"background": "#FFFFFF", "text": "#101010", "warning-text": "#FF4136"}

# Bar - symptoms
df_symptoms = pd.read_csv("data/fr/symptoms.csv")

symptom_fig = px.bar(
    df_symptoms,
    x="frequentie",
    y="symptom",
    orientation="h",
    labels={"frequentie": "Fréquence (%)", "symptom": "Symptômes"},
    color="frequentie",
    color_continuous_scale="pinkyl",
    template="plotly_white",
    height=600
)

symptom_fig.update_layout(yaxis={"categoryorder": "total ascending"})



# Trendline - flu-like symptoms
df_flulike = pd.read_csv("data/fr/flulike.csv")


trendline_flu_fig = px.line(
    df_flulike,
    x="week",
    y="incidentie",
    color="year",
    labels={"incidentie": "Incidence pour 1000 participants", "week": "Semaine", "year": "Année"},
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
df_covidlike = pd.read_csv("data/fr/covidlike.csv")

trendline_covid_fig = px.line(
    df_covidlike,
    x="week",
    y="incidentie",
    color="year",
    labels={"incidentie": "Incidence pour 1000 participants", "week": "Semaine", "year": "Année"},
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

df_provinces = pd.read_csv("data/fr/provinces.csv")

map_fig = px.choropleth(
    df_provinces,
    geojson=provinces,
    locations="province",
    featureidkey="properties.name-french",
    labels={"deelnemersper1000": "Participants pour 1000 résidents", "province": "Province"},
    basemap_visible=False,
    color="deelnemersper1000",
    color_continuous_scale="pinkyl",
    fitbounds="locations",
    projection="mercator",
    height=600,
)

map_fig.update_layout(margin={"r": 10, "t": 0, "l": 10, "b": 0}, dragmode=False)



# Bar - sex and age group
df_sexage = pd.read_csv("data/fr/sexage.csv")

# y-axis = age groups, x-axis = count, double sided with gender, bar chart
sexage_fig = px.bar(
    df_sexage,
    x="count",
    y="age",
    orientation="h",
    color="sex",
    labels={"count": "Nombre de participants", "age": "Groupe d'âge", "sex": "Sexe"},
    template="plotly_white",
)

layout = html.Div(
    children=[
        html.Div(children=[
            html.P(
                children="Dernière modification de cette page le 26.Jui.2024 10:00.",
                style={"textAlign": "left", "color": colors["warning-text"]},
            ),
            html.P(
                children="""
                    Les données que nous obtenons chaque semaine grâce à nos participants nous permettent de recenser la propagation de la grippe, du coronavirus, ainsi que d'autres infections et problèmes de santé. Nous remercions les participants pour leurs contributions hebdomadaires. Ensemble, nous pouvons ainsi suivre l’évolution de la situation en Belgique, et ce, rapidement et à un stade précoce.
                """,
                style={"textAlign": "left", "color": colors["text"]},
            )]
        ),
        html.Div(
            children=[
                html.H2(
                    children="Symptômes et problèmes de santé",
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                html.P(
                    children="""
                        Chaque semaine, nos participants indiquent s'ils ont ressenti un ou plusieurs symptôme(s). La semaine dernière, nous avons reçu 733 questionnaires complétés. Dans 84.0% des questionnaires complétés, aucun symptôme n'a été signalé. Ce graphique indique le pourcentage de participants ayant signalé un symptôme particulier. Une combinaison de symptômes peut indiquer une maladie infectieuse spécifique telle que la grippe, le coronavirus, le VRS, etc.
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
                    children="Ligne de tendance des plaintes de type grippal",
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                html.P(
                    children="""
                        Ce graphique montre le nombre de participants pour 1.000 personnes présentant des symptômes de type grippal sur une période prolongée.
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
                    children="Ligne de tendance des symptômes de type coronavirus",
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                html.P(
                    children="""
                        Ce graphique montre le nombre de participants pour 1.000 personnes présentant des symptômes de type coronavirus sur une période prolongée.
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
                    children="Nos participants",
                    style={"textAlign": "left", "color": colors["text"]},
                ),
                html.P(
                    children="""
                        Ces graphiques indiquent l'âge, le sexe et le lieu de résidence de nos participants. Nous avons 2227 participants, dont 40.2% d'hommes et 59.4% de femmes. Le graphique illustre le nombre de participants pour 1.000 habitants par province. Une couleur plus foncée indique une plus grande participation des habitants de cette province. Vous ne figurez pas encore parmi les participants ? Dans ce cas, inscrivez-vous, et contribuez à la surveillance des maladies infectieuses.
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