import time
from CompDash import runCode, generateText

from dash import Dash, dcc, html, callback_context
from dash.dependencies import Input, Output, State
global currentText, cubrrentOBJ, compilationTime
from Managers.prtManager import createPrintLogger, readPrinterLogger
compilationTime = 0
import sys

createPrintLogger()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1(children='CompDash'),
        html.H3(children='Antonio Gonzalez A01194261'),
        html.H3(children='Gerardo Peart A01194337'),], 
        style={'width' : "100%", 
                'textAlign' : "center", 
                'backgroundColor' : '#8b9b9b', 
                'padding' : 10, 
                'color' : 'white', 
                'height' : '12vh'}),
    html.Div([
        # Columna 1
        html.Div(children=[
            html.Div(children = [
                    dcc.Upload(
                    id='uploadTxt',
                    children=['INGRESA CODIGO EJECUTABLE AQUI'],
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    }
                ), 
                ], style = {"display": "flex", 
                            "justifyContent": "center",
                            'padding' : 10}
            ),    
            html.Div(id = "TextName", style={'whiteSpace': 'pre-line'}),
            html.Div(id="textArea", children = [
                dcc.Textarea(
                    id='textInput',
                    value='', 
                    draggable = False,
                    style={'flex' : 1, 
                            'padding' : 10,
                            'height' : "100%", 
                            'width' : "100%"}),
            ], style={ 'height' : '90%'}),
            html.Div(children = [
            html.Button('Ejecutar', id='executeCode'),
            html.Button('Crear OBJ', id='crearOBJ'),
            html.Button('Crear TXT', id='crearTXT'),
            ], style = {'display': 'flex', 
                        'flex-direction': 'row', 
                        'marginRight' : '10px', 
                        'marginTop' : '5px'}),
        ], style={'padding': 10, 
                      'flex': 1, 
                      'display': 'flex', 
                      'flex-direction': 'column', 
                      'backgroundColor' : '#d1d7d7', 
                      'height' : '82vh'}),

            # Columna 2
            html.Div(children=[
                html.Div(children = [
                    # Txt file upload
                    dcc.Upload( 
                        id = 'uploadObj', 
                        children = ['INGRESA ARCHIVO OBJ AQUI'],
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                    }
                    ), 
                    ], style = {"display": "flex", 
                                "justifyContent": "center",
                                'padding' : 10}
                ),
                html.Div(id = "objFileName", style={'whiteSpace': 'pre-line'}),
                html.Div([
                    dcc.Interval(id='interval1', interval=1 * 1000, n_intervals=0),
                    dcc.Interval(id='interval2', interval= 100, n_intervals=0),
                    html.H1(id='div-out', children=''),
                    html.Iframe(id='console-out',srcDoc='',style={'width': '100%','height': "67vh", 'backgroundColor'  : 'white'})
            ])
            ], style={'padding': 10, 
                      'flex': 1, 
                      'display': 'flex', 
                      'flex-direction': 'column', 
                      'backgroundColor' : '#d1d7d7', 
                      'height' : '82vh'}),
            ], style={'width' : "100%", 'textAlign' : "center",
                    'display': 'flex', 'flex-direction': 'row'}),
            html.Div(id="TextDiv", children = [])
        ], style={'backgroundColor' : '#878683', "overflowY": "auto", "overflowX": "auto"})


@app.callback(Output('TextName', 'children'),
              Input('uploadTxt', 'contents'),
              State('uploadTxt', 'filename'))
def update_output(content, filename):
    global currentText
    if filename != None:
        import base64
        arr = content.split(",")
        if arr[0] == "data:text/plain;base64" or ".txt" not in filename:
            code = base64.b64decode(arr[1])
            currentText = code.decode("utf-8")
        else:
            print("ERROR")
        #runCode(code, generateOBJ)
        children = [filename,  html.Button('Ejecutar', id='executeText', style={"margin-left": "15px"})]
        return children
    else: 
        return []


@app.callback(Output('objFileName', 'children'),
              Input('uploadObj', 'contents'),
              State('uploadObj', 'filename'))
def update_output(content, filename):
    global cubrrentOBJ
    if filename != None:
        import base64
        arr = content.split(",")
        if arr[0] == "data:application/octet-stream;base64" or ".obj" not in filename:
            code = base64.b64decode(arr[1])
            currentText = code.decode("utf-8")
            cubrrentOBJ = currentText.splitlines( )
        else:
            print("ERROR")
        #runCode(code, generateOBJ)
        children = [filename,  html.Button('Ejecutar', id='execute obj', style={"margin-left": "15px"})]
        return children
    else:
        return []

@app.callback(
    Output('TextDiv', 'children'), 
    Input('executeCode', 'n_clicks'),
    Input('crearOBJ', 'n_clicks'),
    Input('crearTXT', 'n_clicks'),
    Input('textInput', 'value')
)
def displayClick(btn1, btn2, btn3, code):
    global compilationTime
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'executeCode' in changed_id:
        st = time.time()
        runCode(code, False)
        et = time.time()
        compilationTime = et - st
    elif 'crearOBJ' in changed_id:
        st = time.time()
        runCode(code, True)
        et = time.time()
        compilationTime = et - st
    # Si el usuario quiere tendra la opcion de descargar el txt
    elif 'crearTXT' in changed_id:
        generateText(code)

@app.callback(Output('div-out', 'children'),
    [Input('interval1', 'n_intervals')])
def update_interval(n):
    global compilationTime
    return 'Compilation time ' + str(compilationTime)

@app.callback(Output('console-out', 'srcDoc'),
    [Input('interval2', 'n_intervals')])
def update_output(n):
    file = readPrinterLogger()
    data=''
    lines = file.readlines()
    if lines.__len__()<=1000:
        last_lines=lines
    else:
        last_lines = lines[-1000:]
    for line in last_lines:
        data=data+line + '<BR>'
    file.close()
    return data

if __name__ == '__main__':
    app.run_server(debug=True)