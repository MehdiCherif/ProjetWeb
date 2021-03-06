#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied
from gestionAbsence.models import *
from django.db.models import Q
from datetime import datetime
from django.utils import formats

# Create your views here.

def accueil(request):
	if request.user.is_authenticated():
		groupe = request.user.groups.all()
		if len(groupe) > 0:
			groupe = groupe[0].name
		else:
			groupe = 'undefined'

		if groupe == 'Enseignant':
			list_newcours = Cours.objects.all().filter(enseignant__user=request.user, date__lte=datetime.now()).exclude(renseigne=True)
			list_oldcours = Cours.objects.all().filter(enseignant__user=request.user, date__lte=datetime.now()).exclude(renseigne=False)
			list_notif = Notification.objects.all().filter(enseignant__user=request.user).exclude(vu=True)
			return render(request, 'enseignant.html',{"titre":"PolyAbs - Espace Enseignant", 'list_newcours':list_newcours, 'list_oldcours':list_oldcours, 'list_notif':list_notif})
		elif groupe == 'Etudiant':
			return render(request, 'etudiant.html',{"titre":"Accueil de PolyAbs", 'liste_abs': getAbsencesEtu(request, request.user.username) })
		elif groupe == 'Secretaire':
			return render(request, 'secretaire.html',{"titre":"PolyAbs - Espace Secrétaire"})
		else:
			return render(request, 'base.html',{"titre":"Accueil de PolyAbs"})
	else :
		return render(request, 'base.html',{"titre":"Accueil de PolyAbs"})

def cours(request, cours_id):
	cours = Cours.objects.get(pk=cours_id)
	list_absences = Absence.objects.all().filter(cours = cours)
	return render(request, 'enseignant_cours.html',{"titre":"PolyAbs - Gestion Absences", 'cours':cours, 'list_absences':list_absences})

def searchEtu(request, nom):
  etuList = Etudiant.objects.all().filter(
    Q(user__last_name__contains=nom) | Q(user__first_name__contains=nom)
  )
  if len(etuList) > 0 :
    page = '<div class="dropdown open"><ul class="dropdown-menu">' 
    for etu in etuList:
      page = page + '<li><a href="#" onclick="addEtu(\''+etu.user.last_name+'\',\''+etu.user.first_name+'\',\''+etu.user.username+'\')">' + etu.user.last_name + " " + etu.user.first_name + "</a></li>" 
    page = page + '</ul></div>'
  else:
    page = ''
  return HttpResponse(page)
	
def genererAbsence(request):
	i = 1
	if request.POST:
		coursId = request.POST.get('cours', 'none')
		cours = Cours.objects.get(id=coursId)
		absences = Absence.objects.all().filter(cours = cours)
		for a in absences:
			a.delete()
		etuUsername = request.POST.get('etudiant'+str(i), 'none')
		cours.renseigne = True
		cours.save()
		while (etuUsername != 'none'):
			etudiant = Etudiant.objects.get(user__username=etuUsername)
			a = Absence(cours=cours, etudiant=etudiant)
			a.save()
			i = i+1
			nbAbsNonJustifie = 0
			absEtu = Absence.objects.all().filter(etudiant = etudiant)
			for abs in absEtu:
				justif = Justificatif.objects.all().filter(etudiant = etudiant, dateDebut__lte = abs.cours.date, dateFin__gte = abs.cours.date)
				if(len(justif) == 0) :
					nbAbsNonJustifie = nbAbsNonJustifie + 1  
			if nbAbsNonJustifie >= 3:
				notification = Notification(enseignant = etudiant.annee.respo, vu = False)
				notification.save()
				notification.contenu = u"<a href='javascript:clickNotif(\"" +etudiant.user.last_name+ u"\",\"" +etudiant.user.first_name+ u"\",\"" +etudiant.user.username+ u"\",\""+ str(notification.id)+ "\")'>" +etudiant.user.first_name+ " " + etudiant.user.last_name+ u"</a> a été absent plus de 3 fois"
				notification.save()
			if nbAbsNonJustifie >= 5:
				notification = Notification(enseignant = etudiant.annee.respo, vu = False)
				notification.save()
				notification.contenu = u"<a href='javascript:clickNotif(\""+etudiant.user.last_name+u"\",\""+etudiant.user.first_name+u"\",\""+etudiant.user.username+u"\",\""+str(notification.id)+u"\")'>"+etudiant.user.first_name + " "+etudiant.user.last_name+ u"</a> a été absent plus de 5 fois"
				notification.save()
			etuUsername = request.POST.get('etudiant'+str(i), 'none')
	return HttpResponseRedirect('/') 
  
