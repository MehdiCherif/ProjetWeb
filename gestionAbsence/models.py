from django.db import models
from django.contrib.auth.models import User

class Personne(models.Model):
    user = models.OneToOneField(User)  
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30) 
