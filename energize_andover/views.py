from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from energize_andover.forms import MetasysUploadForm
from energize_andover.script.file_transfer import transform_and_respond
from django.core.urlresolvers import reverse

def index(request):
    # Handle file upload
    if request.method == 'POST':
        form = MetasysUploadForm(request.POST, request.FILES)
        print('post is %s' % request.POST)
        if form.is_valid():
            return transform_and_respond(form.cleaned_data)
    else:
        form = MetasysUploadForm() # An empty, unbound form

    # Render list page with the documents and the form
    return HttpResponse(render(request, 'energize_andover/index.html',
                               context={'title': 'Metasys Parsing', 'form': form}))
