from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

REPONSES = {
    'collecte': {
        'fr': """📅 <b>Jours de collecte à Abidjan :</b><br>
        • Cocody : Lundi, Mercredi, Vendredi<br>
        • Plateau : Tous les jours<br>
        • Yopougon : Mardi, Jeudi, Samedi<br>
        • Abobo : Lundi, Jeudi<br>
        • Adjamé : Mercredi, Samedi<br>
        • Autres communes : Contacter la mairie""",
        'dioula': "Kɔnɔ tile : Lundi, Mercredi, Vendredi — Cocody la.",
        'baoule': "Blé kpli wie : Lundi, Mercredi, Vendredi — Cocody su."
    },
    'tri': {
        'fr': """♻️ <b>Guide de tri des déchets :</b><br>
        🟢 Bac vert : déchets organiques (restes de repas)<br>
        🔵 Bac bleu : plastique, carton, papier<br>
        🔴 Bac rouge : déchets dangereux (piles, médicaments)<br>
        ⚫ Bac noir : déchets non recyclables""",
        'dioula': "Falen cogo : Bac vert = dumuni kɔrɔ. Bac bleu = plastiki.",
        'baoule': "Toto kpli : Bac vert = nnuan a kpli. Bac bleu = plastiki."
    },
    'signalement': {
        'fr': """📋 <b>Pour faire un signalement :</b><br>
        1. Cliquez sur <a href='/signalement/' style='color:#2e7d32'>Formulaire de signalement</a><br>
        2. Choisissez le type de problème<br>
        3. Prenez une photo<br>
        4. Localisez-vous sur la carte<br>
        5. Envoyez — un éboueur sera notifié !""",
        'dioula': "Signalement kɛcogo : /signalement/ page kan.",
        'baoule': "Signalement wie : /signalement/ page su."
    },
    'depot': {
        'fr': """📍 <b>Points de dépôt principaux :</b><br>
        • Marché Adjamé : 7h-18h<br>
        • Marché Cocody : 6h-20h<br>
        • Marché Yopougon : 6h-19h<br>
        • Treichville centre : 24h/24<br>
        Consultez la <a href='/carte/' style='color:#2e7d32'>carte interactive</a> pour plus.""",
        'dioula': "Depot yɔrɔw : Marché Adjamé, Cocody, Yopougon.",
        'baoule': "Depot sue : Marché Adjamé, Cocody, Yopougon."
    },
}

def get_reponse(message, langue):
    msg = message.lower()
    if any(w in msg for w in ['collecte', 'jour', 'ramassage', 'passage', 'lundi', 'mardi']):
        return REPONSES['collecte'].get(langue, REPONSES['collecte']['fr'])
    elif any(w in msg for w in ['tri', 'trier', 'recycl', 'bac', 'poubelle', 'plastique']):
        return REPONSES['tri'].get(langue, REPONSES['tri']['fr'])
    elif any(w in msg for w in ['signal', 'problème', 'pleine', 'dépôt sauvage', 'retard']):
        return REPONSES['signalement'].get(langue, REPONSES['signalement']['fr'])
    elif any(w in msg for w in ['depot', 'dépôt', 'point', 'où', 'endroit']):
        return REPONSES['depot'].get(langue, REPONSES['depot']['fr'])
    else:
        return """🤖 Je peux vous aider avec :<br>
        📅 Les <b>jours de collecte</b> par commune<br>
        ♻️ Le <b>tri des déchets</b><br>
        📍 Les <b>points de dépôt</b><br>
        📋 Faire un <b>signalement</b><br><br>
        Posez-moi une question sur l'un de ces sujets !"""

@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        langue = data.get('langue', 'fr')
        reponse = get_reponse(message, langue)
        return JsonResponse({'reponse': reponse})
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)