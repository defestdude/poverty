from django.urls import path
from . import views

#URL Conf
urlpatterns  = [
    path('', views.route_landing),
    path('user_login', views.user_login, name='login'),
    path('dashboard', views.dashboard, name='office_dashboard'),
    path('user_logout', views.user_logout, name='logout'),
]