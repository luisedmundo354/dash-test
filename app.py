import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import functions as fun
import math


app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

#Read the csv
df = pd.read_csv('https://s3.us-east-2.amazonaws.com/stats-app-assets/zscores.csv', names=['z','probability'])
df.apply(pd.to_numeric)
op = df['probability'].values

markdown_significance='''Significance level \u03B2'''
markdown_power='''Statistical power 1 - $\beta$:'''
uni = u'\u03B2'

app.layout = html.Div([
    html.H2('Basic Stats'),
    html.Label('Write the p-value:'),
    dcc.Dropdown(id='input-prob1', options=[{'label': round((1-i)*100,3), 'value': i} for i in op], value=''),
    html.Button(id='submit-button1', n_clicks=0, children='Submit'),
    html.Div(id='display-result1'),

    html.Label('Insert the p-value:'),
    dcc.Input(id='input-prob2', type='text', value='0.96'),
    html.Button(id='submit-button2', n_clicks=0, children='Submit'),
    html.Div(id='display-result2'),

    html.H3('Sample size for two independent samples, dichotomous outcomes'),
    html.Label('Baseline proportion:'),
    dcc.Input(id='baseline-proportion', type='text',value=''),
    html.Label('Minimum detectable effect relative:'),
    dcc.Input(id='detectable-effect', type='text',value=''),
    html.Label('Statistical power 1 -'+u'\u03B2'+':'),
    dcc.Input(id='statistical-power', type='text',value=''),
    html.Label('Significance level '+u'\u03B1'+':'),
    dcc.Input(id='significance-level', type='text',value='0.05'),
    html.Button(id='submit-button3', n_clicks=0, children='Submit'),
    html.Div(id='display-result3'),
])



#First function
@app.callback(dash.dependencies.Output(component_id='display-result1', component_property='children'),
[dash.dependencies.Input(component_id='submit-button1',component_property='n_clicks')],
[dash.dependencies.State('input-prob1','value')])
def display_value(n_clicks,input):
    r=df.loc[df['probability']==input,'z']
    return 'z is "{}", tries "{}"'.format(abs(r.iloc[0]),n_clicks)
#Second function
@app.callback(dash.dependencies.Output(component_id='display-result2', component_property='children'),
[dash.dependencies.Input(component_id='submit-button2',component_property='n_clicks')],
[dash.dependencies.State('input-prob2','value')])
def update_output(n_clicks,input):
    r = fun.search_z(float(input))
    return 'z is "{}", tries "{}"'.format(r,n_clicks)


@app.callback(dash.dependencies.Output(component_id='display-result3', component_property='children'),
[dash.dependencies.Input(component_id='submit-button3',component_property='n_clicks')],
[dash.dependencies.State('baseline-proportion','value'),
dash.dependencies.State('detectable-effect','value'),
dash.dependencies.State('statistical-power','value'),
dash.dependencies.State('significance-level','value')])
def sample_output(n_clicks,baseline,detectable,power,significance):
    za = fun.search_z(1-float(significance)/2)
    zb = fun.search_z(float(power))
    p1=(float(detectable)+1)*float(baseline)
    p=(p1+float(baseline))/2
    es=abs(p1-float(baseline))/math.sqrt(p*(1-p))
    ssize = 2*((za+zb)/es)**2
    return 'The sample size should be "{}", tries "{}"'.format(ssize,n_clicks)



if __name__ == '__main__':
    app.run_server(debug=True)
