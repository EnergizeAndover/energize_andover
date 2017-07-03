from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from energize_andover.models import SpecialUser

    #The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    # Show this when the user types help
    help = "Instatiates First Main User"
    def handle(self, *args, **options):
        username = input("Enter Username: ")
        password = input("Enter Password: ")

        user = User.objects.create_user(username=username, password=password)
        user.save()
        ct = ContentType.objects.get_for_model(User)
        try:
            permission = Permission.objects.create(codename = "master",
                                                   name = "Master",
                                                   content_type = ct)
            permission.save()
        except:
            permission = Permission.objects.get(codename='master')
        user.user_permissions.add(permission)
        user.save()
        try:
            permission = Permission.objects.create(codename="can_create_user",
                                                   name="Can Create User",
                                                   content_type=ct)
            permission.save()
        except:
            permission = Permission.objects.get(codename='can_create_user')
        user.user_permissions.add(permission)
        user.save()
        su = SpecialUser(User = user)
        su.save()
