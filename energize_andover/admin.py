from django.contrib import admin
from energize_andover.models import School, Closet, Panel, Room, Circuit, Device, Transformer

admin.site.register(School)
admin.site.register(Closet)
admin.site.register(Panel)
admin.site.register(Room)
admin.site.register(Circuit)
admin.site.register(Device)
admin.site.register(Transformer)