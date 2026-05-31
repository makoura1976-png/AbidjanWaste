from django.db import models
from django.contrib.auth.models import User

class Commune(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Commune"

class Poubelle(models.Model):
    ETAT_CHOICES = [
        ('vide', 'Vide'),
        ('pleine', 'Pleine'),
        ('endommagee', 'Endommagée'),
    ]
    nom = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='vide')
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} — {self.etat}"

class Signalement(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('pris_en_charge', 'Pris en charge'),
        ('resolu', 'Résolu'),
    ]
    TYPE_CHOICES = [
        ('poubelle_pleine', 'Poubelle pleine'),
        ('depot_sauvage', 'Dépôt sauvage'),
        ('retard_collecte', 'Retard de collecte'),
        ('autre', 'Autre'),
    ]
    citoyen = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    type_signalement = models.CharField(max_length=30, choices=TYPE_CHOICES)
    description = models.TextField()
    photo = models.ImageField(upload_to='signalements/', blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    commune = models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_resolution = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.type_signalement} — {self.statut}"

    class Meta:
        ordering = ['-date_creation']