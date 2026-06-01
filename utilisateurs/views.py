from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({
                'success': True,
                'username': user.username,
                'email': user.email
            })
        return JsonResponse({'success': False, 'error': 'Identifiants incorrects'})
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def register_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Ce nom d\'utilisateur existe déjà'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Cet email est déjà utilisé'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        login(request, user)
        return JsonResponse({'success': True, 'username': user.username})
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def logout_api(request):
    logout(request)
    return JsonResponse({'success': True})

def profil_api(request):
    if request.user.is_authenticated:
        try:
            from signalements.models import ProfilCitoyen
            profil = ProfilCitoyen.objects.get(user=request.user)
            points = profil.points
            badge = profil.badge
            rang = ProfilCitoyen.objects.filter(points__gt=points).count() + 1
        except Exception:
            points = 0
            badge = '🌱 Débutant'
            rang = None
        return JsonResponse({
            'authenticated': True,
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'points': points,
            'badge': badge,
            'rang': rang,
        })
    return JsonResponse({'authenticated': False})