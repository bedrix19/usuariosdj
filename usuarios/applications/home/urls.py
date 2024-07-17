from django.urls import path

from . import views

app_name = 'home_app'

urlpatterns = [
    path(
        '',
        views.home,
        name='home',
    ),
    path(
        'panel/',
        views.HomePage.as_view(),
        name='home-panel',
    ),
    path(
        'mixin/',
        views.TemplatePruebaMixin.as_view(),
        name='home-mixin',
    ),
]
