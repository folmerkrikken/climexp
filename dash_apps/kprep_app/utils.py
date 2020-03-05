import dash_html_components as html
import dash_core_components as dcc


def Header_sop(app):
    return html.Div([get_header(app), html.Br([]), get_menu_sop()])

def Header_pp(app):
    return html.Div([get_header(app), html.Br([]), get_menu_pp()])

def Header_overview(app):
    return html.Div([get_header(app), html.Br([]), get_menu_overview()])

    #return html.Div([get_menu()])



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
                    html.H3('KPREP seasonal empirical forecasting system',style={"margin-bottom":"0px","textAlign":'center'}),
                    html.H5('Temperature  -  Precipitation  -  Sea level pressure',style={"margin-top":"0px","textAlign":'center'}),
                    ],
                    className='app-header',
                    #style={'font-size':'32'},
                    ),
                    html.Br(),
                    html.Div(
                        [
                        html.Div(
                            [
                            html.Div(children='This application can be used to explore the seasonal forecasts of the KPREP empirical forecasting system. The seasonal forecasts is based on a statistical emprical forecasting model, which uses past observations to deduce relations between the weather in the last three months (up to the beginning of the month) and the weather over the next months (from the end of the month). The main predictors are large scale climate indices (such as e.g. El Nino), the trends due to global warming and the previous value of the MDC. Overfitting is avoided as much as possible. The system has been documented in Eden et al. 2015 and Eden et al. 2019.'),#,style=style_box),
                            html.Br(),
                            html.Div(children='This app is constructed using Dash, a web application framework for Python. Any questions, suggestion or comments mail folmer.krikken@knmi.nl'),#,,style=style_box),
                            ],style=style_box),#{'textAlign':'center'}),
                        ],style={'textAlign':'center'}),
                ])
            
    return header


def get_menu_sop():
    menu = html.Div(
        [
            dcc.Link(
                "Forecasts - Sources of Predictability",
                href="/kprep_fc/kprep_sop",
                className="tab first selected",
            ),
            dcc.Link(
                "Predictor - Predictand relations",
                href="/kprep_fc/kprep_pp",
                className="tab",
            ),
            dcc.Link(
                "Overview forecasting system",
                href="/kprep_fc/kprep_overview",
                className="tab",
            ),
        ],
        className="row all-tabs",
        style={'textAlign':'center'}
    )
    return menu

def get_menu_pp():
    menu = html.Div(
        [
            dcc.Link(
                "Forecasts - Sources of Predictability",
                href="/kprep_fc/kprep_sop",
                style={'fontColor': 'blue'},
                className="tab first",
            ),
            dcc.Link(
                "Predictor - Predictand relations",
                href="/kprep_fc/kprep_pp",
                className="tab selected",
            ),
            dcc.Link(
                "Overview forecasting system",
                href="/kprep_fc/kprep_overview",
                className="tab",
            ),
        ],
        className="row all-tabs",
        style={'textAlign':'center'}
    )
    return menu

def get_menu_overview():
    menu = html.Div(
        [
            dcc.Link(
                "Forecasts - Sources of Predictability",
                href="/kprep_fc/kprep_sop",
                className="tab first",
            ),
            dcc.Link(
                "Predictor - Predictand relations",
                href="/kprep_fc/kprep_pp",
                className="tab",
            ),
            dcc.Link(
                "Overview forecasting system",
                href="/kprep_fc/kprep_overview",
                className="tab selected",
            ),
        ],
        className="row all-tabs",
        style={'textAlign':'center'}
    )
    return menu