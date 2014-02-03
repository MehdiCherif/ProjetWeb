from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.

def accueil(request):
	return render(request, 'base.html',{"title":"Accueil de PolyAbs"});
  
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

