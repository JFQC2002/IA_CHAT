from django.contrib import admin
from django.urls import path
from chat.controllers import chat_controller
from chat import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('api/chat/send/', chat_controller.send_message, name='send_message'),
    path('api/chat/history/<str:conversation_id>/', chat_controller.get_history, name='get_history'),
]