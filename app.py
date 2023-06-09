import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import ReseauBayesien as rb
name = "CestQuoiCeBruit ?"
isAdvenced = False
explain = "CestQuoiCeBruit ? est un outil d'aide au diagnostic de pannes automobiles. Il permet de déterminer la panne d'un véhicule en fonction de ses symptômes."
center = {'textAlign': 'center', 'margin-top': '25%', 'color': '#fff','font-weight': 'bold'}
title = { 'margin-top': '1%','margin-left': '1%', 'color': '#fff','font-weight': 'bold'}
form = {'background-color': '#fff', 'border-radius': '15px', 'padding': '1%', 'margin-top': '1%','margin-left': '1%', 'margin-right': '1%'}
cardStyle =  {'margin-top': '2%','margin-left': '2%', 'margin-right': '2%'}
car = ["Audi", "BMW", "Ford", "Honda", "Jaguar", "Mercedes", "Nissan", "Toyota", "Volkswagen", "Volvo"]

##### Réseau bayésien #####
def sortSet(set):
    return sorted(set, key=str.lower)

rb = rb.ReseauBayesien()
AllSig_Obs=sortSet(rb.getAllSig_Obs())
AllSig_Organe= sortSet(rb.getAllSig_Organe())
AllConstructeur= sortSet(rb.getAllConstructeur())
AllModele=sortSet(rb.getAllModele())
AllSigContexte=sortSet(rb.getAllSigContexte())
AllKilometrage=sortSet(rb.getAllKilometrage())



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
                                    dbc.Label("La marque de mon véhicule"),
                                    dcc.Dropdown(
                                        id="MonVehicule",
                                        options=[
                                            {"label": col, "value": col} for col in AllConstructeur
                                        ],
                                    ),
                                ]
                            ),
                            html.Div(
                                [
                                    dbc.Label("Modèle"),
                                    dcc.Dropdown(
                                        id="monModele",
                                        options=[
                                            {"label": col, "value": col} for col in AllModele
                                        ],
                                    ),
                                    html.Div(id='modele-output')
                                ]
                            ),
                            html.Div(id='MonVehicule-output'),
                            html.Div(
                                [
                                    dbc.Label("Symptôme"),
                                    dcc.Dropdown(
                                        id="symptome",
                                        options=[
                                            {"label": col, "value": col} for col in AllSig_Obs
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
                                            {"label": col, "value": col} for col in AllKilometrage
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
                                            {"label": col, "value": col} for col in AllSig_Organe
                                        ],
                                    ),
                                    html.Div(id='Organe-output')
                                ]
                            ),
                            html.Div(
                                [
                                    dbc.Label("Observation"),
                                    dcc.Dropdown(
                                        id="Observation",
                                        options=[
                                            {"label": col, "value": col} for col in AllSigContexte
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
     Input('monModele', 'value'),
     Input('Observation', 'value'),
     Input('switch', 'value')
     ]
)
def update_output_div(monVehicule, symptome, km, organe, monModele, observation, switch):

    output1 = None
    output2 = None
    output3 = None
    if monVehicule is not None:
        AllModele = rb.getAllModeleWithConstruct(monVehicule)
        output1 = dropDownImpl(AllModele)
    print(monVehicule)
    print(symptome)
    print(switch)
    if switch == True:
        print("Mode avancé activé")
        output3 = graph

    return output1, output2,output3



if __name__ == '__main__':
    app.run_server(debug=True)
