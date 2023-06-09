import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import ReseauBayesien as ReB

###### Data & Style ######
name = "CestQuoiCeBruit ?"
isAdvenced = False
explain = "CestQuoiCeBruit ? est un outil d'aide au diagnostic de pannes automobiles. Il permet de déterminer la panne d'un véhicule en fonction de ses symptômes."
center = {'textAlign': 'center', 'margin-top': '25%', 'color': '#fff','font-weight': 'bold'}
title = { 'margin-top': '1%','margin-left': '1%', 'color': '#fff','font-weight': 'bold'}
form = {'background-color': '#fff', 'border-radius': '15px', 'padding': '1%', 'margin-top': '1%','margin-left': '1%', 'margin-right': '1%'}
cardStyle =  {'margin-top': '2%','margin-left': '2%', 'margin-right': '2%'}

x_data = []
y_data = []


systemN1= []
systemN2= []
systemN3= []
typeDeTravail= []
###########################

##### Réseau bayésien #####
def sortSet(set):
    return sorted(set, key=str.lower)

rb = ReB.ReseauBayesien()
AllSig_Obs=sortSet(rb.getAllSig_Obs())
AllSig_Organe= sortSet(rb.getAllSig_Organe())
AllConstructeur= sortSet(rb.getAllConstructeur())
AllModele=sortSet(rb.getAllModele())
AllSigContexte=sortSet(rb.getAllSigContexte())
AllKilometrage=sortSet(rb.getAllKilometrage())
###########################


##### Composants Dash #####

# Créer une figure avec ces données
def figureTab(x_data, y_data) :
    fig = go.Figure(data=go.Bar(x=x_data, y=y_data))
    fig.update_layout(
        autosize=False,
        width=500,
        height=250,
        margin=dict( l=20, r=20, b=10, t=10, pad=4),
    )
    # Créer le graphique Dash avec cette figure
    graph = dcc.Graph(
        id='graph',
        figure=fig,
    )
    return graph

def cardFig(cardData):
    cards = []
    for item in cardData:
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
    return cards

radio = dcc.RadioItems(
            id='switch',
            options=[
                {'label': 'Mode Simplifié', 'value': False},
                {'label': 'Mode Avancé', 'value': True}
            ],
            value=False,
            labelStyle={'display': 'inline-block', 'margin-right': '20px'}
        )

###########################


##### Application Dash #####
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
                            dbc.Container([
                            dbc.Row([
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="N1",
                                        options=[
                                            {"label": col, "value": col} for col in systemN1
                                        ],
                                    ),
                                    style={'margin-right':'-50px','width':'210px'}
                                    , width=2),
                                dbc.Col(
                                    html.P(">",style={'text-align':'center'})
                                    , width=2),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="N2",
                                        options=[
                                            {"label": col, "value": col} for col in systemN2
                                        ],
                                    ),
                                    style={'margin-right':'-50px','margin-left':'-50px','width':'220px'}
                                    , width=2),
                                dbc.Col(
                                    html.P(">",style={'text-align':'center'})
                                    , width=2),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="N3",
                                        options=[
                                            {"label": col, "value": col} for col in systemN3
                                        ],
                                    ),
                                    style={'margin-left':'-50px','width':'220px'}
                                    , width=2),
                            ])
                        ], fluid=True),
                            html.Div(id='card-container')
                            ]
                            ), width=6,
                    style={'margin-bottom':'-120px'},),
             html.Div(id='switch-container'),
            ],
            justify="between",
            className="mt-4",
            style={'width':'120%'}
        )
    ]
)])
###########################
##### Callbacks ###########
@app.callback(
    [Output('MonVehicule-output', 'children'),
     Output('symptome-output', 'children'),
     Output('switch-container', 'children'),
     Output('N1', 'options'),
     Output('N1', 'value'),
     Output('N2', 'options'),
     Output('N2', 'value'),
     Output('N3', 'options'),
     Output('N3', 'value'),
     Output('card-container', 'children'),],
    [
     Input('MonVehicule', 'value'),
     Input('symptome', 'value'),
     Input('km', 'value'),
     Input('Organe', 'value'),
     Input('monModele', 'value'),
     Input('Observation', 'value'),
     Input('switch', 'value'),
     Input('N1', 'value'),
     Input('N2', 'value'),
     Input('N3', 'value'),

     ]
)
def update_output_div(monVehicule, symptome, km, organe, monModele, observation, switch, systemN1Resp, systemN2Resp, systemN3Resp):
    global x_data
    global y_data
    output1 = None
    output2 = None
    output3 = None
    output4 = []
    output4bis = None
    output5 = []
    output5bis = None
    output6 = []
    output6bis = None
    output7 = None
    dict = {}
    result = [
            {"title": "Pas de résultat", "text": "Aucun résultat trouvé"},
        ]  
    
    if monModele is not None and symptome is not None and km is not None and organe is not None and observation is not None:
        dict = {"MODELE": monModele, "SIG_OBS": symptome, "KILOMETRAGE_CLASSE": km, "SIG_ORGANE": organe, "SIG_CONTEXTE": observation}
        x_data,y_data = rb.predictionWebN1(dict)
        print("N1")
        print(x_data)
        print(y_data)
        x_data.reverse()
        output4 = [{'label': col, 'value': col} for col in x_data]
        x_data.reverse()
        output4bis = systemN1Resp
        
    if systemN1Resp is not None:
        dict["SYSTEM_N1"] = systemN1Resp
        x_data,y_data = rb.predictionWebN2(dict)
        print("N2")
        print(x_data)
        print(y_data)
        x_data.reverse()
        output5 = [{'label': col, 'value': col} for col in x_data]
        x_data.reverse()
        output5bis = systemN2Resp
    
    if systemN2Resp is not None:
        dict["SYSTEM_N2"] = systemN2Resp
        x_data,y_data = rb.predictionWebN3(dict)
        print("N3")
        print(x_data)
        print(y_data)
        x_data.reverse()
        output6 = [{'label': col, 'value': col} for col in x_data]
        x_data.reverse()
        output6bis = systemN3Resp
    
    if systemN3Resp is not None:
        
        dict["SYSTEM_N3"] = systemN3Resp
        x_data,y_data = rb.predictionWebWork(dict)
        print("Work")
        print(x_data)
        print(y_data)
        x_data.reverse()
        result = []
        for i in x_data:
            result.append({"title": i, "text": "Merci de vous référer à la fiche technique du véhicule"})
        x_data.reverse()


    output7 = cardFig(result) 
    if switch == True:
        print("Mode avancé activé")
        output3 = figureTab(x_data,y_data)

    return output1, output2,output3,output4,output4bis,output5,output5bis,output6,output6bis,output7

###########################
##### Run Application #####
if __name__ == '__main__':
    app.run_server(debug=True)
###########################