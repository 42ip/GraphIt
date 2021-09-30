import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import random
from dash_html_components import Button
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
df = pd.DataFrame()
external_stylesheets = [dbc.themes.BOOTSTRAP]
start = (0,0,0)
end = (15,34,22)
arr = [start]
increment = 5
dis = False
mesh = False
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
        html.Div([
            html.Div([
            html.Div(id='container-button-basic',
                            children='Increment by',style={'font-size':'18px','float':'left','color':'#cfcfcf'}),
                html.Div(dcc.Input(id='input-on-submit', type='text',value='5',
                            style={'width':'40px','text-align':'center','margin-left':'5px','color':'#cfcfcf','background-color':'#101010'})),
            html.Button('Update', id='submit-val',
                                                 style={'color':'#cfcfcf','background-color':'#101010','box-shadow': ' 0px 0px 3px 3px rgba(51,51,51,0.87)','border':'1.5px purple solid','text-align':'center','margin-top':'10px','margin-left':'5px','border-radius':'10px',}, n_clicks=0),
            html.Button('Pause', id='start-stop-button', n_clicks=0,style={'color':'#cfcfcf','background-color':'#101010','box-shadow': ' 0px 0px 3px 3px rgba(51,51,51,0.87)','border':'1.5px darkblue solid','margin-top':'10px','margin-left':'10px','text-align':'center','border-radius':'10px'}),
        ],style = {'margin-top':'10px','margin-left':'5px','display':'inline-block','width':'25%'}),
        html.Div([
            html.Div([
                html.Div(dcc.Input(id='start-ip', type='text',value='0 0 0',
                            style={'width':'80px','text-align':'center','margin-right':'10px','float':'right','color':'#cfcfcf','background-color':'#101010'})),
            html.Div(id='just-a-field1',
                            children='Start Point',style={'font-size':'18px','float':'right','margin-right':'5px','color':'#cfcfcf'}),
            ]),
            
            html.Br(),
            html.Br(),
            
            html.Div([
                html.Div(dcc.Input(id='end-ip', type='text',value='15 34 22',
                            style={'width':'80px','text-align':'center','margin-right':'10px','float':'right','color':'#cfcfcf','background-color':'#101010'})),
            html.Div(id='just-a-field2',
                            children='End Point',style={'font-size':'18px','float':'right','margin-right':'5px','color':'#cfcfcf'}),
            ]),
            html.Br(),
            html.Br(),
            html.Div([
                html.Button('Restart', id='reset-val',
                            style={'color':'#cfcfcf','background-color':'#101010','box-shadow': ' 0px 0px 3px 3px rgba(51,51,51,0.87)','border':'1.5px darkblue solid','text-align':'center','margin-top':'5px','margin-right':'5px','border-radius':'10px','float':'right'}, n_clicks=0),
                html.Button('Mesh', id='type-changer', n_clicks=0,style={'color':'#cfcfcf','background-color':'#101010','border':'1.5px purple solid','margin-top':'5px','margin-right':'10px','text-align':'center','border-radius':'10px','float':'right','box-shadow': ' 0px 0px 3px 3px rgba(51,51,51,0.87)'}),
                
            ]),
            
                
        ],style = {'margin-top':'5px','float':'right','display':'inline-block','width':'25%'}),
        ]),
        
        
         
        dcc.Graph(id='live-graph',style={'position':'relative','margin-top':'10%',}),
        dcc.Interval(
            id='graph-update',
            interval=2*1000,
            n_intervals = 0,
            disabled=False
        ),
    ],
    style={'background-color':'#101010'}
)

@app.callback(
    Output('type-changer','children'),
    [Input('type-changer', 'n_clicks')],
)
def callback_func_state_changer(button_clicks):
    global mesh
    if button_clicks is not None and button_clicks % 2 == 1:
        mesh = True
        return "Scatter"
    else:
        mesh = False
        return "Mesh"
@app.callback([Output('start-ip','value'),Output('end-ip','value')],[Input('reset-val', 'n_clicks')],[State('start-ip','value'),State('end-ip','value')])
def reseter(n_clciks,v1,v2):
    global start
    global end
    global arr
    st1 = [int(x) for x in v1.split()]
    st2 = [int(x) for x in v2.split()]
    start = (st1[0],st1[1],st1[2])
    end = (st2[0],st2[1],st2[2])
    arr = [start]
    return [v1,v2]
@app.callback(
    Output('input-on-submit', 'value'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('input-on-submit', 'value')])
def update_output(n_clicks, value):
    global increment
    increment = int(value)
    return str(increment)
@app.callback(
    [Output('graph-update', 'disabled'),Output('start-stop-button','children')],
    [Input('start-stop-button', 'n_clicks')],
    [State('graph-update', 'disabled')],
)
def callback_func_start_stop_interval(button_clicks, disabled_state):
    if button_clicks is not None and button_clicks % 2 == 1:
        return [True,'Resume']
    else:
        return [False,'Pause']
@app.callback(Output('live-graph', 'figure'),[Input('graph-update', 'n_intervals')])
def update_graph_scatter(input_data):
    global arr
    global mesh
    # print(df.head())
    val = arr[-1]
    # print(val)
    x = y = z = 0
    if val != end:
        x , y , z = val[0],val[1],val[2]
        x += random.randrange(-increment//2,increment+1)
        y += random.randrange(-increment//2,increment+1)
        z += random.randrange(-increment//2,increment+1)
        arr.append((x,y,z))
    else:
        x , y , z = val[0],val[1],val[2]
    x = [x[0] for x in arr]
    y = [x[1] for x in arr]
    z = [[i,x[2]] for i,x in enumerate(arr)] if mesh else [x[2] for x in arr]
    layout = go.Layout(
        title="3D Random Path Generation",
        height=700
        )
    if mesh:data = go.Figure(data=[go.Surface(x=x, y=y, z=z)],layout=layout)
    else:
        data = go.Figure(data=[go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines+markers',
        # template='plotly_dark',
        marker=dict(
        size=12,
        color=x,                # set color to an array/list of desired values
        colorscale='rainbow',   # choose a colorscale
        opacity=0.6
        ),
        line=dict(
            color=x,                # set color to an array/list of desired values
            colorscale='rainbow',
            showscale = True
        )
        )],layout=layout)
    data.update_layout(
        scene = dict(
                    xaxis = dict(
                         backgroundcolor="#101010",
                         gridcolor="#07285c",
                         showbackground=True,
                         zerolinecolor="white",),
                    yaxis = dict(
                        backgroundcolor="#101010",
                        gridcolor="#07285c",
                        showbackground=True,
                        zerolinecolor="white"),
                    zaxis = dict(
                        backgroundcolor="#101010",
                        gridcolor="#07285c",
                        showbackground=True,
                        zerolinecolor="white",),),
                        plot_bgcolor='#101010',paper_bgcolor='#101010')            
    return data

if __name__ == '__main__':
    app.run_server(debug=True)