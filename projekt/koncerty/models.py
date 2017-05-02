from django.db import models
from django.contrib.auth.models import User

class Concert(models.Model):
	concert_type = models.BooleanField(default=False) # False - koncert sa este neuskutocnil, True - koncert sa uskutocnil
	headliner = models.CharField(max_length=50)
	support_bands = models.TextField()
	city = models.CharField(max_length=30)
	venue = models.CharField(max_length=30)
	date = models.DateField()
	time = models.TimeField()

	def __str__(self):
		return self.headliner + ", " + self.support_bands + ", miesto konania: " + self.city + ", " + self.venue + ", dátum a čas: " + str(self.date) + ", " + str(self.time)

class Attending(models.Model):
	concert = models.ForeignKey(Concert)
	user = models.ForeignKey(User)

class Review(models.Model):
	concert = models.ForeignKey(Concert)
	user = models.ForeignKey(User)
	text = models.TextField()

class Transfer(models.Model):
	concert = models.ForeignKey(Concert)
	driver = models.ForeignKey(User)
	seats_provided = models.IntegerField()
	seats_available = models.IntegerField()
	passengers = models.ManyToManyField(User, related_name="passengers")