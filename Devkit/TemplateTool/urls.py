from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Register', views.Registration, name="register"),
    path('Login', views.login, name="login"),
    path('Dashboard', views.dashboard, name="Dashboard"),
    path('logout', views.logout_view, name="logout"),
    path('webapp', views.webapptool, name="webapptool"),
    path('webapp/<int:project_id>', views.record_nav_bar, name="record_nav_bar"),
    path('webapp/<int:project_id>/footer', views.record_footer, name="record_footer"),
    path('webapp/<int:project_id>/loginform', views.record_loginform, name="record_loginform"),
    path('webapp/<int:project_id>/signupform', views.record_signupform, name="record_signupform"),
    path('webapp/<int:project_id>/otherdetails', views.other_details, name="other_details"),
    #path('download_template', views.download_template, name="download_template"),
    path('download_template/<str:application_name>', views.download_template, name="download_template"),
]