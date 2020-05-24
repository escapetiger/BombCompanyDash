import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
from app import cache, app

import io
import xlsxwriter
import flask
from flask import send_file
import uuid

session_id = str(uuid.uuid4())
dt_columns = ['ID', 'flag', 'area', 'field', 'company_type']
def get_full_data(session_id):
    @cache.memoize()
    def full_data(session_id):
        df = pd.read_csv('./data/pred_full_results.csv', index_col=0)
        return df
    return full_data(session_id)

def filter(df, area, field, company_type):
    df = df[['ID', 'flag', 'area', 'field', 'company_type']]
    df = df[(df['area'].isin(area)) & (df['field'].isin(field)) & (df['company_type'].isin(company_type))]
    df = df[df['flag'] == 1]
    return df

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
                # Card Body
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4('地区:',className='mb-0'),
                            dcc.Dropdown(
                                options=[
                                    {'label': '山东', 'value': '山东'},
                                    {'label': '广东', 'value': '广东'},
                                    {'label': '广西', 'value': '广西'},
                                    {'label': '江西', 'value': '江西'},
                                    {'label': '湖北', 'value': '湖北'},
                                    {'label': '湖南', 'value': '湖南'},
                                    {'label': '福建', 'value': '福建'},
                                ],
                                id='area',
                                value=['山东', '广东'],
                                multi=True)
                        ], className='form-group'),
                        html.Div([
                            html.H4('行业:', className='mb-0'),
                            dcc.Dropdown(
                                options=[
                                    {'label': '交通运输业', 'value': '交通运输业'},
                                    {'label': '商业服务业', 'value': '商业服务业'},
                                    {'label': '工业', 'value': '工业'},
                                    {'label': '服务业', 'value': '服务业'},
                                    {'label': '社区服务', 'value': '社区服务'},
                                    {'label': '零售业', 'value': '零售业'},
                                ],
                                id='field',
                                value=['交通运输业'],
                                multi=True),
                        ], className='form-group'),
                        html.Div([
                            html.H4('公司类型:', className='mb-0'),
                            dcc.Dropdown(
                                options=[
                                    {'label': '农民专业合作社', 'value': '农民专业合作社'},
                                    {'label': '合伙企业', 'value': '合伙企业'},
                                    {'label': '有限责任公司', 'value': '有限责任公司'},
                                    {'label': '股份有限公司', 'value': '股份有限公司'},
                                    {'label': '集体所有制企业', 'value': '集体所有制企业'},
                                ],
                                id='company_type',
                                value=['农民专业合作社'],
                                multi=True),
                        ], className='form-group'),

                    ]),
                    html.Div([
                        dash_table.DataTable(
                        id='datatable1',
                        columns=[{"name": i, "id": i, 'deletable': True} for i in dt_columns],
                        editable=False,
                        style_table={
                            'overflowY': 'scroll',
                            'width': '979px',
                            'minWidth': '100%',
                            'maxHeight': '75ex'
                        },
                        row_selectable="multi",
                        style_cell={
                            'fontFamily': 'Open Sans',
                            'textAlign': 'center',
                            'height': '60px',
                            'padding': '2px 22px',
                            'whiteSpace': 'inherit',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                        },
                        style_header={'fontWeight': 'bold',},
                        css=[{'selector': '.dash-cell div.dash-cell-value',
                              'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
                        ),
                        html.Span([
                            html.Button(
                                html.Span(html.H4('下载', className='mb-0')),
                                id='download_btn',
                                className='btn btn-lg iq-bg-success')
                        ], className='float-right'),
                        html.Div(children=session_id, id='session_id', style={'display': 'none'})
                    ], id='table', className='table-editable')
                ], className='iq-card-body')
            ], className='iq-card')
        ], className='row')
    ], className='container-fluid')
], className='content-page')

@app.callback(
    Output('datatable1', 'data'),
    [Input('area', 'value'),
     Input('field', 'value'),
     Input('company_type', 'value'),
     Input('session_id', 'children')]
)
def query(area, field, company_type, session_id):
    df = filter(get_full_data(session_id), area, field, company_type)
    return df.to_dict(orient='records')


# Callback for excel download
@app.callback(
    Output('download-link-ga-category', 'href'),
    [Input('download-button', 'n-clicks'),
     Input('area', 'value'),
     Input('field', 'value'),
     Input('company_type', 'value'),
     Input('session_id', 'children')]
)
def update_link(n_clicks, area, field, company_type, session_id):
    if n_clicks > 0:
        return '/bomb_company/query_result/urlToDownload?value={}/{}/{}'.format(area, field, company_type, session_id)


@app.server.route("/bomb_company/query_result/urlToDownload")
def download_excel():
    value = flask.request.args.get('value')
    #here is where I split the value
    value = value.split('/')
    area = value[0]
    field = value[1]
    company_type = value[2]
    session_id = value[3]

    filename = 'result.xlsx'
    df = get_full_data(session_id)

    buf = io.BytesIO()
    excel_writer = pd.ExcelWriter(buf, engine="xlsxwriter")
    download_1 = filter(df, area, field, company_type)
    download_1.to_excel(excel_writer, sheet_name="sheet1", index=False)
    # df.to_excel(excel_writer, sheet_name="sheet1", index=False)
    excel_writer.save()
    excel_data = buf.getvalue()
    buf.seek(0)

    return send_file(
        buf,
        mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        attachment_filename=filename,
        as_attachment=True,
        cache_timeout=0
    )

