from django.conf.urls import url
from . import views
from grapher import views as GraphViews
from ea_parser import views as ParseViews
from school_adder import views as AdderViews
from login import views as LoginViews

app_name = 'gismap'
urlpatterns = [
    url(r'^$', ParseViews.index, name='index'),
    url(r'^Graph', GraphViews.grapher, name='graph'),
    url(r'^electric', views.electrical_mapping, name='electric'),
    url(r'^School(?P<school_id>[0-9]+)', views.school, name='school'),
    url(r'^Room(?P<room_id>[0-9]+)', views.room, name='room'),
    url(r'^Circuit(?P<circuit_id>[0-9]+)', views.circuit, name='circuit'),
    url(r'^Panel(?P<panel_id>[0-9]+)', views.panel, name='panel'),
    url(r'^Closet(?P<closet_id>[0-9]+)', views.closet, name='closet'),
    url(r'^MapAdder', AdderViews.adder, name='adder'),
    url(r'^Populate', AdderViews.populate, name='populator'),
    url(r'^Search', views.search, name='search'),
    url(r'^Dictionary', views.dictionary, name = 'dictionary'),
    url(r'^Device(?P<device_id>[0-9]+)', views.device, name = "device"),
    url(r'^Login', LoginViews.login, name = "login"),
    url(r'^UserCreation', LoginViews.user_creation, name = "usercreation"),
    url(r'^Management', LoginViews.user_management, name = "user_management"),
    url(r'^Editing(?P<user_id>[0-9]+)', LoginViews.user_editing, name = "user_editing")
]
