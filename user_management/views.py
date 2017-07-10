from django.contrib.contenttypes.models import ContentType
from user_management.forms import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from login.views import check_status, check_admin, update_log

def user_creation(request):
    if request.method == "GET":
        form = NewUserForm(request.GET, request.FILES)
        if form.is_valid():
            user = authenticate(username=request.GET.get('master_username'), password=request.GET.get('master_password'))
            if user is not None and Permission.objects.get(codename = "can_create_user") in user.user_permissions.all():
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
                    message = str("User " + request.GET.get('username') + "created by User " + request.GET.get('master_username'))
                    #message = "User Created"
                    update_log(message, None, request)
                    return HttpResponseRedirect('Login')
                else:
                    return render(request, 'energize_andover/UserCreation.html', {'form': form, 'message': "Missing Username, Password, or Email"})
            else:
                return render(request, 'energize_andover/UserCreation.html', {'form': form, 'message': "Incorrect Administrator Username and/or Password"})
        return render(request, 'energize_andover/UserCreation.html', {'form': form})

def user_management(request):
    if check_status(request) is False:
        return HttpResponseRedirect("Login")
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
    school_edit_permission = Permission.objects.get(codename='can_edit_schools')
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
        if request.GET.get('can_edit'):
            if school_edit_permission not in user_permission_list:
                user.user_permissions.add(school_edit_permission)
        else:
            if school_edit_permission in user_permission_list:
                user.user_permissions.remove(school_edit_permission)
        return HttpResponseRedirect("Management")
    return HttpResponse(render(request, 'energize_andover/UserEditing.html',
                               {"schools": schools, 'user':user,
                                "authorized_schools": authorized_schools,
                                "admin_permission": admin_permission,
                                "school_edit_permission": school_edit_permission,
                                "user_permission_list": user_permission_list}))
