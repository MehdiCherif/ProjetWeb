from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from gestionAbsence.models import *
from django.db.models import Q

# Create your views here.

def accueil(request):
  if request.user.is_authenticated():
    groupe = request.user.groups.all()
    if groupe[0]:
      groupe = groupe[0].name
      
    if groupe == 'Enseignant':
      list_cours = Cours.objects.all()
      return render(request, 'enseignant.html',{"titre":"Accueil de PolyAbs", 'list_cours':list_cours})
    elif groupe == 'Etudiant':
      return render(request, 'etudiant.html',{"titre":"Accueil de PolyAbs"})
    elif groupe == 'Secretaire':
      return render(request, 'secretaire.html',{"titre":"Accueil de PolyAbs"})
      
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



