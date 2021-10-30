
import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

df = pd.read_csv('Data.csv')
df.drop(['Flight #', 'Route', 'Registration', 'cn/In', 'Ground', 'Summary', 'Time'], axis=1, inplace=True)
df.dropna(inplace=True)
df.reset_index(inplace=True)
df.drop('index', axis=1, inplace=True)
df['Survived'] = df['Aboard'] - df['Fatalities']
df['Date'] = pd.to_datetime(df['Date'])
df['dayOfWeek'] = df['Date'].dt.day_name()
df['Year'] = df['Date'].dt.year
print(df.head())
print(df.columns)
# gg = df['Operator'].groupby(df['Year']).count().tolist()
cc = df['Survived'].groupby(df['Year']).sum().tolist()
dd = df["Date"].groupby(df['Year']).count().tolist()

f =[]
for i in range(len(cc)):
    f.append(cc[i]/dd[i])


years = df['Year'].unique()

#print(df.columns, f, dd, cc)
#print(df.Year.unique())

# fig = px.bar(df, x=years, y=gg, template='plotly_dark', title="Test")
fig2 = px.bar(df, x=years, y=cc, template='plotly_dark', title="Survived per year")
fig3 = px.bar(df, x=years, y=dd, template='plotly_dark', title="Accidents per year")
fig4 = px.bar(df, x=years, y=f, template='plotly_dark', title="Survived on accidents per year")
#fig2 = px.pie(df,values='Survived', names='Type', title="Survived per year")

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1('Plane Accidents',
            style={'color': 'red', 'textAlign': 'center', 'backgroundColor': 'cyan'}),

    dcc.Dropdown(id='select_year',
                 options=[
                     {'label': '1908', 'value': 1908},
                     {'label': '1915', 'value': 1915},
                     {'label': '1930', 'value': 1930},
                     {'label': '1940', 'value': 1940},
                     {'label': '1950', 'value': 1950},
                     {'label': '1960', 'value': 1960},
                     {'label': '1990', 'value': 1990},
                     {'label': '2000', 'value': 2000},
                     {'label': '2009', 'value': 2009}],
                 multi=False,
                 value=1908,
                 style={'width': '40%'}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    html.Div([
        
        dcc.Graph(id='my_graph', figure={}, style={'padding':'10px'}),
    # html.Br(),
    # html.Div([
    #             dcc.Graph(figure=fig)
    #
    #         ]),
    dcc.Graph(figure=fig2, style={'padding':'10px'})
        ], style={"display": "grid", "grid-template-columns": "50%  50%"}),
    html.Br(),
    

    html.Br(),
    html.Div([
        dcc.Graph(figure=fig3, style={'padding':'10px'}),
        dcc.Graph(figure=fig4, style={'padding':'10px'})
        ], style={"display": "grid", "grid-template-columns": "50%  50%"}),
    
    #html.Br(),



])


# Connect the plotly grahps wuth Dash components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_graph', component_property='figure')],
    [Input(component_id='select_year', component_property='value')]
)
def update_graph(option_selected):  # 1 param --> 1 i/p
    print(option_selected)
    print(type(option_selected))

    container = 'Data for year: {}'.format(option_selected)

    dff = df.copy()
    dff = dff[dff['Year'] == option_selected]

    fig = px.scatter(dff, x='Operator', y='Survived', template='plotly_dark', color='Location')
    # px.scatter(df, x='gdpPercap', y='lifeExp', template='plotly_dark', animation_frame='year', color='continent',
    #            title="Test", symbol="continent",
    #            log_x=True, width=800, height=800,
    #            size='pop', size_max=60, hover_name='country')

    return container, fig  # 2 outputs


app.run_server()