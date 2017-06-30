from django.http import HttpResponse


def index(request):
    return HttpResponse('You have reached the root of the project.')
