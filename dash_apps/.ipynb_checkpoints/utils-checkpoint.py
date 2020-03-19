import dash_html_components as html
import dash_core_components as dcc


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])
    return html.Div([get_menu()])



style_box = {'width': '60%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': '#DCDCDC',# '#f9f9f9',
                                 'padding': '10px',
                                 'margin-bottom': '10px',
                                 'margin-left': '10px',
                                 'textAlign':'center',
            }

def get_header(app):
    header = html.Div(
                [
                html.Div(
                    [
                    html.H3('KPREP empirical forecasting system',style={"margin-bottom":"0px","textAlign":'center'}),
                    html.H5('Monthly Drought Code / Fire weather risk',style={"margin-top":"0px","textAlign":'center'}),
                    ],
                    className='app-header',
                    ),
                    html.Br(),
                    html.Div(
                        [
                        html.Div(
                            [
                            html.Div(children='This application can be used to assess the fire weather risk, quantified by the monthly drought code, for the following fire season. The seasonal forecasts is based on a statistical emprical forecasting model, which uses past observations to deduce relations between the weather in the last three months (up to the beginning of the month) and the weather over the next months (from the end of the month). The main predictors are large scale climate indices (such as e.g. El Nino), the trends due to global warming and the previous value of the MDC. Overfitting is avoided as much as possible. The system has been documented in Eden et al. 2015 and Eden et al. 2019.'),#,style=style_box),
                            html.Br(),
                            html.Div(children='This app is constructed using Dash, a web application framework for Python. Any questions, suggestion or comments mail folmer.krikken@knmi.nl'),#,,style=style_box),
                            ],style=style_box),#{'textAlign':'center'}),
                        ],style={'textAlign':'center'}),
                ])
            
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Forecasts Fire Weather",
                href="/",
                className="tab first",
            ),
            dcc.Link(
                "Research page: Sources of predictability",
                href="/kprep-mdc-sop",
                className="tab",
            ),
            dcc.Link(
                "Research page: Predictor - Predictand relationships",
                href="/kprep-mdc-pp",
                className="tab",
            ),
        ],
        className="row all-tabs",
        style={'textAlign':'center'}
    )
    return menu