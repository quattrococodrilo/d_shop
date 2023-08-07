from django.urls import path
from .views import home

app_name = 'core'

urlpatterns = [
    path(route='', view=home, name='home'),
]
