import dash
import dash_core_components as dcc
import dash_html_components as html

layout = html.Section([
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H1('Sign Up', className='mb-0'),
                    html.P('Enter your email address and password to access admin panel.'),
                    html.Form([
                        html.Div([
                            html.Label('Your Full Name'),
                            dcc.Input(type='text', id='InputFullName', placeholder='Your Full Name',
                                      className='form-control mb-0')
                        ], className='form-group'),
                        html.Div([
                            html.Label('Email Address'),
                            dcc.Input(type='email', id='InputEmail', placeholder='Enter email',
                                      className='form-control mb-0')
                        ], className='form-group'),
                        html.Div([
                            html.Label('Password'),
                            dcc.Input(type='password', id='InputPassword', placeholder='Enter password',
                                      className='form-control mb-0')
                        ], className='form-group'),
                        html.Div([
                            html.Div([
                                dcc.RadioItems(id='customCheck1', className='custom-control-input'),
                                html.Label([html.Span('I accept'), html.A('Terms and Conditions', href='#')],
                                           className='custom-control-label')
                            ], className='custom-control custom-checkbox d-inline-block mt-2 pt-1'),
                            html.Button('Sign Up', type='submit', className='btn btn-primary float-right')
                        ], className='d-inline-block w-100'),
                        html.Div([
                            html.Span("Already have an account?", className='dark-color d-inline-block line-height-2'),
                            html.A('Log In', href='./sign_in'),
                            html.Ul([
                                html.Li(html.A(html.I(className='ri-facebook-box-line'), href='#')),
                                html.Li(html.A(html.I(className='ri-twitter-line'), href='#')),
                                html.Li(html.A(html.I(className='ri-instagram-line'), href='#')),
                            ], className='iq-social-media')
                        ], className='sign-info')
                    ], className='mt-4')
                ], className='sign-in-from bg-white')
            ], className='col-sm-12 align-self-center')
        ], className='row no-gutters')
    ], className='container p-0')
], className='sign-in-page')
