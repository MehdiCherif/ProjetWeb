from django.conf.urls import patterns, include, url
from gestionAbsence import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	url(r'^$', views.accueil),
	url(r'^login/', views.log_in),
	url(r'^logout/', views.log_out),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^cours/(?P<cours_id>\d+)', views.cours),
	url(r'^searchEtu/(?P<nom>\w+)', views.searchEtu),
	url(r'^genererAbsence', views.genererAbsence),
	url(r'^getAbsencesEtu/(?P<username>\w+)', views.getAbsencesEtu),
	url(r'^justification/', views.justification),
	url(r'^contact/', views.contact),
	url(r'^aPropos/', views.aPropos),
	url(r'^getJustif/(?P<username>\w+)', views.getJustif),
)
