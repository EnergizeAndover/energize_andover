from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from energize_andover.models import *
from login.forms import *
import codecs
from datetime import datetime

def login (request):
    if check_status(request):
        return HttpResponseRedirect("electric")
    if request.method == "GET":
        form = LoginForm(request.GET, request.FILES)
        if form.is_valid():
            print(True)
            if request.GET.get('username') is None or request.GET.get("password") is None:
                return HttpResponse(render(request, 'energize_andover/Login.html', {'form': form,
                                                                                    'message': "Login Failed: Missing Username and/or Password"}))
            user = authenticate(username=request.GET.get('username'), password=request.GET.get('password'))
            if user is not None:
                request.session['logged_in'] = True
                request.session['username'] = request.GET.get('username')
                request.session['password'] = request.GET.get('password')
                schools = School.objects.filter()
                if request.session.get('destination', None) == None:
                    return HttpResponseRedirect('electric')
                dest_string = request.session['destination']
                request.session['destination'] = None
                message = "User " + request.session['username'] + " logged in."
                update_log(message, None, request)
                return HttpResponseRedirect(dest_string)
            else:
                return HttpResponse(render(request, 'energize_andover/Login.html', {'form': form, 'message': "Login Failed: Incorrect Username and/or Password"}))
        return HttpResponse(render(request, 'energize_andover/Login.html', {'form': form}))


def logout (request):
    if (request.GET.get('mybtn')):
        print ("true")
        message = "User " + request.session['username'] + " logged out."
        print (message)
        update_log(message, None, request)
        request.session['logged_in'] = None
        request.session['username'] = None
        request.session['password'] = None
        return HttpResponseRedirect("Login")

def check_status(request):
    if (request.session.get('logged_in', None) == None):
        req = str(request).replace("/energize_andover", "")
        request.session['destination'] = req[req.index ("/") + 1: len(req) - 2]
        return False
    return True

def check_admin(request):
    user = authenticate(username = request.session['username'], password = request.session['password'])
    if Permission.objects.get(codename="can_create_user") in user.user_permissions.all():
        return True
    return False


def check_school_privilege(school, request):
    user = authenticate(username=request.session['username'], password=request.session['password'])
    if user is not None:
        su = SpecialUser.objects.get(User=user)
        if school not in su.Authorized_Schools.all():
            return False
    return True


def check_school_edit_privilege(request):
    user = authenticate(username=request.session['username'], password=request.session['password'])
    if Permission.objects.get(codename="can_edit_schools") in user.user_permissions.all():
        return True
    return False


def update_log (message, school, request):
    f = codecs.open("/var/www/gismap/energize_andover/templates/energize_andover/ChangeLog.html", "r")
    file = str(f.read())
    w = codecs.open("/var/www/gismap/energize_andover/templates/energize_andover/ChangeLog.html", "w")
    break_pt = file.index("</h1>") + 5
    if not school == None:
        w.write(file[0:break_pt] + "\n<p>Time: " + str(datetime.now()) + ", School: " + school.Name + ", User: " + request.session[
            'username'] + ", Description: " + message + "</p>" + file[break_pt:])
    else:
        try:
            w.write(file[0:break_pt] + "\n<p>Time: " + str(datetime.now()) + ", User: " + request.session['username'] + ", Description: " + message + "</p>" + file[break_pt:])
        except:
            w.write(file[0:break_pt] + "\n<p>Time: " + str(datetime.now()) + ", Description: " + message + "</p>" + file[break_pt:])
"""
ct = ContentType.objects.get_for_model(User)
permission = Permission.objects.create(codename="can_edit_schools",
                                                   name="Can Edit Schools",
                                                   content_type=ct)
permission.save()
"""
