# EXPAND STOCK SYMBOL INPUT TO PERMIT MULTIPLE STOCK SELECTION
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
#import pandas_datareader.data as web # requires v0.6.0 or later
from datetime import datetime
import pandas as pd
import yfinance as yf
import os
print(os.getcwd())
nsdq = pd.read_csv(r'C:\Users\Dalton\Desktop\Python Projects\Stock Dashboard\data\NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)
options = []
for tic in nsdq.index:
    options.append({'label':'{} {}'.format(tic,nsdq.loc[tic]['Name']), 'value':tic})

app = dash.Dash()

colors = {
    'background': 'rgb(80,80,80)',
    'graphs':'rgb(40,40,40)',
    'text': 'rgb(50,50,100)'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1('Stock Ticker Dashboard',
        style={
            'color':colors['text'],
            'paddingLeft':'48px'}),
    html.Div([
        html.H3('Select stock symbols:',
            style={
                'color':colors['text'],
                'paddingRight':'42px',
                'width':'30%'}),
        dcc.Dropdown(
            id='ticker_symbol',
            options=options,
            value=['AAPL'],
            multi=True,
        )
    ], style={'display':'inline-block',
                'verticalAlign':'top',
                'width':'30%',
                'paddingLeft':'48px'}),
    html.Div([
        html.H3('Select start and end dates:',
                style={'paddingLeft':'42px',
                        'color':colors['text']}),
        dcc.DatePickerRange(
            id='my_date_picker',
            min_date_allowed=datetime(2015, 1, 1),
            max_date_allowed=datetime.today(),
            start_date=datetime(2020, 1, 1),
            end_date=datetime.today(),
            style={'paddingLeft':'40px','paddingBottom':'5px'}
        )
    ], style={'display':'inline-block'}),
    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize':24, 'marginLeft':'30px'}
        ),
    ], style={'display':'inline-block'}),
    dcc.Graph(
        id='my_graph',
        style={'color': colors['background'],
                'paddingLeft':'50px',
                'paddingRight':'50px'},
        figure={
            'data': [
                {'x': [1,2], 'y': [3,1]}
            ]
        }
    )
])

@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('ticker_symbol', 'value'),
    State('my_date_picker', 'start_date'),
    State('my_date_picker', 'end_date')])
def refreshData(n_clicks, options, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    delta = end - start
    if int(delta.days) > 59:
        traces = []
        for tic in options:
            stockdf = yf.download(tic, start=start, end=end)
            traces.append({'x':stockdf.index, 'y':stockdf.Close,'name':tic})
        fig = {
            'data': traces,
            'layout': {'title':', '.join(options)+' Closing Prices'}
        }
        return fig
    else:
        traces = []
        for tic in options:
            stockdf = yf.download(tic, interval="15m", start=start, end=end)
            traces.append({'x':stockdf.index, 'y':stockdf.Close,'name':tic})
        fig = {
            'data': traces,
            'layout': {'title':', '.join(options)+' Closing Prices'}
        }
        return fig

if __name__ == '__main__':
    app.run_server()
