# sourced from https://dash.plot.ly/getting-started
# modified to include a map 
# map example from https://plot.ly/python/choropleth-maps/#united-states-choropleth-map 

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'choropleth', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'choropleth', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization',
                'geo': {
                    'scope' : 'usa',
                    'projection' : {'type' : 'washington usa'},
                    'showlakes' : True,
                    'lakecolor' : 'rgb(255, 255, 255)'},
                    'lonaxis' : {'range' : '[-122, -121]'},
                    'lataxis' : {'range' : '[47, 48]'}
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)