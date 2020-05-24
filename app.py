# Initialize my app
import dash
import dash_auth
import dash_html_components as html
from flask_caching import Cache
# Create an app
# external_stylesheets = ['bWLwgP.css']
# external_stylesheets = [
#     {
#         'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css',
#         'rel': 'stylesheet',
#         'integrity': 'sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4',
#         'crossorigin': 'anonymous'
#     }
# ]
#
# external_scripts = [
#     {
#         'src': 'https://use.fontawesome.com/releases/v5.0.13/js/solid.js',
#         'integrity': 'sha384-tzzSw1/Vo+0N5UhStP3bvwWPq+uvzCMfrN1fEFe+xBmv1C/AtVX5K0uZtmcHitFZ',
#         'crossorigin': 'anonymous'
#     },
#     {
#         'src': 'https://use.fontawesome.com/releases/v5.0.13/js/fontawesome.js',
#         'integrity': 'sha384-6OIrr52G08NpOFSZdxxz1xdNSndlD4vdcf/q2myIUVO0VsqaGHJsB0RaBE01VTOY',
#         'crossorigin': 'anonymous'
#     },
#     {
#         'src': 'https://code.jquery.com/jquery-3.3.1.slim.min.js',
#         'integrity': 'sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo',
#         'crossorigin': 'anonymous'
#     },
#     {
#         'src': 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js',
#         'integrity': 'sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ',
#         'crossorigin': 'anonymous'
#     },
#     {
#         'src': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js',
#         'integrity': 'sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm',
#         'crossorigin': 'anonymous'
#     }
# ]


app = dash.Dash(
    __name__,
    meta_tags=[
        # A description of the app, used by e.g.
        # search engines when displaying search results.
        {
            'name': 'description',
            'content': 'My description'
        },
        # A tag that tells Internet Explorer (IE)
        # to use the latest renderer version available
        # to that browser (e.g. Edge)
        {
            'http-equiv': 'X-UA-Compatible',
            'content': 'Chrome'
        },
        # A tag that tells the browser not to scale
        # desktop widths to fit mobile screens.
        # Sets the width of the viewport (browser)
        # to the width of the device, and the zoom level
        # (initial scale) to 1.
        #
        # Necessary for "true" mobile support.
        {
          'name': 'viewport',
          'content': 'width=device-width, initial-scale=1.0, shrink-to-fit=no'
        }
    ],
    # external_scripts=external_scripts,
    # external_stylesheets=external_stylesheets,
    url_base_pathname='/bomb_company/'
)

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets, url_base_pathname='/bomb_company/')
server = app.server
app.title = 'Bomb Comapny'

app.config.suppress_callback_exceptions = True

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = [
    ['caiyi', '123']
]
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# Set Cache
cache = Cache(app.server, config={
    # 'CACHE_TYPE': 'redis',
    # Note that filesystem cache doesn't work on systems with ephemeral filesystem like Heroku
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory',

    # should be equal to maximum number of users on the app at a single time
    # higher numbers will store more data in the filesystem / redis cache
    'CACHE_THRESHOULD': 200
})
