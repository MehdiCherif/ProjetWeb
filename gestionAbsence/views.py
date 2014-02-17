from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from gestionAbsence.models import *

# Create your views here.

def accueil(request):
  if request.user.is_authenticated():
    return render(request, 'base.html',{"titre":"COOOO Accueil de PolyAbs"})
  else :
    return render(request, 'base.html',{"titre":"Accueil de PolyAbs"})

def searchEtu(request, nom, prenom):
  etuList = Etudiants.objects.all().filter(user__last_name = nom, user__first_name = prenom)
  page = '<table>'
  for etu in etuList :
    page = page + '<tr><td><a href="/info/etu/' + etu.user.id + '">' + etu.user.last_name + " " + etu.user.first_name + "</a></td></tr>"
  page = '</table>'
  return HttpResponse(page)
  
def getAbsencesEtu(request, username):
	absences = Absences.objets.all().filter(id = username)
	page = "azerty"
	for abs in absences:
		page += "<tr><td>"+abs.date+"</td><td>"+abs.cours+"</td><td>"+abs.justif+"</td>"
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

