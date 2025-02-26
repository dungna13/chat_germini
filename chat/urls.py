from django.urls import path
from .views import chat_with_gemini
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: render(request, "chat/index.html"), name='chat'),
    path('chat/', chat_with_gemini, name='chat_gpt'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)