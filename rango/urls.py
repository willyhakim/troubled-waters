#Rango/urls.py
from django.conf.urls import url
from django.views.generic import TemplateView 
from rango import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^about/$', TemplateView.as_view(template_name = 'rango/about.html')),
	url(r'^add_category/$', views.add_category, name = 'add_category'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
]