from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
import requests
from django.conf.urls import url
#from energize_andover.energize_andover.forms import MetasysUploadForm, GraphUploadForm, SmartGraphUploadForm
#from energize_andover.energize_andover.script.file_transfer import get_transformed_file
#from energize_andover.energize_andover.script.file_transfer_grapher import get_transformed_graph
from energize_andover.forms import MetasysUploadForm, GraphUploadForm, SmartGraphUploadForm
from energize_andover.script.file_transfer import get_transformed_file, graph_transformed_file
from energize_andover.script.file_transfer_grapher import get_transformed_graph
from django.core.urlresolvers import reverse

def index(request):
    # Handle file upload
    if request.method == 'POST':
        print(request.POST.get("parse"))
    if request.method == 'POST' and request.POST.get('parse'):
        print(request.POST)
        form = MetasysUploadForm(request.POST, request.FILES)
        print('post is %s' % request.POST)

        if form.is_valid():

            data = form.cleaned_data
            if not data['graph']:

                return get_transformed_file(data)
            else:
                form2 = SmartGraphUploadForm()
                get_transformed_file(data)
                return HttpResponse(render(request, 'energize_andover/index.html',
                                           context={'title': 'Metasys Parsing',
                                                    'form2': form2}))
    elif request.method == 'POST' and request.POST.get('graph'):
        form2 = SmartGraphUploadForm(request.POST, request.FILES)
        print('post is %s' % request.POST)
        if form2.is_valid():
            return graph_transformed_file(form2.cleaned_data)
        else:
            return HttpResponse(render(request, 'energize_andover/index.html',
                                       context={'title': 'Metasys Parsing',
                                                'form2': form2}))
    else:
        form = MetasysUploadForm()  # An empty, unbound form

    # Render list page with the documents and the form
    return HttpResponse(render(request, 'energize_andover/index.html',
                               context={'title': 'Metasys Parsing', 'form': form}))


def grapher(request):
    #Handle file upload
    if request.method == 'POST':
        form = GraphUploadForm(request.POST, request.FILES)
        print('post is %s' % request.POST)
        if form.is_valid():
            return render(get_transformed_graph(form.cleaned_data))
    else:
        form = GraphUploadForm()

    # Render list page with the documents and the form
    return HttpResponse(render(request, 'energize_andover/grapher.html',
                               context={'title': 'Grapher', 'form': form}))