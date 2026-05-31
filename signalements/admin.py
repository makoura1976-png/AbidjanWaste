from django.contrib import admin
from .models import Commune, Poubelle, Signalement

@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code']

@admin.register(Poubelle)
class PoubelleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'etat', 'commune', 'date_mise_a_jour']
    list_filter = ['etat', 'commune']

@admin.register(Signalement)
class SignalementAdmin(admin.ModelAdmin):
    list_display = ['type_signalement', 'statut', 'commune', 'date_creation']
    list_filter = ['statut', 'type_signalement', 'commune']