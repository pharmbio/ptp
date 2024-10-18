from django.shortcuts import render, redirect
from .forms import InferenceJobForm
from .models import InferenceJob
from .tasks import run_inference
from django.http import JsonResponse

def submit_job(request):

    #from django.conf import settings
    #if settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
    #    enable_email = True

    if request.method == 'POST':
        form = InferenceJobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save()
            print("form is valid! continue!",flush=True)
            run_inference.delay(job.id)
            print("form is valid! continue 2!", flush=True)
            return redirect('inference:job_status', job_id=job.id)
    else:
        form = InferenceJobForm()
    return render(request, 'inference/submit.html', {'form': form})


from django.http import JsonResponse
from .models import InferenceJob, Result


def job_status(request, job_id):
    job = InferenceJob.objects.get(id=job_id)
    try:
        result = Result.objects.get(job=job)
        result_url = result.result_file.url if result.result_file else None
    except Result.DoesNotExist:
        result_url = None

    return render(request, 'inference/status.html', locals())


def job_status_json(request, job_id):
    job = InferenceJob.objects.get(id=job_id)
    try:
        result = Result.objects.get(job=job)
        result_url = result.result_file.url if result.result_file else None
    except Result.DoesNotExist:
        result_url = None

    return JsonResponse({
        'status': job.status,
        'result_file': result_url
    })