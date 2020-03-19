#!/home/folmer/anaconda3/bin/python
import sys,os
sys.stdout = open('/var/www/output/dash_output.txt', 'w')
print('hello')
print(sys.path)
#sys.path.inster(0,'/home/folmer/anaconda3/bin/python/site-packages')
import dash

import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.requests_pathname_prefix = app.config.routes_pathname_prefix.split('/')[-1]
server = app.server
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montreal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)#,host='0.0.0.0')#,port=80)