def getJustif(request, username):
	if (request.user.groups.all()[0].name == 'Secretaire'):
		justifs = ""
		listJustifs = Justificatif.objects.all().filter(etudiant__user__username = username)
		print len(listJustifs)
		if len(listJustifs) > 0:
			for justif in listJustifs:
				justifs += "<tr><td>"+formats.date_format(justif.dateDebut, "DATETIME_FORMAT")
				justifs += "</td><td>"+formats.date_format(justif.dateFin, "DATETIME_FORMAT")+"</td><td>"
				justifs += justif.secretaire.user.last_name+"</td><td>"+justif.justification+"</td></tr>"	
		else:
			justifs = "Cet étudiant n'a pas de justificatifs enregistré"
		return HttpResponse(justifs)
	else:
		raise PermissionDenied
  
def getAbsencesEtu(request, username):
	groupe = request.user.groups.all()
	page = ""
	if len(groupe) > 0:
		groupe = groupe[0].name
		absences = Absence.objects.all().filter(etudiant__user__username = username)
		if (len(absences) > 0):
			page += u"<tr><td><b>Date</b></td><td><b>Matière</b></td><td><b>Enseignant</b></td><td><b>Justification</b></td></tr>"
		else:
			page += u"<p class='lead'>Vous n'avez aucune absence à ce jour.</p>"
		for abs in absences:
			dateAbs = abs.cours.date
			dateAbs2 = formats.date_format(dateAbs, "DATETIME_FORMAT")
			page += "<tr><td>"+dateAbs2+"</td><td>"+abs.cours.nom+"</td><td>"+abs.cours.enseignant.user.last_name+"</td>"
			justif = Justificatif.objects.all().filter(etudiant__user__username = username, dateDebut__lte=abs.cours.date, dateFin__gte=abs.cours.date)
			if (len(justif) > 0):
				if groupe == "Etudiant" or groupe == "Enseignant":
					page += "<td><span class='glyphicon glyphicon-ok-sign' id='popabs"+str(abs.id)+"'></span></td>"
					page += "<script>$('#popabs"+str(abs.id)+"').popover({trigger:'hover',content:'"+justif[0].justification+"',placement:'auto'});</script>"
				elif groupe == "Secretaire":
					page += "<td><span class='glyphicon glyphicon-ok-sign'></span></td>"
			else:
				if groupe == "Etudiant" or groupe == "Enseignant":
					page += "<td><span class='glyphicon glyphicon-remove-sign'></span></td>"
				elif groupe == "Secretaire":
					page += "<td><a onclick='openJustif("+str(abs.id)+")'><button type='button' class='btn btn-block' id='openJustif'><span class='glyphicon glyphicon-pencil'></span></button></a></td>"
	page += "<script>$('.btn').popover();</script>"
	
	if groupe == "Etudiant":
		return page
	return HttpResponse(page)

def justification(request):
	if request.POST and request.user.groups.all()[0].name == "Secretaire":
		etud = Etudiant.objects.all().filter(user__username = request.POST.get('etudiant', 'none'))[0]
		dateD = request.POST.get('dateDebut', 'none')
		dateF = request.POST.get('dateFin', 'none')
		justif = request.POST.get('justif', 'none')
		secr = Secretaire.objects.all().filter(user__username = request.user.username)[0]
		descr = request.POST.get('justif', 'none')
		justi = Justificatif(etudiant = etud, dateDebut = dateD, dateFin = dateF, secretaire = secr, justification = justif)
		justi.save()
	return HttpResponseRedirect('/')
  
def log_in(request):
	logout(request)
	username = password = ''
	if request.POST:
		username = request.POST.get('username', 'none')
		password = request.POST.get('password', 'none')
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
	raise PermissionDenied 

def log_out(request):
	logout(request)
	return HttpResponseRedirect('/')

def contact(request):
	return render(request, 'contact.html',{"titre":"PolyAbs - Contact"})
	
def aPropos(request):
	return render(request, 'aPropos.html',{"titre":"PolyAbs - A Propos"})

def getEtu(request):
	firstName = request.POST.get('firstName','none')
	lastName = request.POST.get('lastName','none')
	etuList = Etudiant.objects.all().filter(user__last_name = lastName, user__first_name = firstName)
	print etuList.count()
	result = "Aucun etudiant trouve"
	for e in etuList:
		result = e.user.username
	return HttpResponse(result)
	
def viewNotif(request, notifId):
	notif = Notification.objects.get(id = notifId)
	notif.vu = True
	notif.save()
	return ''
