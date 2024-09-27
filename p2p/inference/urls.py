from django.urls import path
from . import views


app_name = 'inference'

urlpatterns = [
    path('', views.submit_job, name='submit_job'),
    path('status/<int:job_id>/', views.job_status, name='job_status'),
]