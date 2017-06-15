from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from energize_andover.models import *
from login.forms import *

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
                return HttpResponseRedirect(dest_string)
            else:
                return HttpResponse(render(request, 'energize_andover/Login.html', {'form': form, 'message': "Login Failed: Incorrect Username and/or Password"}))
        return HttpResponse(render(request, 'energize_andover/Login.html', {'form': form}))


def logout (request):
    if (request.GET.get('mybtn')):
        request.session['logged_in'] = None
        request.session['username'] = None
        request.session['password'] = None
        return HttpResponseRedirect("Login")

def user_creation(request):
    if request.method == "GET":
        form = NewUserForm(request.GET, request.FILES)
        if form.is_valid():
            user = authenticate(username=request.GET.get('master_username'), password=request.GET.get('master_password'))
            if user is not None and Permission.objects.filter(codename = "can_create_user").first() in user.user_permissions.all():
                schools = form.cleaned_data['approved_schools']
                if request.GET.get('username') is not None and request.GET.get('password') is not None and request.GET.get('email') is not None:
                    new_user = User.objects.create_user(username=request.GET.get('username'),
                                     password=request.GET.get('password'), email=request.GET.get('email'))
                    new_user.save()
                    schools_user = SpecialUser(User = new_user)
                    schools_user.save()
                    for i in schools:
                        schoo = School.objects.filter(Name = i).first()
                        schools_user.Authorized_Schools.add(schoo)
                    schools_user.save()
                    return HttpResponseRedirect('Login')
                else:
                    return render(request, 'energize_andover/UserCreation.html', {'form': form, 'message': "Missing Username, Password, or Email"})
            else:
                return render(request, 'energize_andover/UserCreation.html', {'form': form, 'message': "Incorrect Administrator Username and/or Password"})
        return render(request, 'energize_andover/UserCreation.html', {'form': form})

def user_management(request):
    if check_status(request) is False:
        return HttpResponseRedirect("electric")
    if check_admin(request) is False:
        return HttpResponseRedirect("electric")
    user_list = User.objects.all()
    usrs = []
    for user in user_list:
        if not (user.username == request.session['username'] or Permission.objects.get(codename = 'master') in user.user_permissions.all()):
            usrs.append(user)
    if request.method == "GET":
        for usr in usrs:
            if (request.GET.get(usr.username)) == "Delete":
                usr.delete()
                return HttpResponseRedirect('Management')
            elif (request.GET.get(usr.username)) == "Edit":
                return HttpResponseRedirect('Editing'+str(usr.pk))
    return HttpResponse(render(request, 'energize_andover/UserManagement.html', {'users': usrs}))

def user_editing(request, user_id):
    if check_status(request) is False:
        return HttpResponseRedirect("electric")
    if check_admin(request) is False:
        return HttpResponseRedirect("electric")
    print (user_id)
    user = User.objects.get(pk = user_id)
    su = SpecialUser.objects.get(User = user)
    authorized_schools = su.Authorized_Schools.all()
    schools = School.objects.all()
    admin_permission = Permission.objects.get(codename='can_create_user')
    user_permission_list = user.user_permissions.all()
    if request.GET.get('save'):
        for school in schools:
            if request.GET.get(school.Name):
                if school not in authorized_schools:
                    su.Authorized_Schools.add(school)
            else:
                if school in authorized_schools:
                    su.Authorized_Schools.remove(school)
        if request.GET.get('is_admin'):
            if admin_permission not in user_permission_list:
                user.user_permissions.add(admin_permission)
        else:
            if admin_permission in user_permission_list:
                user.user_permissions.remove(admin_permission)
        return HttpResponseRedirect("Management")
    return HttpResponse(render(request, 'energize_andover/UserEditing.html',
                               {"schools": schools, 'user':user,
                                "authorized_schools": authorized_schools,
                                "admin_permission": admin_permission,
                                "user_permission_list": user_permission_list}))

def check_status(request):
    if (request.session.get('logged_in', None) == None):
        req = str(request).replace("/energize_andover", "")
        request.session['destination'] = req[req.index ("/") + 1: len(req) - 2]
        return False
    return True

def check_admin(request):
    user = authenticate(username = request.session['username'], password = request.session['password'])
    if Permission.objects.filter(codename="can_create_user").first() in user.user_permissions.all():
        return True
    return False
"""
ct = ContentType.objects.get_for_model(User)
permission = Permission.objects.create(codename = "master",
                                       name = "Master",
                                       content_type = ct)
permission.save()
User.objects.filter(username = "energizeandover").first().user_permissions.add(permission)
"""
