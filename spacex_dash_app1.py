# Importar bibliotecas necessárias
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Ler os dados do arquivo CSV
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Obter valores mínimos e máximos de Payload Mass
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Criar a aplicação Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Dropdown para seleção do site de lançamento
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
        ],
        value='ALL',
        placeholder="Select a Launch Site",
        searchable=True
    ),
    
    html.Br(),
    
    # Gráfico de pizza para sucesso/falha dos lançamentos
    html.Div(dcc.Graph(id='success-pie-chart')),
    
    html.Br(),
    
    html.P("Payload range (Kg):"),
    
    # Slider para selecionar intervalo de payload
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: str(i) for i in range(0, 10001, 1000)},
        value=[min_payload, max_payload]
    ),
    
    # Gráfico de dispersão para correlação entre payload e sucesso
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# Callback para atualizar o gráfico de pizza com base na seleção do site
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        df = spacex_df
    else:
        df = spacex_df[spacex_df['Launch Site'] == selected_site]
    
    fig = px.pie(df, names='class', title='Success vs. Failure Counts')
    return fig

# Callback para atualizar o gráfico de dispersão com base na seleção do site e intervalo de payload
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    min_payload, max_payload = payload_range
    df = spacex_df[spacex_df['Payload Mass (kg)'].between(min_payload, max_payload)]
    
    if selected_site != 'ALL':
        df = df[df['Launch Site'] == selected_site]
    
    fig = px.scatter(
        df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload Mass vs. Success'
    )
    return fig

# Rodar o servidor
if __name__ == '__main__':
    app.run_server()
