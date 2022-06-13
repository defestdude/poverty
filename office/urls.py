from django.urls import path
from rest_framework import routers
from . import views
from django.urls import re_path, include


# router = routers.DefaultRouter()
# router.register(r'office', views.PredictorViewSet)

#URL Conf
urlpatterns  = [
    path('', views.route_landing),
    path('user_login', views.user_login, name='login'),
    path('dashboard', views.dashboard, name='office_dashboard'),
    path('office', views.back_office, name='office'),
    path('train', views.begin_training, name='train'),
    path('user_logout', views.user_logout, name='logout'),
    path('shocks_injector', views.shocks_injector, name='shocks_injector'),
    path('data', views.PredictorViewSet.as_view({'get': 'list'}), name="data"),
]