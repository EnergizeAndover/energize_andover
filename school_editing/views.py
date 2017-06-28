from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from energize_andover.models import *
from .forms import *

def panel_editing(request, panel_id):
    panel_obj = get_object_or_404(Panel, pk=panel_id)
    if panel_obj.rooms() is not None:
        Rooms = panel_obj.rooms()
    if panel_obj.circuits() is not None:
        Circuits = panel_obj.circuits()
    if panel_obj.panels() is not None:
        Panels = panel_obj.panels()
    parray = []
    for i in range(0, len(Circuits)):
        parray.append(Circuits[i])
    name = ""
    rarray = []
    transformers = Transformer.objects.all()
    for i in range(0, len(Panels)):
        a_break = False
        panel = Panels[i]
        path = panel.FQN
        for count in reversed(range(6)):
            for j in range(0, len(transformers)):
                if len(transformers[j].Name) == count:
                    if transformers[j].Name in path:
                        path = path.replace(transformers[j].Name, "")
        name = path[0: path.index(panel.Name) - 1]
        for j in range(0, len(parray)):
            if parray[j].FQN == name and parray[j] not in rarray:
                rarray.append(parray[j])
    for i in range(0, len(rarray)):
        parray.remove(rarray[i])
    form = PanelEditForm(initial={'Name': panel_obj.Name,
                                  'Voltage': panel_obj.Voltage,
                                  'Notes': panel_obj.Notes,
                                  #'Closet': panel_obj.Closet,
                                  'Rooms': Rooms})
                                  #'Parent': panel_obj.Panels})
    if request.POST.get("Save"):
        if panel_obj.School is not None:
            school = panel_obj.School

        Main = Panel.objects.filter(Name='MSWB')
        if Main.count() > 0:
            Main = Main[0]

        picture = "energize_andover/" + panel_obj.Name.replace(" ", "") + ".jpg"
        return render(request, 'energize_andover/Panel.html',
                      {'panel': panel_obj,
                       'Rooms': Rooms, 'Circuits': parray,
                       'Subpanels': Panels, 'Main': Main, 'school': school,
                       'picture': picture})
    return HttpResponse(render(request, 'energize_andover/Panel.html',
                  {'panel': panel_obj, 'form': form}))
