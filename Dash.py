import time

from numpy import outer
from CompDash import runCode, generateText, runOBJ
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, callback_context
from dash.dependencies import Input, Output, State
global currentText, currentOBJ, compilationTime, cCode, cOBJ, compTable, compArray
compTable = pd.DataFrame()
compArray = []
currentText = None
currentOBJ = None
cCode = ""
cOBJ = ""
from Managers.prtManager import createPrintLogger, readPrinterLogger
compilationTime = 0

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
                            'width' : "95%", 
                            'font-size': '22px'}),
            ], style={ 'height' : '90%'}),
            html.Div(children = [
            html.Button('Ejecutar', id='executeCode'),
            html.Button('Crear OBJ', id='crearOBJ'),
            html.Button('Crear TXT', id='crearTXT'),
            html.Button('Eje .txt', id='execute_txt'),
            html.Button('Eje .obj', id='execute_obj')
            ], style = {'display': 'flex', 
                        'flex-direction': 'row', 
                        'marginLeft' : '10px',
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
                        dcc.Tabs([
                            dcc.Tab(label='Compilador', children = [
                                html.Div([
                                    dcc.Interval(id='interval1', interval=1 * 1000, n_intervals=0),
                                    dcc.Interval(id='interval2', interval= 100, n_intervals=0),
                                    html.H1(id='div-out', children=''),
                                    html.Iframe(id='console-out',srcDoc='',style={'width': '100%','height': "63vh", 'backgroundColor'  : 'white', 'font-size': '22px'})
                                ])

                            ]), 
                            dcc.Tab(label='Cuadruplos / Codigo', children = [
                                html.Div([
                                    html.Div([
                                        html.H1('Cuadruplos'), 
                                        html.Div(id='cuadruplosOutput', children = [
                                            "Aqui iran cuadruplos generados"
                                        ], style={'whiteSpace': 'pre-line', 'backgroundColor' : '#d1d7d7', 'height' : "60vh", 'width' : '70%', 
                                        'backgroundColor' : 'white', "display": "flex", "justifyContent": "center", 'padding' : 10,'font-size': '18px', "overflow": "scroll"})
                                    ], style = {'padding': 10, 'flex': 1,  'display': 'flex', 'flex-direction': 'column', 'backgroundColor' : '#d1d7d7', 'align-items': 'center', 'justify-content': 'center'}),
                                    html.Div([
                                        html.H1('Código'), 
                                        html.Div(id='textOutput', children = [
                                            "Aqui iran el codigo utlizado"
                                        ], style={'whiteSpace': 'pre-line', 'backgroundColor' : '#d1d7d7', 'height' : "60vh", 'width' : '70%', 
                                        'backgroundColor' : 'white', "display": "flex", "justifyContent": "center", 'padding' : 10, 'textAlign' : "left", 'font-size': '18px', "overflow": "scroll"})
                                    ], style = {'padding': 10, 'flex': 1,  'display': 'flex', 'flex-direction': 'column', 'backgroundColor' : '#d1d7d7', 'align-items': 'center', 'justify-content': 'center'})
                                ], style = {'width' : "100%", 'textAlign' : "center", 'display': 'flex', 'flex-direction': 'row'})
                            ]), 
                            dcc.Tab(label='Graficos de compilacion', children = [
                                html.Div([                   
                                    html.Div([
                                        html.H1('Tiempo de Compilación'), 
                                        html.Div(id = "compilationTime", children = [
                                              "Aqui iran los Tiempos de compilacion", "Aqui iran los Tiempos de compilacion"
                                        ], style = {'width' : "100%", 'textAlign' : "center", 'whiteSpace': 'pre-line', 'backgroundColor' : 'white', 'height' : "60vh", 'width' : '100%'})    
                                    ], style = {'padding': 10, 'flex-direction': 'column', 'backgroundColor' : '#d1d7d7', 'align-items': 'center', 'justify-content': 'center', 'width' : "15rem"}),
                                    html.Div([
                                        html.H1('Grafica de Compilación'), 
                                        dcc.Graph(id="compilationGraph")
                                    ], style = {'padding': 10, 'flex': 1,  'display': 'flex', 'flex-direction': 'column', 'backgroundColor' : '#d1d7d7', 'align-items': 'center', 'justify-content': 'center'}),
                                    ], style = {'width' : "100%", 'textAlign' : "center", 'display': 'flex', 'flex-direction': 'row'})
                            ]), 
                            dcc.Tab(label='Graficos de memoria', children = [
                                html.Div([
                                ], style = {'backgroundColor' : 'green'})
                            ]), 
                            ]),
                        
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
        children = [filename]
        return children
    else: 
        return []


@app.callback(Output('objFileName', 'children'),
              Input('uploadObj', 'contents'),
              State('uploadObj', 'filename'))
def update_output(content, filename):
    global currentOBJ
    if filename != None:
        import base64
        arr = content.split(",")
        if arr[0] == "data:application/octet-stream;base64" or ".obj" not in filename:
            code = base64.b64decode(arr[1])
            currentText = code.decode("utf-8")
            currentOBJ = currentText.splitlines( )
        else:
            print("ERROR")
        #runCode(code, generateOBJ)
        children = [filename]
        return children
    else:
        return []

@app.callback(
    Output('cuadruplosOutput', 'children'),
    Output('textOutput', 'children'),
    Output('compilationTime', 'children'),
    Output('compilationGraph', 'figure'),
    Input('executeCode', 'n_clicks'),
    Input('crearOBJ', 'n_clicks'),
    Input('crearTXT', 'n_clicks'),
    Input('textInput', 'value'), 
    Input('execute_txt', 'n_clicks'),
    Input('execute_obj', 'n_clicks')
)
def displayClick(btn1, btn2, btn3, code, bt4, bt5):
    global compilationTime, currentText, currentOBJ, cCode, cOBJ, compArray
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'executeCode' in changed_id:
        st = time.time()
        cCode, cOBJ = runCode(code, False, False)
        et = time.time()
        compilationTime = et - st
        cOBJ = parseCuad(cOBJ)        
        compArray.append(compilationTime)
        compList = parseCompTime(compArray)
        figComp = plotCompGraph(compArray)
        return cOBJ, cCode, compList, figComp
    elif 'crearOBJ' in changed_id:
        st = time.time()
        cCode, cOBJ = runCode(code, True, False)
        et = time.time()
        compilationTime = et - st
        cOBJ = parseCuad(cOBJ)
        compArray.append(compilationTime)
        compList = parseCompTime(compArray)
        figComp = plotCompGraph(compArray)
        return cOBJ, cCode, compList, figComp
    # Si el usuario quiere tendra la opcion de descargar el txt
    elif 'crearTXT' in changed_id:
        generateText(code)
    elif 'execute_txt' in changed_id:
        if currentText == None:
            print("NO TXT") 
        else:
            cCode, cOBJ = runCode(currentText, False, True)
            cOBJ = parseCuad(cOBJ)
            compArray.append(compilationTime)
            parseCompTime(compArray)
            figComp = plotCompGraph(compArray)
            return cOBJ, cCode, compList, figComp
    elif 'execute_obj' in changed_id:
        if currentOBJ == None:
            print("NO OBJ")
        else:
            cCode = ""
            st = time.time()
            cOBJ = runOBJ(currentOBJ)
            et = time.time()
            compilationTime = et - st
            cOBJ = parseCuad(cOBJ)
            compArray.append(compilationTime)
            compList = parseCompTime(compArray)
            figComp = plotCompGraph(compArray)
            return cOBJ, cCode, compList, figComp


    return "", "", "", plotCompGraph(compArray)

def parseCuad(cuad):
    c = 0
    st = ""
    for item in cuad:
       st += str(c) + ".  " + str(item.op) + ",  " + str(item.rightop) + ",  " + str(item.leftop) + ",  " + str(item.top) + "\n"
       print(st) 
       c += 1   
       
    return st

def parseCompTime(compArr):
    st = ""
    for value in compArr:
        st += str(round(value, 5)) + "\n"

    return st

def plotCompGraph(array):
    array = array[-50:]
    df = pd.DataFrame()
    df["Comp Time"] = array
    df["At"] = df.index
    
    fig = px.line(df, 
              x="At", 
              y="Comp Time", 
              labels={
                     "Comp Time": "Tiempo en ejecutar (s)",
                     "At": "compilación"
              },
              title='Tiempo de compilación')
    fig.update_layout(
        font_family="Times New Roman",
        font_color="Black",
        title_font_family="Times New Roman",
        width=1000, height=700,
        title_font_color="Black",
    )
    return fig

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

