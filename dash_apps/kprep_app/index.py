import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app_kprep import app,server
from pages import kprep_sop,kprep_pp,kprep_overview

# Describe the layout/ UI of the app2


# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    print('!!!!!!!!!!!pathname',pathname)
    if pathname == "/kprep_fc/kprep_sop":
        return kprep_sop.page_1_layout
    elif pathname == "/kprep_fc/kprep_pp":
        return kprep_pp.page_2_layout
    elif pathname == "/kprep_fc/kprep_overview":
        return kprep_overview.page_3_layout
    else:
        return kprep_sop.page_1_layout

#server = app.server    
print('__name__',__name__)
if __name__ == '__main__':
    app.run_server(debug=True,threaded=True)
