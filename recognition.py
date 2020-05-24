import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
from app import cache, app

import base64
import io
import datetime
import pandas as pd
import uuid
import joblib

import preprocessing as pp

session_id = str(uuid.uuid4())

layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                # Card Title
                html.Div([
                    html.Div([
                        html.H2('条件查询', className='card-title')
                    ], className='iq-header-title'),
                ], className='iq-card-header d-flex justify-content-between'),
                html.Div([
                    # Card Body
                    html.Div([
                        # Instruction
                        html.Div(html.H4('请上传文件', className='mb-0')),
                        html.Div([
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                    ]),
                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                                multiple=True,
                                ),
                            ])
                        ], className='form-group'),
                    html.Div(id='output-upload-data', style={'width':'979px'}),
                    html.Div(
                        html.Button(
                        html.H4('查看分类结果', className='mb-0'),
                        id='submit-btn',
                        className='btn btn-lg iq-bg-success float-right',
                        type='submit',
                        n_clicks=0),
                    ),
                    html.Div(id='output-results', className='table-editable'),
                    html.Div(id='session_id', style={'display': 'none'})
                    ], className='iq-card-body')
                ], className='iq-card')
            ], className='row')
        ], className='container-fluid')
], className='content-page')
def parse(contents, filename, session_id):
    @cache.memoize()
    def read_data(contents, filename, session_id):
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in filename or 'xlsx' in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])
        return df
    return read_data(contents, filename, session_id)

def parse_contents(contents, filename, date, session_id):
    df = parse(contents, filename, session_id)
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # dash_table.DataTable(
        #     data=df.to_dict('records'),
        #     columns=[{'name': i, 'id': i} for i in df.columns],
        #     style_table={
        #         'overflowY': 'scroll',
        #         'overflowX': 'scroll',
        #         'maxWidth': '979px',
        #         'width': '979px',
        #         'minWidth': '100%',
        #         'maxHeight': '25ex'
        #     },
        #     style_header={'fontWeight': 'bold', },
        #     css=[{'selector': '.dash-cell div.dash-cell-value',
        #           'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
        #
        # ),

        html.Hr(),  # horizontal line

        # # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ])


@app.callback(Output('output-upload-data', 'children'),
              [Input('upload-data', 'contents'),
               Input('session_id', 'children')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, session_id, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d, session_id) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        children.append(html.H4('上传完毕'))
        children.append(html.Hr())
        return children

@app.callback(
    Output('output-results', 'children'),
    [Input('upload-data', 'contents'),
     Input('session_id', 'children'),
     Input('submit-btn', 'n_clicks')],
    [State('upload-data', 'filename')]
)
def recognition(list_of_contents, session_id, n_clicks, list_of_names):
    if n_clicks is not None and n_clicks > 0:
        df_list = [
            parse(c, n, session_id) for c, n in
            zip(list_of_contents, list_of_names)
        ]
        gbc = joblib.load('./model/gbc.m')
        base, knowledge, money_report, year_report = df_list[0], df_list[1], df_list[2], df_list[3]
        df = pp.merge_all_tables(base, knowledge, money_report, year_report)
        df = pp.convert_cat(df)
        df = pp.scaling(df)
        y_pred = gbc.predict(df.values)
        res = pd.DataFrame({
            'ID': base.ID,
            'label': y_pred
        })
        return html.Div([
            html.H3('分类结果'),
            dash_table.DataTable(
                data=res.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in res.columns],
                filter_action="native",
                style_table={
                    'overflowY': 'scroll',
                    'maxWidth': '979px',
                    'width': '779px',
                    'minWidth': '479px',
                    'maxHeight': '75ex'
                },
                style_cell={
                    'fontFamily': 'Open Sans',
                    'textAlign': 'center',
                    'height': '60px',
                    'padding': '2px 22px',
                    'whiteSpace': 'inherit',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                },
                style_header={'fontWeight': 'bold'},
                css=[{'selector': '.dash-cell div.dash-cell-value',
                      'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
            ),
        ], style={'text-align': 'center'})
