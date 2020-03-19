# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

base_times = dict(zip(['March','April','May','June','July','August','September','October'],range(3,11)))
valid_times = dict(zip(['April','May','June','July','August','September','October'],range(4,11)))

all_options = {
    'America': ['New York City', 'San Francisco', 'Cincinnati'],
    'Canada': [u'Montréal', 'Toronto', 'Ottawa']
}
app.layout = html.Div([
    dcc.Dropdown(
        id='base_time',
        options=[{'label': k, 'value': k} for k in base_times.keys()],
        value='March'
    ),

    html.Hr(),

    dcc.Dropdown(id='valid_time'),

    html.Hr(),

    html.Div(id='display-selected-values')
])


@app.callback(
    Output('valid_time', 'options'),
    [Input('base_time', 'value')])
def set_cities_options(base_time):
    #print(selected_country)
    print(base_time)
    tmp_options = dict([(i,base_times[i]) for i in list(base_times)[list(base_times).index(base_time)+1:]])
    print('options',tmp_options)
    #print([{'label': i, 'value': i} for i in all_options[base_time]])
    return [{'label': i,'value': i} for i in tmp_options.keys()]
    #return [{'label': i, 'value': i} for i in all_options[base_time]]


@app.callback(
    Output('valid_time', 'value'),
    [Input('valid_time', 'options')])
def set_cities_value(available_options):
    print('avail options',available_options)
    print('value',available_options[0]['value'])
    #return list(available_options.keys())[0]
    return available_options[0]['value']


@app.callback(
    Output('display-selected-values', 'children'),
    [Input('base_time', 'value'),
     Input('valid_time', 'value')])
def set_display_children(selected_country, selected_city):
    return u'{} is a city in {}'.format(
        selected_city, selected_country,
    )


if __name__ == '__main__':
    app.run_server(debug=True)