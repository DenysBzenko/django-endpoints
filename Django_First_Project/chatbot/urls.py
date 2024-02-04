from django.urls import path
from .views import home, message_list, message_detail, message_create, message_delete
from django.http import JsonResponse

urlpatterns = [
    path('', home, name='home'),
    path('messages/', message_list, name='message_list'),
    path('messages/<int:id>/', message_detail, name='message_detail'),
    path('messages/create/', message_create, name='message_create'),
    path('messages/delete/<int:id>/', message_delete, name='message_delete'),
]

def handler404(request, exception):
    return JsonResponse({'error': 'The requested endpoint was not found.'}, status=404)
