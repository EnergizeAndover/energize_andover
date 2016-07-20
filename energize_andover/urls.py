from django.conf.urls import url
from . import views

app_name = 'energize_andover'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^Graph', views.grapher, name='graph'),
    url(r'^electric', views.electrical_mapping, name='electric'),
    url(r'^School', views.school, name='school'),

]
