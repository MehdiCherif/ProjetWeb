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
      list_cours = Cours.objects.all().filter(enseignant__user=request.user, date__lte=datetime.now()).exclude(justifie=True)
      return render(request, 'enseignant.html',{"titre":"PolyAbs - Espace Enseignant", 'list_cours':list_cours})
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
  return render(request, 'enseignant_cours.html',{"titre":"PolyAbs - Gestion Absences", 'cours':cours})

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
		coursId = request.POST.get('cours', 'non')
		etuId = request.POST.get('etudiant'+str(i), 'none')
		cours = Cours.objects.get(id=coursId)
		cours.justifie = True
		cours.save()
		while (etuId != 'none'):
			print etuId
			etudiant = Etudiant.objects.get(id=etuId)
			a = Absence(cours=cours, etudiant=etudiant)
			a.save()
			print 'saved'
			i = i+1
			etuId = request.POST.get('etudiant'+str(i), 'none')
			
	return accueil(request) 
  
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
			justif = Justificatif.objects.all().filter(absence = abs)
			if (len(justif) > 0):
				if groupe == "Etudiant":
					page += "<td><span class='glyphicon glyphicon-ok-sign' id='popabs"+str(abs.id)+"'></span></td>"
					page += "<script>$('#popabs"+str(abs.id)+"').popover({trigger:'hover',content:'"+justif[0].description+"',placement:'auto'});</script>"
				elif groupe == "Secretaire":
					page += "<td><span class='glyphicon glyphicon-ok-sign'></span></td>"
			else:
				if groupe == "Etudiant":
					page += "<td><span class='glyphicon glyphicon-remove-sign'></span></td>"
				elif groupe == "Secretaire":
					page += "<td><a onclick='openJustif("+str(abs.id)+")'><button type='button' class='btn btn-block' id='openJustif'><span class='glyphicon glyphicon-pencil'></span></button></a></td>"
	page += "<script>$('.btn').popover();</script>"
	return page

def justification(request):
	if request.POST and request.user.groups.all()[0].name == "Secretaire":
		idAbs = request.POST.get('idAbs', 'none')
		abs = Absence.objects.get(pk=idAbs)
		secr = Secretaire.objects.all().filter(user__username = request.user.username)[0]
		descr = request.POST.get('justif', 'none')
		justi = Justificatif(absence = abs, secretaire = secr, description = descr)
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
