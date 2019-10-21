from django.urls import path

from . import views

from .views import (
    MyReadingsListView,
    AboutView,
    LoginView,
    LogoutView,
    SingUpView,
)

urlpatterns = [
    path('', views.index, name='index'),
    path('my-readings', MyReadingsListView.as_view(), name='my-readings'),
    path('about', AboutView.as_view(), name='about'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('sing-up', SingUpView.as_view(), name='sing-up'),
]
