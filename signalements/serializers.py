from rest_framework import serializers
from .models import Commune, Poubelle, Signalement

class CommuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = '__all__'

class PoubelleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poubelle
        fields = '__all__'

class SignalementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signalement
        fields = '__all__'