import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd


app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

#Read the csv
df = pd.read_csv('https://s3.us-east-2.amazonaws.com/stats-app-assets/zscores.csv', names=['z','probability'])
df.apply(pd.to_numeric)


app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value'),
    dcc.Input(id='input-prob', value='initial value', type='text'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div(id='div-prob')
])



#First function
@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
#Second function
@app.callback(dash.dependencies.Output(component_id='div-prob', component_property='children'),
[dash.dependencies.Input(component_id='submit-button',component_property='n_clicks')],
[dash.dependencies.State('input-prob','value')])
def update_output(n_clicks,input):
    ap=10
    p=0
    for index,row in df.iterrows():
        d = abs(row['probability']-input)
        if d < ap:
            ap = d
            p = row['probability']
    r=df.loc[df['probability']==p,'z']
    return 'z is "{}", tries "{}"'.format(r.iloc[1] if input>0.5 else r.iloc[0],n_clicks)

if __name__ == '__main__':
    app.run_server(debug=True)
