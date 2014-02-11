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
	url(r'^searchEtu/(?P<nom>\w+)/(?P<prenom>\w+)', views.searchEtu),
)
