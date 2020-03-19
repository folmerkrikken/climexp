import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#from app_kprep import app
from pages import kprep_sop,kprep_pp,kprep_overview


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://codepen.io/chriddyp/pen/brPBPO.css']

app = dash.Dash(
    __name__, 
    requests_pathname_prefix='/kprep_fc/',
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=external_stylesheets,
    routes_pathname_prefix='/kprep_fc/',
    )
#app.css.config.serve_locally = True
#app.scripts.config.serve_locally = True
server = app.server
app.config.suppress_callback_exceptions = True

# Describe the layout/ UI of the app2
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/kprep_fc/kprep_sop":
        return kprep_sop.page_1_layout
    elif pathname == "/kprep_fc/kprep_pp":
        return kprep_pp.page_2_layout(app)
    elif pathname == "/kprep_fc/kprep_overview":
        return kprep_overview.page_3_layout(app)
    else:
        return kprep_sop.page_1_layout(app)

if __name__ == '__main__':
    app.run_server(debug=True)
