from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.

def accueil(request):
  if request.user.is_authenticated():
    return render(request, 'base.html',{"titre":"COOOO Accueil de PolyAbs"});
  else :
    return render(request, 'base.html',{"titre":"Accueil de PolyAbs"});

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



