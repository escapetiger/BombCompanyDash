import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app
import add_user
import sign_in
import sign_up
import query
import recognition

app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
        </head>
        <body>
    
            <div class="wrapper">
                <div class="iq-sidebar">
                    <div class="iq-sidebar-logo d-flex justify-content-between">
                       <a href="./bombcompany">
                       <img src="./assets/images/logo.gif" class="img-fluid" alt="">
                       <span>Bomb</span>
                       </a>
                       <div class="iq-menu-bt align-self-center">
                          <div class="wrapper-menu">
                             <div class="line-menu half start"></div>
                             <div class="line-menu"></div>
                             <div class="line-menu half end"></div>
                          </div>
                       </div>
                    </div>
                    <div id="sidebar-scrollbar">
                       <nav class="iq-sidebar-menu">
                          <ul class="iq-menu">
                             <li class="iq-menu-title"><i class="ri-separator"></i><span>Main</span></li>
                             <li class='active'>
                                <a href="javascript:void(0);" class="iq-waves-effect"><i class="las la-user-tie"></i><span>User</span><i class="ri-arrow-right-s-line iq-arrow-right"></i></a>
                                <ul class="iq-submenu">
                                    <li><a href="./profile"><span>User Profile</span></a></li>
                                    <li><a href="./profile_edit"><span>User Edit</span></a></li>
                                    <li><a href="./add_user"><span>User Add</span></a></li>
                                    <li><a href="./user_list"><span>User List</span></a></li>
                                </ul>
                             </li>
                             <li>
                                <a href="javascript:void(0);" class="iq-waves-effect"><i class="las la-user-tie"></i><span>Query</span><i class="ri-arrow-right-s-line iq-arrow-right"></i></a>
                                <ul class="iq-submenu">
                                    <li><a href="./query"><span>Bomb Company Query</span></a></li>
                                    <li><a href="./recognition"><span>Bomb Comapny Recognition</span></a></li>
                                </ul>
                             </li>
                       </nav>
                       <div class="p-3"></div>
                    </div>
                </div>
                  <!-- TOP Nav Bar -->
                  <div class="iq-top-navbar">
                        <div class="iq-navbar-custom">
                           <div class="iq-sidebar-logo">
                           <div class="top-logo">
                              <a href="index.html" class="logo">
                              <img src="./assets/images/logo.gif" class="img-fluid" alt="">
                              <span>Metorik</span>
                              </a>
                           </div>
                        </div>
                           <div class="navbar-breadcrumb">
                              <h5 class="mb-0">User</h5>
                              <nav aria-label="breadcrumb">
                                 <ol class="breadcrumb">
                                    <li class="breadcrumb-item"><a href="">Home</a></li>
                                    <li class="breadcrumb-item active" aria-current="page">User</li>
                                 </ol>
                              </nav>
                           </div>
                            <nav class="navbar navbar-expand-lg navbar-light p-0">
                              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                              <i class="ri-menu-3-line"></i>
                              </button>
                              <div class="iq-menu-bt align-self-center">
                                 <div class="wrapper-menu">
                                    <div class="line-menu half start"></div>
                                    <div class="line-menu"></div>
                                    <div class="line-menu half end"></div>
                                 </div>
                              </div>
                              <div class="collapse navbar-collapse" id="navbarSupportedContent">
                                 <ul class="navbar-nav ml-auto navbar-list">
                                    <li class="nav-item">
                                       <a class="search-toggle iq-waves-effect" href="#"><i class="ri-search-line"></i></a>
                                       <form action="#" class="search-box">
                                          <input type="text" class="text search-input" placeholder="Type here to search..." />
                                       </form>
                                    </li>
                                    <li class="nav-item dropdown">
                                       <a href="#" class="search-toggle iq-waves-effect">
                                          <i class="ri-mail-line"></i>
                                          <span class="badge badge-pill badge-dark badge-up count-mail">5</span>
                                       </a>
                                       <div class="iq-sub-dropdown">
                                          <div class="iq-card shadow-none m-0">
                                             <div class="iq-card-body p-0 ">
                                                <div class="bg-primary p-3">
                                                   <h5 class="mb-0 text-white">All Messages<small class="badge  badge-light float-right pt-1">5</small></h5>
                                                </div>
                                                <a href="#" class="iq-sub-card" >
                                                   <div class="media align-items-center">
                                                      <div class="">
                                                         <img class="avatar-40 rounded" src="./assets/images/user/01.jpg" alt="">
                                                      </div>
                                                      <div class="media-body ml-3">
                                                         <h6 class="mb-0 ">Nik Emma Watson</h6>
                                                         <small class="float-left font-size-12">13 Jun</small>
                                                      </div>
                                                   </div>
                                                </a>
                                                <a href="#" class="iq-sub-card" >
                                                   <div class="media align-items-center">
                                                      <div class="">
                                                         <img class="avatar-40 rounded" src="./assets/images/user/02.jpg" alt="">
                                                      </div>
                                                      <div class="media-body ml-3">
                                                         <h6 class="mb-0 ">Lorem Ipsum Watson</h6>
                                                         <small class="float-left font-size-12">20 Apr</small>
                                                      </div>
                                                   </div>
                                                </a>
                                                <a href="#" class="iq-sub-card" >
                                                   <div class="media align-items-center">
                                                      <div class="">
                                                         <img class="avatar-40 rounded" src="./assets/images/user/03.jpg" alt="">
                                                      </div>
                                                      <div class="media-body ml-3">
                                                         <h6 class="mb-0 ">Why do we use it?</h6>
                                                         <small class="float-left font-size-12">30 Jun</small>
                                                      </div>
                                                   </div>
                                                </a>
                                                <a href="#" class="iq-sub-card" >
                                                   <div class="media align-items-center">
                                                      <div class="">
                                                         <img class="avatar-40 rounded" src="./assets/images/user/04.jpg" alt="">
                                                      </div>
                                                      <div class="media-body ml-3">
                                                         <h6 class="mb-0 ">Variations Passages</h6>
                                                         <small class="float-left font-size-12">12 Sep</small>
                                                      </div>
                                                   </div>
                                                </a>
                                                <a href="#" class="iq-sub-card" >
                                                   <div class="media align-items-center">
                                                      <div class="">
                                                         <img class="avatar-40 rounded" src="./assets/images/user/05.jpg" alt="">
                                                      </div>
                                                      <div class="media-body ml-3">
                                                         <h6 class="mb-0 ">Lorem Ipsum generators</h6>
                                                         <small class="float-left font-size-12">5 Dec</small>
                                                      </div>
                                                   </div>
                                                </a>
                                             </div>
                                          </div>
                                       </div>
                                    </li>
                                    <li class="nav-item">
                                       <a href="#" class="iq-waves-effect"><i class="ri-shopping-cart-2-line"></i></a>
                                    </li>
                                    <li class="nav-item">
                                       <a href="#" class="search-toggle iq-waves-effect">
                                          <i class="ri-notification-2-line"></i>
                                          <span class="bg-danger dots"></span>
                                       </a>
                                       <div class="iq-sub-dropdown">
                                          <div class="iq-card shadow-none m-0">
                                             <div class="iq-card-body p-0 ">
                                                <div class="bg-danger p-3">
                                                   <h5 class="mb-0 text-white">All Notifications<small class="badge  badge-light float-right pt-1">4</small></h5>
                                                </div>
                                                <a href="#" class="iq-sub-card" >
                                                   <div class="media align-items-center">
                                                      <div class="media-body ml-3">
                                                         <h6 class="mb-0 ">New Order Recieved</h6>
                                                         <small class="float-right font-size-12">23 hrs ago</small>
                                                         <p class="mb-0">Lorem is simply</p>
                                                      </div>
                                                   </div>
                                                </a>
                                                <a href="#" class="iq-sub-card" >
                                                   <div class="media align-items-center">
                                                      <div class="">
                                                         <img class="avatar-40 rounded" src="./assets/images/user/01.jpg" alt="">
                                                      </div>
                                                      <div class="media-body ml-3">
                                                         <h6 class="mb-0 ">Emma Watson Nik</h6>
                                                         <small class="float-right font-size-12">Just Now</small>
                                                         <p class="mb-0">95 MB</p>
                                                      </div>
                                                   </div>
                                                </a>
                                                <a href="#" class="iq-sub-card" >
                                                   <div class="media align-items-center">
                                                      <div class="">
                                                         <img class="avatar-40 rounded" src="./assets/images/user/02.jpg" alt="">
                                                      </div>
                                                      <div class="media-body ml-3">
                                                         <h6 class="mb-0 ">New customer is join</h6>
                                                         <small class="float-right font-size-12">5 days ago</small>
                                                         <p class="mb-0">Jond Nik</p>
                                                      </div>
                                                   </div>
                                                </a>
                                                <a href="#" class="iq-sub-card" >
                                                   <div class="media align-items-center">
                                                      <div class="">
                                                         <img class="avatar-40" src="./assets/images/small/jpg.svg" alt="">
                                                      </div>
                                                      <div class="media-body ml-3">
                                                         <h6 class="mb-0 ">Updates Available</h6>
                                                         <small class="float-right font-size-12">Just Now</small>
                                                         <p class="mb-0">120 MB</p>
                                                      </div>
                                                   </div>
                                                </a>
                                             </div>
                                          </div>
                                       </div>
                                    </li>
                                    <li class="nav-item iq-full-screen"><a href="#" class="iq-waves-effect" id="btnFullscreen"><i class="ri-fullscreen-line"></i></a></li>
                                 </ul>
                              </div>
                              <ul class="navbar-list">
                                 <li>
                                    <a href="#" class="search-toggle iq-waves-effect bg-primary text-white"><img src="./assets/images/user/1.jpg" class="img-fluid rounded" alt="user"></a>
                                    <div class="iq-sub-dropdown iq-user-dropdown">
                                       <div class="iq-card shadow-none m-0">
                                          <div class="iq-card-body p-0 ">
                                             <div class="bg-primary p-3">
                                                <h5 class="mb-0 text-white line-height">Hello Nik jone</h5>
                                                <span class="text-white font-size-12">Available</span>
                                             </div>
                                             <a href="./profile" class="iq-sub-card iq-bg-primary-hover">
                                                <div class="media align-items-center">
                                                   <div class="rounded iq-card-icon iq-bg-primary">
                                                      <i class="ri-file-user-line"></i>
                                                   </div>
                                                   <div class="media-body ml-3">
                                                      <h6 class="mb-0 ">My Profile</h6>
                                                      <p class="mb-0 font-size-12">View personal profile details.</p>
                                                   </div>
                                                </div>
                                             </a>
                                             <a href="./profile_edit" class="iq-sub-card iq-bg-primary-success-hover">
                                                <div class="media align-items-center">
                                                   <div class="rounded iq-card-icon iq-bg-success">
                                                      <i class="ri-profile-line"></i>
                                                   </div>
                                                   <div class="media-body ml-3">
                                                      <h6 class="mb-0 ">Edit Profile</h6>
                                                      <p class="mb-0 font-size-12">Modify your personal details.</p>
                                                   </div>
                                                </div>
                                             </a>
                                             <a href="./account_setting" class="iq-sub-card iq-bg-primary-danger-hover">
                                                <div class="media align-items-center">
                                                   <div class="rounded iq-card-icon iq-bg-danger">
                                                      <i class="ri-account-box-line"></i>
                                                   </div>
                                                   <div class="media-body ml-3">
                                                      <h6 class="mb-0 ">Account settings</h6>
                                                      <p class="mb-0 font-size-12">Manage your account parameters.</p>
                                                   </div>
                                                </div>
                                             </a>
                                             <a href="./privacy_setting.html" class="iq-sub-card iq-bg-primary-secondary-hover">
                                                <div class="media align-items-center">
                                                   <div class="rounded iq-card-icon iq-bg-secondary">
                                                      <i class="ri-lock-line"></i>
                                                   </div>
                                                   <div class="media-body ml-3">
                                                      <h6 class="mb-0 ">Privacy Settings</h6>
                                                      <p class="mb-0 font-size-12">Control your privacy parameters.</p>
                                                   </div>
                                                </div>
                                             </a>
                                             <div class="d-inline-block w-100 text-center p-3">
                                                <a class="iq-bg-danger iq-sign-btn" href="./sign_in" role="button">Sign out<i class="ri-login-box-line ml-2"></i></a>
                                             </div>
                                          </div>
                                       </div>
                                    </div>
                                 </li>
                              </ul>
                           </nav>
                        </div>
                     </div>
                  <!-- TOP Nav Bar END -->
            </div>
            {%app_entry%}
            <!-- Footer -->
            <footer class='bg-white iq-footer'>
                {%config%}
                {%scripts%}
                <div class="container-fluid">
                    <div class="row">
                        <div class="col-lg-6">
                            <ul class="list-inline mb-0">
                                <li class="list-inline-item"><a href="#">Privacy Policy</a></li>
                                <li class="list-inline-item"><a href="#">Terms of Use</a></li>
                            </ul>
                        </div>
                        <div class="col-lg-6 text-right">
                            Copyright 2020 <a href="#">Metorik</a> All Rights Reserved.
                        </div>
                    </div>
                </div>
                {%renderer%}
            </footer>
            <!-- Footer END -->
        </body>
    </html>
'''
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# Update page
# # # # # # # # #
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/bomb_company/sign_in':
        return sign_in.layout
    elif pathname == '/bomb_company/sign_up':
        return sign_up.layout
    elif pathname == '/bomb_company/profile':
        return add_user.layout
    elif pathname == '/bomb_company/profile_edit':
        return add_user.layout
    elif pathname == '/bomb_company/query':
        return query.layout
    elif pathname == '/bomb_company/recognition':
        return recognition.layout
    elif pathname == '/bomb_company/add_user':
        return add_user.layout

    else:
        return None


if __name__ == '__main__':
    app.run_server(debug=True)
