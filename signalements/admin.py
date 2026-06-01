from django.contrib import admin
from django.utils.html import format_html
from .models import Commune, Poubelle, Signalement, ProfilCitoyen

@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code']

@admin.register(Poubelle)
class PoubelleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'etat', 'commune', 'date_mise_a_jour']
    list_filter = ['etat', 'commune']

@admin.register(Signalement)
class SignalementAdmin(admin.ModelAdmin):
    list_display = ['type_signalement', 'statut', 'commune', 'date_creation', 'apercu_photo']
    list_filter = ['statut', 'type_signalement', 'commune']
    readonly_fields = ['apercu_photo_detail']

    def apercu_photo(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:6px;">',
                obj.photo.url
            )
        return '—'
    apercu_photo.short_description = 'Photo'

    def apercu_photo_detail(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-width:400px;border-radius:10px;">',
                obj.photo.url
            )
        return 'Aucune photo'
    apercu_photo_detail.short_description = 'Aperçu photo'

@admin.register(ProfilCitoyen)
class ProfilCitoyenAdmin(admin.ModelAdmin):
    list_display = ['user', 'points', 'badge', 'commune']