from django.contrib import admin
from .models import Concert, Review, Attending

# Register your models here.
admin.site.register(Concert)
admin.site.register(Review)
admin.site.register(Attending)
