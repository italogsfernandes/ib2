from django.urls import path

from . import views

from .views import (
    MyReadingsListView,
    AboutView,
    LoginView,
    LogoutView,
    SingUpView,
    GetTMPDataView,
)

urlpatterns = [
    path('', views.index, name='index'),
    path('my-readings', MyReadingsListView.as_view(), name='my-readings'),
    path('about', AboutView.as_view(), name='about'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('sing-up', SingUpView.as_view(), name='sing-up'),
    path('extra', views.sensores_conectados_extra_view, name="extra_view"),
    path('tmp_data', GetTMPDataView.as_view(), name="tmp_data"),
]
