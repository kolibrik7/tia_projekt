from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.zoznam, name="zoznam"),
	url(r'^pridanie_koncertu/$', views.pridanie_koncertu, name="pridanie_koncertu"),
	url(r'^(?P<concert_id>[0-9]+)/$', views.detail, name="detail"),
	url(r'^(?P<concert_id>[0-9]+)/edit/$', views.editovanie_koncertu, name="editovanie_koncertu"),
	url(r'^(?P<concert_id>[0-9]+)/delete_JOZKOs5f90u5DNr9sYEj/$', views.zmazanie_koncertu, name="zmazanie_koncertu"),
]