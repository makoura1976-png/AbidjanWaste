from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Commune(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Commune"

class ProfilCitoyen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    commune = models.ForeignKey('Commune', on_delete=models.SET_NULL, null=True, blank=True)
    badge = models.CharField(max_length=50, default='Débutant')

    def mettre_a_jour_badge(self):
        if self.points >= 500:
            self.badge = '🏆 Champion'
        elif self.points >= 200:
            self.badge = '⭐ Expert'
        elif self.points >= 100:
            self.badge = '🥈 Actif'
        elif self.points >= 50:
            self.badge = '🥉 Engagé'
        else:
            self.badge = '🌱 Débutant'
        self.save()

    def __str__(self):
        return f"{self.user.username} — {self.points} pts"

@receiver(post_save, sender=User)
def creer_profil(sender, instance, created, **kwargs):
    if created:
        ProfilCitoyen.objects.create(user=instance)

@receiver(post_save, sender=User)
def sauvegarder_profil(sender, instance, **kwargs):
    if hasattr(instance, 'profilcitoyen'):
        instance.profilcitoyen.save()

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
    points_attribues = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type_signalement} — {self.statut}"

    class Meta:
        ordering = ['-date_creation']

    def save(self, *args, **kwargs):
        if self.statut == 'resolu' and not self.points_attribues and self.citoyen:
            super().save(*args, **kwargs)
            try:
                profil = self.citoyen.profilcitoyen
                profil.points += 10
                profil.mettre_a_jour_badge()
            except:
                pass
            self.points_attribues = True
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)