from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from signalements.views import CommuneViewSet, PoubelleViewSet, SignalementViewSet, carte_view, signalement_view, classement_view
from chatbot.views import chatbot_api
from utilisateurs.views import login_api, register_api, logout_api, profil_api
from django.shortcuts import render

router = DefaultRouter()
router.register(r'communes', CommuneViewSet)
router.register(r'poubelles', PoubelleViewSet)
router.register(r'signalements', SignalementViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/chatbot/', chatbot_api, name='chatbot-api'),
    path('api/auth/login/', login_api, name='login-api'),
    path('api/auth/register/', register_api, name='register-api'),
    path('api/auth/logout/', logout_api, name='logout-api'),
    path('api/auth/profil/', profil_api, name='profil-api'),
    path('api/classement/', classement_view, name='classement-api'),
    path('carte/', carte_view, name='carte'),
    path('signalement/', signalement_view, name='signalement'),
    path('chatbot/', lambda req: render(req, 'chatbot.html'), name='chatbot-page'),
    path('dashboard/', lambda req: render(req, 'dashboard.html'), name='dashboard'),
    path('login/', lambda req: render(req, 'login.html'), name='login'),
    path('register/', lambda req: render(req, 'register.html'), name='register'),
    path('classement/', lambda req: render(req, 'classement.html'), name='classement'),
    path('', lambda req: render(req, 'index.html'), name='accueil'),
]