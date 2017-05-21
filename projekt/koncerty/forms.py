from django import forms
from .models import Concert
from django.utils.translation import ugettext_lazy as _
import datetime

def years():
	first_year = datetime.datetime.now().year - 5
	return list(range(first_year, first_year + 20))

class ConcertForm(forms.ModelForm):
	date = forms.DateField(label="Dátum", widget=forms.SelectDateWidget(years=years()), initial=datetime.date.today)
	support_bands = forms.CharField(label="Predkapely", widget=forms.Textarea(), required=False)

	class Meta:
		model = Concert
		fields = ['headliner', 'support_bands', 'city', 'venue', 'date', 'time']
		labels = {
			'headliner': _("Headliner"),
			'city': _("Mesto"),
			'venue': _("Klub/aréna"),
			'time': _("Čas"),
		}
		help_texts = {
			'time': "Zadajte čas v tvare HH:MM",
		}
