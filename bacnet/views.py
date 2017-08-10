from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import sched, time
import threading
from .models import *
from threading import Thread
from bacnet.script.NAEInteract1 import main, findNAE
import json
from datetime import datetime


s = sched.scheduler(time.time, time.sleep)
def graphing(request):
    Thread(target=data_pull_schedule()).start()
    Thread(target=data_submit_schedule(request)).start()

def data_pull_schedule():
    while (True):
        s.enter(5, 1, main, ())

def data_submit_schedule(request):
    while(True):
        s.enter(5, 1, return_data(request))

def return_data(request, school_id):
    school = get_object_or_404(School, pk=school_id)
    data_values = Data_Point.objects.filter(School=school)
    date_and_time = ""
    date = datetime.strptime("01-01-01", "%y-%m-%d")
    time = datetime.strptime("00:00", "%H:%M")
    cost = .16
    checked = False
    if request.POST.get("request_data"):
        cost = request.POST.get("cost/kW")
        checked = bool(request.POST.get("checkbox"))
        try:
            date_and_time = request.POST.get("Datetime")
            date = datetime.strptime(date_and_time[2:date_and_time.index("T")], "%y-%m-%d")
            time = datetime.strptime(date_and_time[date_and_time.index("T") + 1:], "%H:%M")
        except:
            date_and_time = ""
            date = datetime.strptime("01-01-01", "%y-%m-%d")
            time = datetime.strptime("00:00", "%H:%M")
    data_dict = {}
    previous_value = {}
    unique_names = []
    for datapoint in Data_Point.objects.all():
        if datapoint.Name not in unique_names:
            unique_names.append(datapoint.Name)
            data_dict[datapoint.Name]=[datapoint.Value]
            if "kWh" in datapoint.Name:
                data_dict[datapoint.Name]=[0]
                previous_value[datapoint.Name]=datapoint.Value
        else:
            if "kWh" in datapoint.Name:
                data_dict[datapoint.Name].append(datapoint.Value-previous_value[datapoint.Name])
                previous_value[datapoint.Name] = datapoint.Value
            else:
                data_dict[datapoint.Name].append(datapoint.Value)


    times = []
    main_kWs=[]
    dhb_kWs = []
    de_kWs = []
    dg_kWs = []
    dl_kWs = []
    amdp_kWs = []
    m1_kWs = []
    for data in data_values:
        data_date = datetime.strptime(data.Time[2:data.Time.index(" ")], "%y-%m-%d")
        index = data.Time.index(" ")
        data_time = datetime.strptime(data.Time[index + 1: index + 6], "%H:%M")
        if data_date > date or (data_date == date and data_time >= time):
            if checked:
                for key in data_dict:
                    if "(kWh)" in key:
                        for i in range(0, len(data_dict[key])):
                            data_dict[key][i] = data_dict[key][i] * float(cost)
                        data_dict[key.replace("kWh", "$")] = data_dict.pop(key)

                if data.Name == "Main (kW)":
                    print (data.Value)
                    print(cost)

                    main_kWs.append(data.Value * float(cost))
                    times.append(data.Time)
                elif data.Name == "DHB (kW)":
                    dhb_kWs.append(data.Value * float(cost))
                elif data.Name == "DE (kW)":
                    de_kWs.append(data.Value * float(cost))
                elif data.Name == "DG (kW)":
                    dg_kWs.append(data.Value * float(cost))
                elif data.Name == "DL (kW)":
                    dl_kWs.append(data.Value * float(cost))
                elif data.Name == "AMDP (kW)":
                    amdp_kWs.append(data.Value * float(cost))
                elif data.Name == "M1 (kW)":
                    m1_kWs.append(data.Value * float(cost))
            else:
                if data.Name == "Main (kW)":
                    main_kWs.append(data.Value)
                    times.append(data.Time)
                elif data.Name == "DHB (kW)":
                    dhb_kWs.append(data.Value)
                elif data.Name == "DE (kW)":
                    de_kWs.append(data.Value)
                elif data.Name == "DG (kW)":
                    dg_kWs.append(data.Value)
                elif data.Name == "DL (kW)":
                    dl_kWs.append(data.Value)
                elif data.Name == "AMDP (kW)":
                    amdp_kWs.append(data.Value)
                elif data.Name == "M1 (kW)":
                    m1_kWs.append(data.Value)
    times = json.dumps(times)
    print (data_dict)
    return render(request, "energize_andover/Graph.html", {'times': times,
                                                           'data': data_dict,
                                                           'main_kWs': main_kWs,
                                                           'dhb_kWs': dhb_kWs,
                                                           'de_kWs': de_kWs,
                                                           'dg_kWs': dg_kWs,
                                                           'dl_kWs': dl_kWs,
                                                           'm1_kWs': m1_kWs,
                                                           'amdp_kWs': amdp_kWs,
                                                           'date': date_and_time,
                                                           'checked': checked,
                                                           'cost': cost,
                                                           'change_title': str(checked).lower(),
                                                           'school': school}
                  )


