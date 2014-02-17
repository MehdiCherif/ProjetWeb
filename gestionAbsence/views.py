#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from gestionAbsence.models import *
from django.db.models import Q
from datetime import datetime
from django.utils import formats

# Create your views here.

def accueil(request):
  if request.user.is_authenticated():
    groupe = request.user.groups.all()
    if len(groupe) and groupe[0]:
      groupe = groupe[0].name
    else:
      groupe = 'undefined'
      
    if groupe == 'Enseignant':
      list_cours = Cours.objects.all()
      return render(request, 'enseignant.html',{"titre":"Accueil de PolyAbs", 'list_cours':list_cours})
    elif groupe == 'Etudiant':
      return render(request, 'etudiant.html',{"titre":"Accueil de PolyAbs"})
    elif groupe == 'Secretaire':
      return render(request, 'secretaire.html',{"titre":"Accueil de PolyAbs"})
    else:
      return render(request, 'base.html',{"titre":"Accueil de PolyAbs"})
  else :
    return render(request, 'base.html',{"titre":"Accueil de PolyAbs"})

def cours(request, cours_id):
  cours = Cours.objects.get(pk=cours_id)
  return render(request, 'enseignant_cours.html',{"titre":"Accueil de PolyAbs", 'cours':cours})

def searchEtu(request, nom):
  etuList = Etudiant.objects.all().filter(
    Q(user__last_name__contains=nom) | Q(user__first_name__contains=nom)
  )
  if len(etuList) > 0 :
    page = '<div class="dropdown open"><ul class="dropdown-menu">' 
    for etu in etuList:
      page = page + '<li><a href="#" onclick="addEtu(\''+etu.user.last_name+'\',\''+etu.user.first_name+'\',\''+str(etu.user.id)+'\')">' + etu.user.last_name + " " + etu.user.first_name + "</a></li>" 
    page = page + '</ul></div>'
  else:
    page = ''
  return HttpResponse(page)
  
def getAbsencesEtu(request, id):
	absences = Absence.objects.all().filter(etudiant__user__username = id)
	page = ""
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
			page += "<td>Justifiee</td>"
		else:
			page += "<td>Non justifee</td>"
	return HttpResponse(page)
  
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

def log_out(request):
	logout(request)
	return HttpResponseRedirect('/')

def getEtu(request):
	firstName = request.POST.get('firstName','none')
	lastName = request.POST.get('lastName','none')
	print firstName
	print lastName
	print "AVANT"
	etuList = Etudiant.objects.all().filter(user__last_name = lastName, user__first_name = firstName)
	print "APRES"
	print etuList.count()
	result = "Aucun etudiant trouve"
	for e in etuList:
		result = e.user.username
	return HttpResponse(result)

