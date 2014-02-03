from django.db import models

class Persone(models.Model):
    id = models.CharField(primary_key=True)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30) 
