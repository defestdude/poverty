from django.urls import path
from . import views

#URL Conf
urlpatterns  = [
    path('', views.route_landing),
    path('user_login', views.user_login, name='login'),
    path('dashboard', views.dashboard, name='office_dashboard'),
    path('office', views.back_office, name='office'),
    path('user_logout', views.user_logout, name='logout'),
    path('shocks_injector', views.shocks_injector, name='shocks_injector'),
    path('data/', views.ItemListView.as_view(), name="data"),
]