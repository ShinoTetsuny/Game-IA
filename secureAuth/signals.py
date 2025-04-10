# Les signaux sont déjà importés et configurés dans models.py
# Ce fichier est inclus pour garantir que les signaux sont correctement chargés au démarrage de l'application
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# Les signaux sont définis dans models.py, mais ils peuvent être redéfinis ici si nécessaire 