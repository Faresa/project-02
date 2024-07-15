from django.urls import path
from client.views import HomeView, ClientList, ClientDetailView, create_client, add_client_relationship

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('clients/', ClientList.as_view(), name='client_list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:client_id>/add_relationship/', add_client_relationship, name='add_client_relationship'),
    path('clients/create/', create_client, name='create_client'),
    
    
]
