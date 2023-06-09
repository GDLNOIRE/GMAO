import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
name = "CestQuoiCeBruit ?"
isAdvenced = False
explain = "CestQuoiCeBruit ? est un outil d'aide au diagnostic de pannes automobiles. Il permet de déterminer la panne d'un véhicule en fonction de ses symptômes."
center = {'textAlign': 'center', 'margin-top': '25%', 'color': '#fff','font-weight': 'bold'}
title = { 'margin-top': '1%','margin-left': '1%', 'color': '#fff','font-weight': 'bold'}
form = {'background-color': '#fff', 'border-radius': '15px', 'padding': '1%', 'margin-top': '1%','margin-left': '1%', 'margin-right': '1%'}
cardStyle =  {'margin-top': '2%','margin-left': '2%', 'margin-right': '2%'}
car = ["Audi", "BMW", "Ford", "Honda", "Jaguar", "Mercedes", "Nissan", "Toyota", "Volkswagen", "Volvo"]

result = [
    {"title": "Carte 1", "text": "Contenu de la carte 1"},
    {"title": "Carte 2", "text": "Contenu de la carte 2"},
    {"title": "Carte 3", "text": "Contenu de la carte 3"},
    {"title": "Carte 2", "text": "Contenu de la carte 2"},
    {"title": "Carte 2", "text": "Contenu de la carte 2"},
]
dropDowns = [
    {"title":"Mon véhicule","options":car,"id":"car",'idOutput':"carOutput"},
    {"title":"Symptôme","options":car,"id":"symptome",'idOutput':"symptomeOutput"},
    {"title":"Kilométrage","options":car,"id":"km",'idOutput':"kmOutput"},
    {"title":"Organe","options":car,"id":"organe",'idOutput':"organeOutput"},
    {"title":"Ligne de bus","options":car,"id":"line",'idOutput':"lineOutput"},
    {"title":"Observation","options":car,"id":"observation",'idOutput':"observationOutput"},
    
]

x_data = ['A', 'B', 'C', 'D', 'E']
y_data = [10, 15, 7, 10, 12]

# Créer une figure avec ces données
fig = go.Figure(data=go.Bar(x=x_data, y=y_data))
fig.update_layout(
    autosize=False,
    width=500,
    height=250,
    margin=dict( l=20, r=20, b=10, t=10, pad=4),
)

# Créer le graphique Dash avec cette figure
graph = dcc.Graph(
    id='example-graph',
    figure=fig,
)

cards = []
for item in result:
    card = dbc.Card(
        [
            dbc.CardHeader(item["title"]),
            dbc.CardBody(
                [
                    html.P(item["text"], className="card-text"),
                ]
            )
        ],
        className="mb-4",
        style=cardStyle
    )
    cards.append(card)

ddown = []
for item in dropDowns:
    ddown.append(
        html.Div(
            [
                dbc.Label(item["title"]),
                dcc.Dropdown(
                    id=item["id"],
                    options=[
                        {"label": col, "value": col} for col in item["options"]
                    ],
                ),
                html.Div(id=item["idOutput"])
            ]
        )
    )

radio = dcc.RadioItems(
            id='switch',
            options=[
                {'label': 'Mode Simplifié', 'value': False},
                {'label': 'Mode Avancé', 'value': True}
            ],
            value=False,
            labelStyle={'display': 'inline-block', 'margin-right': '20px'}
        )

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    style={
        'position': 'absolute',
        'top': '0',
        'background-image': 'url("/assets/bg.jpg")',
        'background-size': 'cover',
        'background-position': 'center',
        'width': '100%',
        'height': '100vh'
    },
        children=[
        html.H1(name, style=title),

dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            html.H3("Signaler un problème", className="card-title",style={'text-align': 'center'}),
                            html.Div(
                                [
                                    dbc.Label("Mon véhicule"),
                                    dcc.Dropdown(
                                        id="MonVehicule",
                                        options=[
                                            {"label": col, "value": col} for col in car
                                        ],
                                    ),
                                     html.Div(id='MonVehicule-output')
                                ]
                            ),
                            html.Div(
                                [
                                    dbc.Label("Symptôme"),
                                    dcc.Dropdown(
                                        id="symptome",
                                        options=[
                                            {"label": col, "value": col} for col in car
                                        ],
                                    ),
                                    html.Div(id='symptome-output')
                                ]
                            ),
                            html.Div(
                                [
                                    dbc.Label("Kilométrage"),
                                    dcc.Dropdown(
                                        id="km",
                                        options=[
                                            {"label": col, "value": col} for col in car
                                        ],
                                    ),
                                    html.Div(id='km-output')
                                ]
                            ),
                            html.Div(
                                [
                                    dbc.Label("Organe"),
                                    dcc.Dropdown(
                                        id="Organe",
                                        options=[
                                            {"label": col, "value": col} for col in car
                                        ],
                                    ),
                                    html.Div(id='Organe-output')
                                ]
                            ),
                            html.Div(
                                [
                                    dbc.Label("Ligne de bus"),
                                    dcc.Dropdown(
                                        id="ligne",
                                        options=[
                                            {"label": col, "value": col} for col in car
                                        ],
                                    ),
                                    html.Div(id='ligne-output')
                                ]
                            ),
                            html.Div(
                                [
                                    dbc.Label("Observation"),
                                    dcc.Dropdown(
                                        id="Observation",
                                        options=[
                                            {"label": col, "value": col} for col in car
                                        ],
                                    ),
                                    html.Div(id='Observation-output')
                                ]
                            ),
                            html.Div([
                                radio,
                                html.P(id='output-container'),
                            ]),
                               
                        ],
                        body=True,
                        style={'max-width': '400px'},
                    ),
                    width=6
                ),
                ## COLONNE 2
                dbc.Col(dbc.Card(
                        [
                            html.H3("Nos Suggestions", className="card-title",style={'text-align': 'center'}),
                            html.Div(cards)
                            ]
                            ), width=6,
                    style={'margin-bottom':'-120px'},),
             html.Div(id='switch-container'),
            ],
            justify="between",
            className="mt-4"
        )
    ]
)])

@app.callback(
    [Output('MonVehicule-output', 'children'),
     Output('symptome-output', 'children'),
     Output('switch-container', 'children'),],
    [
     Input('MonVehicule', 'value'),
     Input('symptome', 'value'),
     Input('km', 'value'),
     Input('Organe', 'value'),
     Input('ligne', 'value'),
     Input('Observation', 'value'),
     Input('switch', 'value')
     ]
)
def update_output_div(monVehicule, symptome, km, organe, ligne, observation, switch):
    print(monVehicule)
    print(symptome)
    print(switch)
    if switch == True:
        print("Mode avancé activé")
        return None, None, graph
    else:
        return None, None, None


if __name__ == '__main__':
    app.run_server(debug=True)
