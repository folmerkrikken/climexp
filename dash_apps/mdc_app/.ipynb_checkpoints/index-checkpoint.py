import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app_mdc import app2, server
from pages import kprep_mdc_forecast,kprep_mdc_sop,kprep_mdc_pp

# Describe the layout/ UI of the app2
app2.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Update page
@app2.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/kprep_mdc_forecast":
        return kprep_mdc_forecast.page_1_layout
    elif pathname == "/kprep_mdc_sop":
        return kprep_mdc_sop.page_2_layout
    elif pathname == "/kprep_mdc_pp":
        return kprep_mdc_pp.page_3_layout
    else:
        return kprep_mdc_forecast.page_1_layout

if __name__ == '__main__':
    app2.run_server(debug=True)
