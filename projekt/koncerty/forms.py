from django import forms
import datetime

def years():
	first_year = datetime.datetime.now().year - 5
	return list(range(first_year, first_year + 20))

class ConcertForm(forms.Form):
	headliner = forms.CharField(label="Headliner", max_length=50)
	support_bands = forms.CharField(label="Predkapely", required=False)
	city = forms.CharField(label="Mesto", max_length=30)
	venue = forms.CharField(label="Klub/aréna", max_length=30)
	date = forms.DateField(label="Dátum", widget=forms.SelectDateWidget(years=years()), initial=datetime.date.today)
	time = forms.TimeField(label="Čas", widget=forms.TimeInput)