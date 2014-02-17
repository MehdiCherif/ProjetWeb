from django.db import models
from django.contrib.auth.models import User


class Enseignant(models.Model):
    user = models.OneToOneField(User)  

class Secretaire(models.Model):
    user = models.OneToOneField(User)  

class Departement(models.Model):
    nom = models.CharField(max_length=20, primary_key=True)
    respo = models.OneToOneField(Enseignant)

class Annee(models.Model):
    nom = models.CharField(max_length=20, primary_key=True)
    respo = models.OneToOneField(Enseignant)
    dept = models.ForeignKey(Departement)

class Etudiant(models.Model):
    user = models.OneToOneField(User)  
    annee = models.ForeignKey(Annee) 
    
class Cours(models.Model):
    nom = models.CharField(max_length=20)
    date = models.DateTimeField()
    enseignant = models.ForeignKey(Enseignant)
    
class Absence(models.Model):
    cours = models.ForeignKey(Cours)
    etudiant = models.ForeignKey(Etudiant)
        
class Justificatif(models.Model):
    absence = models.ForeignKey(Absence)
    secretaire = models.ForeignKey(Secretaire)
    description = models.CharField(max_length=1000)