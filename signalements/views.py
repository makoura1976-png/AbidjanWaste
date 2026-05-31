from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from .models import Commune, Poubelle, Signalement
from .serializers import CommuneSerializer, PoubelleSerializer, SignalementSerializer

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return None

class CommuneViewSet(viewsets.ModelViewSet):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer

class PoubelleViewSet(viewsets.ModelViewSet):
    queryset = Poubelle.objects.all()
    serializer_class = PoubelleSerializer

class SignalementViewSet(viewsets.ModelViewSet):
    queryset = Signalement.objects.all()
    serializer_class = SignalementSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]

def carte_view(request):
    return render(request, 'carte.html')

def signalement_view(request):
    return render(request, 'signalement.html')