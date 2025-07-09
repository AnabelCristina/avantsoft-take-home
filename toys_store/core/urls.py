from core import update_client, delete_client, list_clients, create_client
from views import up
from django.urls import path

urlpatterns = [
    path('clients/<int:pk>/', update_client, name='update_client'),
    path('clients/<int:pk>/delete/', delete_client, name='delete_client'),
    path('clients/', list_clients, name='list_clients'),
    path('clients/create/', create_client, name='create_client'),
]