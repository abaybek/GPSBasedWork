from django.urls import path

from . import views

urlpatterns = [
    path('', views.model_form_upload, name='model_form_upload'),
    path('result/<int:pk>/', views.results, name='results')
]