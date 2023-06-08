import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
name = "CestQuoiCeBruit ?"
center = {'textAlign': 'center', 'margin-top': '25%', 'color': '#fff','font-weight': 'bold'}
title = { 'margin-top': '1%','margin-left': '1%', 'color': '#fff','font-weight': 'bold'}
form = {'background-color': '#fff', 'border-radius': '15px', 'padding': '1%', 'margin-top': '1%','margin-left': '1%', 'margin-right': '5%'}
car = ["Audi", "BMW", "Ford", "Honda", "Jaguar", "Mercedes", "Nissan", "Toyota", "Volkswagen", "Volvo"]
result = [
    {"title": "Carte 1", "text": "Contenu de la carte 1"},
    {"title": "Carte 2", "text": "Contenu de la carte 2"},
    {"title": "Carte 3", "text": "Contenu de la carte 3"}
]
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
        className="mb-4"
    )
    cards.append(card)

app.layout = html.Div(
    children=[
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ]
)

# Première page
page_1_layout = html.Div(
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
        html.H1(name, style=center),
        dbc.Button(
            "Signaler un problème",
            href='/page-2',
            color="primary",
            style={'margin-left': '43%', 'margin-top': '2%'}
        )
    ]
)

# Deuxième page
page_2_layout = html.Div(
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
                            html.Div(
                                [
                                    dbc.Label("Mon véhicule"),
                                    dcc.Dropdown(
                                        id="MonVehicule",
                                        options=[
                                            {"label": col, "value": col} for col in car
                                        ],
                                        value="sepal length (cm)",
                                    ),
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
                                        value="sepal width (cm)",
                                    ),
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
                                        value="sepal width (cm)",
                                    ),
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
                                        value="sepal width (cm)",
                                    ),
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
                                        value="sepal width (cm)",
                                    ),
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
                                        value="sepal width (cm)",
                                    ),
                                ]
                            ),
                            dbc.Button("Envoyer", id="aaa", color="primary", className="mt-3"),
                        ],
                        body=True,
                        style={'max-width': '400px', 'margin': '0 auto'},
                    ),
                    width=6
                ),
                ## COLONNE 2
                dbc.Col(dbc.Card(
                        [html.Div(cards)]), width=6),
            ],
            justify="between",
            className="mt-4"
        )
    ]
)])
# Troisième page
page_3_layout = html.Div(
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
        html.H1(name, style=center),
        dbc.Button("Retour à la page d'accueil", href='/', color="primary")
    ]
)
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')], 
)
def display_page(pathname):
    if pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    else:
        return page_1_layout

def submit_form(n_clicks, MonVehicule, symptome, km):
    if n_clicks:
        # Construction de l'URL pour la page /page-3 avec les valeurs du formulaire en tant que paramètres de requête
        url = f"/page-3?x={MonVehicule}&y={symptome}&cluster={km}"
        return url
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)
