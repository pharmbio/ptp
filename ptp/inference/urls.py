from django.conf import settings
from django.urls import path
from . import views

app_name = 'inference'

urlpatterns = [
    path('', views.submit_job, name='submit_job'),
    path('status/<uuid:job_id>/', views.job_status, name='job_status'),
    path('stat/<uuid:job_id>/', views.job_status_json, name='job_status_json'),
]