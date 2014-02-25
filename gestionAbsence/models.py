from django.db import models
from django.contrib.auth.models import User


class Enseignant(models.Model):
	user = models.OneToOneField(User)  
	def __unicode__(self):
		return u'%s %s' % (self.user.first_name,self.user.last_name)

class Secretaire(models.Model):
	user = models.OneToOneField(User)  
	def __unicode__(self):
		return u'%s %s' % (self.user.first_name,self.user.last_name)

class Departement(models.Model):
	nom = models.CharField(max_length=20, primary_key=True)
	respo = models.OneToOneField(Enseignant)
	def __unicode__(self):
		return u'%s' % (self.nom)

class Annee(models.Model):
	nom = models.CharField(max_length=20, primary_key=True)
	respo = models.OneToOneField(Enseignant)
	dept = models.ForeignKey(Departement)
	def __unicode__(self):
		return u'%s' % (self.nom)

class Etudiant(models.Model):
	user = models.OneToOneField(User)  
	annee = models.ForeignKey(Annee) 
	def __unicode__(self):
		return u'%s %s' % (self.user.first_name,self.user.last_name)
    
class Cours(models.Model):
	nom = models.CharField(max_length=20)
	date = models.DateTimeField()
	enseignant = models.ForeignKey(Enseignant)
	renseigne = models.BooleanField()
	def __unicode__(self):
		return u'%s - %s (%s)' % (self.nom,self.enseignant.user.last_name,self.date)		
    
class Absence(models.Model):
	cours = models.ForeignKey(Cours)
	etudiant = models.ForeignKey(Etudiant)
	def __unicode__(self):
		return u'%s %s' % (self.cours.nom,self.etudiant.user.last_name)

class Notification(models.Model):
	enseignant = models.ForeignKey(Enseignant)
	contenu = models.CharField(max_length=1000)
	def __unicode__(self):
		return u'%s %s' % (self.enseignant.user.last_name,self.contenu)
		
class Justificatif(models.Model):
	etudiant = models.ForeignKey(Etudiant)
	dateDebut = models.DateTimeField()
	dateFin = models.DateTimeField()
	secretaire = models.ForeignKey(Secretaire)
	justification = models.CharField(max_length=1000)
	def __unicode__(self):
		return u'(%s-%s) : %s - %s' % (self.dateDebut, self.dateFin, self.secretaire.user.last_name, self.justification)