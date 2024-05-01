from django.urls import path

from domain.views import create_statement, get_all_statement, get_all_category

app_name = 'core'

urlpatterns = [
    path('create/', create_statement, name='create_statement'),
    path('statements/', get_all_statement, name='get_all_statement'),
    path('categories/', get_all_category, name='get_all_category')
]