from django.urls import path
from .views_simple import (
    HomeView, 
    PersonCreateView, 
    PersonListView,
    api_person_create,
    api_person_list
)

app_name = 'persons'

urlpatterns = [
    # Веб-интерфейс
    path('', HomeView.as_view(), name='home'),
    path('create/', PersonCreateView.as_view(), name='create'),
    path('list/', PersonListView.as_view(), name='list'),
    
    # API
    path('api/persons/', api_person_list, name='api_list'),
    path('api/persons/create/', api_person_create, name='api_create'),
]
