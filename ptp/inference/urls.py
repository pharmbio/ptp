from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static


app_name = 'inference'

urlpatterns = [
    path('', views.submit_job, name='submit_job'),
    path('status/<uuid:job_id>/', views.job_status, name='job_status'),
    path('stat/<uuid:job_id>/', views.job_status_json, name='job_status_json'),
]

if settings.DEBUG or settings.SERVE_STATIC:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)