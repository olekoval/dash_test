from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

poverty_data = pd.read_csv('data/PovStatsData.csv')
regions = ['East Asia & Pacific', 'Europe & Central Asia', 'Fragile and conflict affected situations', 
           'High income', 'IDA countries classified as fragile situations', 'IDA total', 
           'Latin America & Caribbean', 'Low & middle income', 'Low income', 'Lower middle income',
           'Middle East & North Africa', 'Middle income', 'South Asia', 'Sub-Saharan Africa', 
           'Upper middle income', 'World']

population_df = poverty_data[~poverty_data['Country Name'].isin(regions) &
(poverty_data['Indicator Name']=='Population, total')]

app.layout = html.Div(className="wrapper", children=[
    
    html.Div(className="header", children=[
    html.H1('Poverty And Equity Database',
            className="text-info bg-light rounded-3 p-4",
            style={'fontSize': '40px'}),
    html.H2('The World Bank', className="text-info")]
    ),
    
    html.Div(className="dropdown-area", children=[
    dcc.Dropdown(id='country',
               options=[
                 {'label': country, 'value': country} for country in poverty_data['Country Name'].unique()]),
    html.Br(),             
    dcc.Dropdown(id='year_dropdown',
                 options=[
                     {'label': year, 'value': str(year)} 
                     for year in range(1974, 2019)
                 ],
                 value='2010' # значення за замоченням
        ),
    html.Br(),
    html.Div(id='report', className="border rounded-3 border-2 border-info text-info p-3"),
    html.Br()
    ]),

    html.Div(className="figure", children=[
        dcc.Graph(id='population_chart')
    ]),

    html.Div(className="tabs", children=[
    dbc.Tabs([
        dbc.Tab(label='Key Facts',
                children=[
            html.Ul([
                html.Li('Number of Economies: 170'),
                html.Li('Temporal Coverage: 1974 - 2019'),
                html.Li('Update Frequency: Quarterly'),
                html.Li('Last Updated: March 18, 2020'),
                html.Li([
                    'Source: ',
                    html.A('https://datacatalog.worldbank.org/dataset/poverty-and-equity-database',
                           href='https://datacatalog.worldbank.org/dataset/poverty-and-equity-database')
                ]), 
            ]), 
        ]), 
        
        dbc.Tab(label='Project Info', children=[
            html.Ul([
                html.Br(),
                html.Li('Book title: Interactive Dashboards and Data Apps with Plotly and Dash'),
                html.Li([
                    'GitHub repo: ',
                    html.A('https://github.com/PacktPublishing/Interactive-Dashboards-and-Data-Apps-with-Plotly-and-Dash',
                           href='https://github.com/PacktPublishing/Interactive-Dashboards-and-Data-Apps-with-Plotly-and-Dash')
                ])
            ]) 
        ])         
      ]) 
    ])      
])

@callback(
    Output(component_id='report', component_property='children'),    
    Input(component_id='country', component_property='value')
)

def display_country_report(country):
    if country is None:
        return ''
    filtered_df = poverty_data[(poverty_data['Country Name']==country) &
                               (poverty_data['Indicator Name']=='Population, total')]
    population = filtered_df.loc[:, '2010'].values[0]
    
    return [html.H3(country), f'The population of {country} in 2010 was {population:,.0f}.']


@callback(
        Output(component_id='population_chart', component_property='figure'),
        Input(component_id='year_dropdown', component_property='value')
)
def plot_countries_by_population(year):
    year_df = (population_df[['Country Name', year]]
               .sort_values(year, ascending=False)
            )
    year_df = year_df.iloc[:20, :]
    
    fig = go.Figure()
    fig.add_bar(
        x=year_df['Country Name'], 
        y=year_df[year]
    )
    fig.layout.title = f'Top twenty countries by population - {year}'
    return fig
    
if __name__ == '__main__':
    app.run(debug=True)
