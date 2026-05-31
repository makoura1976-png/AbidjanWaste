from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from signalements.views import CommuneViewSet, PoubelleViewSet, SignalementViewSet, carte_view, signalement_view
from chatbot.views import chatbot_api
from django.shortcuts import render

router = DefaultRouter()
router.register(r'communes', CommuneViewSet)
router.register(r'poubelles', PoubelleViewSet)
router.register(r'signalements', SignalementViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/chatbot/', chatbot_api, name='chatbot-api'),
    path('carte/', carte_view, name='carte'),
    path('signalement/', signalement_view, name='signalement'),
    path('chatbot/', lambda req: render(req, 'chatbot.html'), name='chatbot-page'),
    path('dashboard/', lambda req: render(req, 'dashboard.html'), name='dashboard'),
    path('', lambda req: render(req, 'index.html'), name='accueil'),
]