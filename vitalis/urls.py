from django.urls import path

from . import views

from .views import MyReadingsListView


urlpatterns = [
    path('', views.index, name='index'),
    path('my-readings', MyReadingsListView.as_view(), name='my-readings'),
]
