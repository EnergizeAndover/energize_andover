from django.conf.urls import url
from . import views
from ea_parser import views as ParseViews
from school_adder import views as AdderViews
from login import views as LoginViews
from user_management import views as UMViews
from school_editing import views as SEViews
from table_sorter import views as TableViews
from qr_codes import views as QRViews

app_name = 'gismap'
urlpatterns = [
    url(r'^$', ParseViews.index, name='index'),
    url(r'^electric', views.electrical_mapping, name='electric'),
    url(r'^School(?P<school_id>[0-9]+)', views.school, name='school'),
    url(r'^Room(?P<room_id>[0-9]+)', views.room, name='room'),
    url(r'^Circuit(?P<circuit_id>[0-9]+)', views.circuit, name='circuit'),
    url(r'^Panel(?P<panel_id>[0-9]+)', views.panel, name='panel'),
    url(r'^Closet(?P<closet_id>[0-9]+)', views.closet, name='closet'),
    url(r'^Edit/Panel(?P<panel_id>[0-9]+)', SEViews.panel_editing, name='panel_editing'),
    url(r'^Edit/Room(?P<room_id>[0-9]+)', SEViews.room_editing, name='room_editing'),
    url(r'^Edit/Device(?P<device_id>[0-9]+)', SEViews.device_editing, name='device_editing'),
    url(r'^Edit/Circuit(?P<circuit_id>[0-9]+)', SEViews.circuit_editing, name='circuit_editing'),
    url(r'^Edit/Closet(?P<closet_id>[0-9]+)', SEViews.closet_editing, name='closet_editing'),
    url(r'^MapAdder', AdderViews.adder, name='adder'),
    url(r'^Populate', AdderViews.populate, name='populator'),
    url(r'^Search', views.search, name='search'),
    url(r'^Dictionary', views.dictionary, name = 'dictionary'),
    url(r'^ChangeLog', views.changelog, name = 'changelog'),
    url(r'^Device(?P<device_id>[0-9]+)', views.device, name = "device"),
    url(r'^Login', LoginViews.login, name = "login"),
    url(r'^UserCreation', UMViews.user_creation, name = "usercreation"),
    url(r'^Management', UMViews.user_management, name = "user_management"),
    url(r'^Editing(?P<user_id>[0-9]+)', UMViews.user_editing, name = "user_editing"),
    url(r'^TableSorting(?P<school_id>[0-9]+)(?P<type>[-\w]+)', TableViews.list, name='table_sorting'),
    url(r'^QRCode/Room(?P<qr_id>[0-9]+)', QRViews.qr_rooms_redirect, name='qr_room_redirect'),
    url(r'^QRCode/Panel(?P<qr_id>[0-9]+)', QRViews.qr_panels_redirect, name='qr_panel_redirect'),
    url(r'^QRCode/Closet(?P<qr_id>[0-9]+)', QRViews.qr_closets_redirect, name='qr_closet_redirect'),
]
