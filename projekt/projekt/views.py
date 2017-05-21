from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm
#from django.contrib.auth.forms import UserCreationForm

def index(request):
	return render(request, "projekt/index.html")

def registracia(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get("username")
			raw_password = form.cleaned_data.get("password1")
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect("index")
	else:
		form = RegistrationForm()

	return render(request, "registration/registracia.html", {'form': form})