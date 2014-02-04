from django.db import models
from django.contrib.auth.models import User


class Enseignant(models.Model):
    user = models.OneToOneField(User)  
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30) 

class Secretaire(models.Model):
    user = models.OneToOneField(User)  
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)

class Departement(models.Model):
    respo = models.OneToOneField(Enseignant)

class Annee(models.Model):
    respo = models.OneToOneField(Enseignant)
    dept = models.ForeignKey(Departement)

class Etudiant(models.Model):
    user = models.OneToOneField(User)  
    annee = models.ForeignKey(Annee)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30) 