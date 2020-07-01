import dash_html_components as html
import dash_core_components as dcc
import os


def Header_sop(app):
    return html.Div([get_header(app), html.Br([]), get_menu_sop()])

def Header_pp(app):
    return html.Div([get_header(app), html.Br([]), get_menu_pp()])

def Header_overview(app):
    return html.Div([get_header(app), html.Br([]), get_menu_overview()])

    #return html.Div([get_menu()])
bd = '/home/oldenbor/climexp/KPREPData/'
if not os.path.isdir(bd):
    bd = '/home/folmer/climexp/KPREPData/'
bdnc = bd+'ncfiles/'

info =  {'plottypes':{'Correlation':'cor','RMSESS':'rmsess','CRPSS (clim)':'crpss','CRPSS (S5)':'crpss_s5','Tercile summary plot':'tercile','Forecast anomalies':'for_anom'},
        'variables':{'Temperature':'GCEcom','Precipitation':'GPCCcom','Sea-level pressure':'20CRslp'},
        'variables_prad':{'Temperature':'GCEcom','Precipitation':'GPCCcom','Sea-level pressure':'20CRslp'},
        'variables_pred':{'CO2':'CO2EQ','NINO34':'NINO34','PDO':'PDO','AMO':'AMO','IOD':'IOD','PREC':'CPREC','PERS':'PERS','PERS_TREND':'PERS_TREND'},
        'bdnc':bdnc,
        'clickData':dict({u'points': [{u'y': -8., u'x': 21., u'pointNumber': 6, u'curveNumber': 632}]}),        
        }

info_sop = '**This page allows to study the sources of predictability of the forecasting system. By selecting a grid point on Figure 1, Figure 2-4 show the data for that gridpoint. The figures show the contribution of the individual predictors to the forecasted anomaly (Fig 2), the historical forecasts (Fig 3) and the timeseries of the individual predictors and its contribution to the forecasted anomaly (Fig 4).**'

info_pp = '**This page allows to study the individual relations between the predictand and the predictor**'

info_overview = '**This page presents an overview of the forecasting system - not done yet..**'
# Stippled where not significant at 10% level
info_titles = {'Temperature':'Surface air temperature',
               'Precipitation':'Surface precipitation',
               'Sea-level pressure':'Mean sea level pressure',
               'Forecast anomalies':['Ensemble mean anomaly (wrt 1980-2010 clim.)',''],
               'Correlation':'',
               'RMSESS':['RMSESS hindcasts, reference: climatology (1961-current)',''],
               'CRPSS (clim)':['CRPSS hindcasts, reference: climatology (1961-current)',''],
               'CRPSS (S5)':['CRPSS hindcasts, reference: ECMWF S5 (1981-current)',''],
               'Tercile summary plot':['Probability of most likely tercile (wrt to 1961-2019 hindcasts)',''],
               'Correlation':['Correlation between hindcast and observations (1961-current)','Stippled where significant at 5% level']
              }

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
                            #html.Div(children='This application can be used to explore the seasonal forecasts of the KPREP empirical forecasting system. The seasonal forecasts are based on a statistical emprical forecasting model, which uses past observations to deduce relations between the weather in the last three months (up to the beginning of the month) and the weather over the next months (from the end of the month). The main predictors are large scale climate indices (such as e.g. El Nino) and the trends due to global warming. The system has been documented in Eden et al. 2015 '),#,style=style_box),
                            dcc.Markdown('**This application can be used to explore the seasonal forecasts of the KPREP empirical forecasting system. The seasonal forecasts are based on a statistical emprical forecasting model, which uses past observations to deduce relations between the weather in the last three months (up to the beginning of the month) and the weather over the next months (from the end of the month). The main predictors are large scale climate indices (such as e.g. El Nino) and the trends due to global warming. The system has been documented in [Eden et al. 2015](https://doi.org/10.5194/gmd-8-3947-2015)**'),
                            html.Br(),
                            dcc.Markdown('**This app is constructed using [Dash](https://plotly.com/dash/), a web application framework for Python. Any questions, suggestion or comments mail [folmer.krikken@knmi.nl](mailto:folmer.krikken@knmi.nl)**'),#,,style=style_box),
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