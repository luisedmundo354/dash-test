import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np


app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

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




@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    Output(component_id='div-prob', component_property='children'),
    [Input(component_id='submit-button',component_property='n_clicks')],
    [State('input-prob','value')])
def update_output(n_clicks,input):
    r = np.sin(input)
    return 'Sin is "{}", tries "{}"'.format(r,n_clicks)

if __name__ == '__main__':
    app.run_server(debug=True)
