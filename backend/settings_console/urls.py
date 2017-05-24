from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/add_email/$', views.add_generated_email, name='add_generated_email'),
    url(r'^ajax/toggle_email/$', views.toggle_email, name='toggle_email'),
    url(r'^password/$', views.change_password, name='change_password'),
]