from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import GpsDataForm
from .models import GpsData



# Create your views here.

def index(request):
    return HttpResponse("Hi there bro!")

def model_form_upload(request):

    if request.method == 'POST':
        form = GpsDataForm(request.POST, request.FILES)
        if form.is_valid():
            m = form.save()
            map_results = m.get_map()
            return render(request, 'ml/results.html', {'pk': m.pk, 
                                                      'map': map_results[1], 
                                                     'name': m.name, 
                                                    'email': m.email,
                                                    'velocity': map_results[2],
                                                    'acceleration': map_results[3],
                                                    'total': map_results[4]
                                                    })
    else:
        form = GpsDataForm()
    return render(request, 'ml/model_form_upload.html', {
        'form': form
    })


def results(request, pk):
    obj = GpsData.objects.get(pk=pk)
    if request.method == 'GET':
        html = obj.get_map()[0]
        return HttpResponse(html)