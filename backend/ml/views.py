from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import GpsDataForm



# Create your views here.

def index(request):
    return HttpResponse("Hi there bro!")

def model_form_upload(request):
    if request.method == 'POST':
        form = GpsDataForm(request.POST, request.FILES)
        if form.is_valid():
            m = form.save()
            html = m.get_map()
            return HttpResponse(html)
    else:
        form = GpsDataForm()
    return render(request, 'ml/model_form_upload.html', {
        'form': form
    })
