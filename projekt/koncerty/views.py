from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.forms import Form
from django.contrib.auth.models import User

from .models import Concert, Attending, Review, Transfer
from .forms import ConcertForm

def zoznam(request):
	concert_list = Concert.objects.all()
	return render(request, "koncerty/zoznam.html", {'concert_list': concert_list})

def detail(request, concert_id):
	concert = get_object_or_404(Concert, pk=concert_id)
	attendees = Attending.objects.filter(concert=concert_id).values_list("user__username", flat=True).order_by("user__username")
	reviews = list(Review.objects.filter(concert=concert_id))
	transfers = list(Transfer.objects.filter(concert=concert_id))
	context = {'concert': concert, 'attendees': attendees, 'reviews': reviews, 'transfers': transfers}

	if request.method == "POST":

		if request.is_ajax():
			if "prihlasenie" in request.POST:
				attending_check = Attending.objects.filter(concert=concert_id, user=request.POST["user_id"]).first()

				if attending_check == None:
					obj = Attending()
					obj.concert = concert
					obj.user = get_object_or_404(User, pk=request.POST["user_id"])
					obj.save()

				return JsonResponse({})

			if "odhlasenie" in request.POST:
				Attending.objects.filter(concert=concert_id, user=request.POST["user_id"]).delete()
				return JsonResponse({})


		if "recenzia" in request.POST:		
			obj = Review()
			obj.text = request.POST["text_recenzie"]
			obj.concert = concert
			obj.user = get_object_or_404(User, pk=request.POST["user_id"])
			obj.save()
			reviews = list(Review.objects.filter(concert=concert_id))
			return render(request, "koncerty/detail.html", context)

		if "odvoz" in request.POST:
			obj = Transfer()
			obj.concert = concert
			obj.driver = get_object_or_404(User, pk=request.POST["driver"])
			obj.seats_provided = request.POST["seats_provided"]
			obj.seats_available = request.POST["seats_provided"]
			obj.save()
			transfers = list(Transfer.objects.filter(concert=concert_id))
			return render(request, "koncerty/detail.html", context)

		if "odvoz_prihlasenie" in request.POST:
			transfer = get_object_or_404(Transfer, pk=request.POST["transfer_id"])
			passenger = get_object_or_404(User, pk=request.POST["passenger"])
			transfer.passengers.add(passenger)
			transfer.seats_available = transfer.seats_available - 1
			transfer.save()
			transfers = list(Transfer.objects.filter(concert=concert_id))
			return render(request, "koncerty/detail.html", context)

		if "odvoz_odhlasenie" in request.POST:
			transfer = get_object_or_404(Transfer, pk=request.POST["transfer_id"])
			passenger = get_object_or_404(User, pk=request.POST["passenger"])
			transfer.passengers.remove(passenger)
			transfer.seats_available = transfer.seats_available + 1
			transfer.save()
			transfers = list(Transfer.objects.filter(concert=concert_id))
			return render(request, "koncerty/detail.html", context)
	
	return render(request, "koncerty/detail.html", context)

def pridanie_koncertu(request):
	if request.method == "POST":
		form = ConcertForm(request.POST)
		if form.is_valid():
			obj = Concert()
			obj.headliner = form.cleaned_data.get("headliner")
			obj.support_bands = form.cleaned_data.get("support_bands")
			obj.city = form.cleaned_data.get("city")
			obj.venue = form.cleaned_data.get("venue")
			obj.date = form.cleaned_data.get("date")
			obj.time = form.cleaned_data.get("time")
			obj.save()
			return HttpResponseRedirect("/koncerty/")
	else:
		form = ConcertForm()

	return render(request, "koncerty/pridanie_koncertu.html", {'form': form})