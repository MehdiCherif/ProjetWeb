from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from gestionAbsence.models import *

# Create your views here.

def accueil(request):
  if request.user.is_authenticated():
    groupe = request.user.groups.all()
    if groupe[0]:
      groupe = groupe[0].name
      
    if groupe == 'Enseignant':
      list_absence = Cours.objects.all()
      return render(request, 'enseignant.html',{"titre":"Accueil de PolyAbs", 'list_absence':list_absence})
    elif groupe == 'Etudiant':
      return render(request, 'etudiant.html',{"titre":"Accueil de PolyAbs"})
    elif groupe == 'Secretaire':
      return render(request, 'secretaire.html',{"titre":"Accueil de PolyAbs"})
      
  else :
    return render(request, 'base.html',{"titre":"Accueil de PolyAbs"})

def enseignant_cours(request, cours_id):
  cours = Cours.objects.get(cours_id)
  return render(request, 'enseignant_cours.html',{"titre":"Accueil de PolyAbs", 'cours':cours})

def searchEtu(request, nom, prenom):
  etuList = Etudiants.objects.all().filter(user__last_name = nom, user__first_name = prenom)
  
  page = '<table>'
  
  for etu in etuList :
    page = page + '<tr><td><a href="/info/etu/' + etu.user.id + '">' + etu.user.last_name + " " + etu.user.first_name + "</a></td></tr>"
  
  page = '</table>'
  return HttpResponseRedirect(page)
  
  
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



