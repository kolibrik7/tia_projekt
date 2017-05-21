from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.forms import Form
from django.contrib.auth.models import User

from .models import Concert, Attending, Review, Transfer
from .forms import ConcertForm

def zoznam(request):
	concert_list_future = Concert.objects.filter(concert_type=False)
	concert_list_past = Concert.objects.filter(concert_type=True)
	return render(request, "koncerty/zoznam.html", {'concert_list_future': concert_list_future, 'concert_list_past': concert_list_past})

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

			if "odvoz_prihlasenie" in request.POST:
				transfer = get_object_or_404(Transfer, pk=request.POST["transfer_id"])
				passenger = get_object_or_404(User, pk=request.POST["passenger"])
				transfer.passengers.add(passenger)
				transfer.seats_available = transfer.seats_available - 1
				transfer.save()
				return JsonResponse({})

			if "odvoz_odhlasenie" in request.POST:
				transfer = get_object_or_404(Transfer, pk=request.POST["transfer_id"])
				passenger = get_object_or_404(User, pk=request.POST["passenger"])
				transfer.passengers.remove(passenger)
				transfer.seats_available = transfer.seats_available + 1
				transfer.save()
				return JsonResponse({})


		if "recenzia" in request.POST:		
			obj = Review()
			obj.text = request.POST["text_recenzie"]
			obj.concert = concert
			obj.user = get_object_or_404(User, pk=request.POST["user_id"])
			obj.save()
			reviews = list(Review.objects.filter(concert=concert_id))
			context = {'concert': concert, 'attendees': attendees, 'reviews': reviews, 'transfers': transfers}
			return render(request, "koncerty/detail.html", context)

		if "odvoz" in request.POST:
			obj = Transfer()
			obj.concert = concert
			obj.driver = get_object_or_404(User, pk=request.POST["driver"])
			obj.seats_provided = request.POST["seats_provided"]
			obj.seats_available = request.POST["seats_provided"]
			obj.save()
			transfers = list(Transfer.objects.filter(concert=concert_id))
			context = {'concert': concert, 'attendees': attendees, 'reviews': reviews, 'transfers': transfers}
			return render(request, "koncerty/detail.html", context)

		if "odvoz_zrusenie" in request.POST:
			Transfer.objects.filter(concert=concert_id, pk=request.POST["transfer_id"]).delete()
			transfers = list(Transfer.objects.filter(concert=concert_id))
			context = {'concert': concert, 'attendees': attendees, 'reviews': reviews, 'transfers': transfers}
			return render(request, "koncerty/detail.html", context)

	return render(request, "koncerty/detail.html", context)

def pridanie_koncertu(request):
	if request.method == "POST":
		form = ConcertForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/koncerty/")
	else:
		form = ConcertForm()

	return render(request, "koncerty/pridanie_koncertu.html", {'form': form})

def editovanie_koncertu(request, concert_id):
	concert = get_object_or_404(Concert, id=concert_id)
	form = ConcertForm(request.POST or None, instance=concert)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/koncerty/")

	return render(request, "koncerty/editovanie_koncertu.html", {'form': form})

def zmazanie_koncertu(request, concert_id):
	Concert.objects.filter(pk=concert_id).delete()
	return HttpResponseRedirect("/koncerty/")