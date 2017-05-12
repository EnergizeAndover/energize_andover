from django.conf.urls import url
from . import views

app_name = 'energize_andover'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^Graph', views.grapher, name='graph'),
    url(r'^electric', views.electrical_mapping, name='electric'),
    url(r'^School(?P<school_id>[0-9]+)', views.school, name='school'),
    url(r'^Room(?P<room_id>[0-9]+)', views.room, name='room'),
    url(r'^Circuit(?P<circuit_id>[0-9]+)', views.circuit, name='circuit'),
    url(r'^Panel(?P<panel_id>[0-9]+)', views.panel, name='panel'),
    url(r'^Closet(?P<closet_id>[0-9]+)', views.closet, name='closet'),
    url(r'^MapAdder', views.adder, name='adder'),
    url(r'^Populate', views.populate, name='populator'),
    url(r'^Search', views.search, name='search'),
    url(r'^Dictionary', views.dictionary, name = 'dictionary'),
    url(r'^Device(?P<device_id>[0-9]+)', views.device, name = "device")
]
