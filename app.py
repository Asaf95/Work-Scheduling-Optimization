import base64
import datetime
import io
import webbrowser
import dash
import pandas as pd
import plotly.express as px
from dash import dash_table,dcc ,html, callback_context
from dash.dependencies import Input, Output, State
import input_converter
from database import user_output_data as uod
import logging
import dash_bootstrap_components as dbc


def update_ui_output():
    fig2 = uod.get_gantt()
    return fig2


external_stylesheets, colors, basic_style, basic_style2 = uod.get_fronts()
# Using this for reading PDF file to show how to use in the dash


def get_logger():
    logging.basicConfig(level=logging.INFO, filename="logs", filemode="w",
                        format="%(asctime)s - lin  e: %(lineno)d - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('logs.test')
    formatter = logging.Formatter('%(asctime)s - line: %(lineno)d - module: %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


app = dash.Dash(__name__,external_stylesheets=external_stylesheets, suppress_callback_exceptions=True,)
app.title ='Work Scheduling Optimization'
app.layout = html.Div(style={'backgroundColor': colors['background']},
                      children=[
                          html.Br(),
                          html.Div([
                              html.Button('How To Use', id='btn-nclicks-1', n_clicks=0),
                              html.Button('Source Code', id='btn-nclicks-2', n_clicks=0),
                          ], style={'marginLeft': '75%'}),
                          html.Div(id='container-button-timestamp'),
                          html.H1("Work Scheduling Optimization", style= basic_style2),

                          dcc.Tabs([
                              dcc.Tab(label='User Input', children=[

                                  html.H5(
                                      "Please enter the number of the Machines and Workers",
                                      style=basic_style2),
                                  dcc.Input(id="input1", type="number", placeholder="Number of Machines A",
                                            style={'marginLeft': '20%', 'textAlign': 'center'}),
                                  dcc.Input(id="input2", type="number", placeholder="Number of Machines B", debounce=True,
                                            style={'textAlign': 'center','margin': '10px'}),
                                  dcc.Input(id="input3", type="number", placeholder="Number of Workers A", debounce=True,
                                            style={'textAlign': 'center'}),
                                  dcc.Input(id="input4", type="number", placeholder="Number of Workers B", debounce=True,
                                            style={'textAlign': 'center','margin': '10px'}),
                                  html.Hr(),
                                  html.H5(
                                      "Upload the file with the Jobs needed to be scheduled",
                                      style=basic_style2),
                                  html.Div(id="output", style={'textAlign': 'center', 'margin': '10px', }),

                                  dcc.Upload(
                                      id='upload-data',
                                      children=html.Div([
                                          'Drag and Drop or ',
                                          html.A('Select Files')
                                      ]),
                                      style=basic_style,
                                      # Allow multiple files to be uploaded
                                      multiple=True
                                  ),
                                  html.Div(id='output-div'),
                                  html.Div(id='output-datatable')
                              ]),
                              dcc.Tab(label='Solution Output', children=[
                                  html.Div([
                                      html.Button('Refresh Results', id='btn-nclicks-3', n_clicks=0)
                                  ], style=basic_style2),
                                  dcc.Graph(
                                      figure=update_ui_output()
                                  ),

                              ]),
                              dcc.Tab(label='Environment Configuration', children=[
                                  html.Br(),
                                  # get the job properties for each ID with how many resource and limitations
                                  html.H5("Jobs properties", style=basic_style2),
                                  html.Div(id="output-en", style={'textAlign': 'center', 'margin': '10px', }),

                                  dcc.Upload(
                                      id='upload-data-env-config-jobs-prop',
                                      children=html.Div([
                                          'Drag and Drop or ',
                                          html.A('Select Files')
                                      ]),
                                      style=basic_style,
                                      # Allow multiple files to be uploaded
                                      multiple=True
                                  ),
                                  html.Div(id='output-div-en'),
                                  html.Div(id='output_job_prop'),

                                  html.Br(),

                                  # the second csv file in env-config ui
                                  # get the Environment (machines) limitations
                                  html.Br(),
                                  html.H5("Machines properties", style=basic_style2),
                                  html.Div(id="output-en2", style={'textAlign': 'center', 'margin': '10px', }),

                                  dcc.Upload(
                                      id='upload-data-env-config-mach-prp',
                                      children=html.Div([
                                          'Drag and Drop or ',
                                          html.A('Select Files')
                                      ]),
                                      style=basic_style,
                                      # Allow multiple files to be uploaded
                                      multiple=True
                                  ),
                                  html.Div(id='output-div-en2'),
                                  html.Div(id='output_mach_prop'),
                                  html.Br(),
                              ]),

                          ]),
                      ])

"""
Main Page Callback
those functions are used to update the UI and to share the data with other models in the sw 
"""


def parse_contents(contents, filename, date):
    """
    this function handles the file that the user imported into the dashboard
    it's the only function that transform the csv file to ConvertData module

    :param contents:
    :param filename:
    :param date:
    :return:
    """
    logger = get_logger()
    try:
        if contents is not None:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            print(filename)
            if 'csv' or "Input_Job" in filename:
                print('the file name is in csv or Input_Job')
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
                print(df)
                input_converter.convert_user_jobs_csv(df, filename)
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
                input_converter.convert_user_jobs_csv(df, filename)
            # else:
            #     df = pd.read_csv(
            #         io.StringIO(decoded.decode('utf-8')))
            #     input_converter.convert_user_jobs_csv(df, filename)
            else:
                pass
    except Exception as e:
        print(f"""something went wrong in parse_contents() function while trying to use the function to upload the file
              {e} """)
        logger.error("USER DATA IS WRONG")
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        html.P("Inset X axis data"),
        dcc.Dropdown(id='xaxis-data',
                     options=[{'label': x, 'value': x} for x in df.columns]),
        html.P("Inset Y axis data"),
        dcc.Dropdown(id='yaxis-data',
                     options=[{'label': x, 'value': x} for x in df.columns]),
        html.Button(id="submit-button", children="Create Graph"),
        html.Hr(),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=15
        ),
        dcc.Store(id='stored-data', data=df.to_dict('records')),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser not will be in use in production
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


"""
this refers to the csv file that the user uploaded to the sw, the data inside it is hte tasks that he have.
"""

@app.callback(
    Output('container-button-timestamp', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks')
)
def displayClick(btn1, btn2, btn3):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn-nclicks-1' in changed_id:
        msg = ''
        webbrowser.open_new("database\how2use.pdf")
    elif 'btn-nclicks-2' in changed_id:
        msg = ''
        webbrowser.open('https://github.com/Asaf95/backup_WSO', new=0, autoraise=True)
    elif 'btn-nclicks-3' in changed_id:
        msg = ''
        update_ui_output()
        app.run_server(debug=True, use_reloader=False)
    else:
        msg = ''
    return html.Div(msg)


@app.callback(Output('output-datatable', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    logger = get_logger()
    try:
        if list_of_contents is not None:
            children = [
                parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
            return children
    except Exception as e:
        logger.error()
        print(f'problem was find while running the function update_output() in the main UI script. {e} ')


"""
this refers to the csv file that the user uploaded to the sw, the data inside it is hte tasks that he have.
"""


@app.callback(Output('output-div', 'children'),
              Input('submit-button', 'n_clicks'),
              State('stored-data', 'data'),
              State('xaxis-data', 'value'),
              State('yaxis-data', 'value'))
def make_graphs(n, data, x_data, y_data):
    logger = get_logger()
    try:
        if n is None:
            return dash.no_update
        else:
            bar_fig = px.bar(data, x=x_data, y=y_data)
            return dcc.Graph(figure=bar_fig)
    except Exception as e:
        logger.error()
        print(f'problem was find while running the function make_graphs() in the main UI script. {e} ')


"""
This variables are used for the user variables in Input tag 
"""


@app.callback(
    Output("output", "children"),
    Input("input1", "value"),
    Input("input2", "value"),
    Input("input3", "value"),
    Input("input4", "value"),
)
def update_output(input1, input2, input3, input4):
    logger = get_logger()
    if input1 and input2 and input3 and input4 is not None:
        logger.info("update_output function had run()")
        input_converter.convert_user_values(input1, input2, input3, input4)  # convert the user input to the backen
        return u'Input 1 {} and Input 2 {} and input 3 {} and input 4 {}'.format(input1, input2, input3, input4)
    else:
        pass


"""
Environment Configuration first csv file 
EnvCon-Jobs-Properties
"""


@app.callback(Output('output_job_prop', 'children'),
              Input('upload-data-env-config-jobs-prop', 'contents'),
              State('upload-data-env-config-jobs-prop', 'filename'),
              State('upload-data-env-config-jobs-prop', 'last_modified'))
def update_output_job_prop(list_of_contents, list_of_names, list_of_dates):
    get_logger()
    try:
        if list_of_contents is not None:
            logger.info(f'Start of the Function with the following args '
                        f'list_of_contents {list_of_contents} list_of_names {list_of_names} list_of_dates {list_of_dates}')
            children = [
                parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
            return children
    except Exception as e:
        logger.error()
        print(f'problem was find while runing the function update_output() in the main UI script. {e} ')


@app.callback(Output('output_mach_prop', 'children'),
              Input('upload-data-env-config-mach-prp', 'contents'),
              State('upload-data-env-config-mach-prp', 'filename'),
              State('upload-data-env-config-mach-prp', 'last_modified'))
def update_mach_prop(list_of_contents, list_of_names, list_of_dates):
    logger = get_logger()
    try:
        if list_of_contents is not None:
            logger.info("the function update_mach_prop is in use now")
            children = [
                parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
            logger.info('End of the Function')
            return children
    except Exception as e:
        logger.error()
        print(f'problem was find while running the function update_output() in the main UI script. {e} ')


if __name__ == '__main__':
    logger = get_logger()
    webbrowser.open('http://127.0.0.1:8050/', new=1, autoraise=True)
    app.run_server(debug=True, use_reloader=False)
