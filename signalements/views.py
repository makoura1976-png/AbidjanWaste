from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from .models import Commune, Poubelle, Signalement, ProfilCitoyen
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

def classement_view(request):
    profils = ProfilCitoyen.objects.select_related('user', 'commune').order_by('-points')[:20]
    data = []
    for p in profils:
        data.append({
            'username': p.user.username,
            'points': p.points,
            'badge': p.badge,
            'commune': p.commune.nom if p.commune else None,
        })
    return JsonResponse(data, safe=False)