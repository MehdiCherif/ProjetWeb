from django.conf.urls import patterns, include, url
from gestionAbsence import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PolyAbs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.accueil),
    url(r'^login/', views.log_in),
    url(r'^logout/', views.log_out),
    url(r'^admin/', include(admin.site.urls)),
<<<<<<< HEAD
	url(r'^searchEtu/(?P<nom>\w+)/(?P<prenom>\w+)', views.searchEtu),
	url(r'^getAbsencesEtu/(?P<username>\w+)', views.getAbsencesEtu),
	url(r'^getEtu/', views.getEtu),
=======
    url(r'^cours/(?P<cours_id>\d+)', views.cours),
	  url(r'^searchEtu/(?P<nom>\w+)', views.searchEtu),
>>>>>>> d8ded672ff05eb9884205fb7b3da4448fc94d9ca
)
