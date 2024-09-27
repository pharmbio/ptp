import os
import subprocess
from celery import shared_task
from .models import InferenceJob, Result
from django.core.mail import send_mail
from django.conf import settings
import pandas as pd

@shared_task
def run_inference(job_id):
    job = InferenceJob.objects.get(id=job_id)
    job.status = 'running'
    job.save()

    # Paths for input and output
    smiles_file_path = job.smiles_file.path
    output_dir = f"/tmp/inference_{job_id}/"
    os.makedirs(output_dir, exist_ok=True)

    # Select models based on the ChEMBL version
    if job.chembl_version == '33':
        model_files = ['model_chembl33_1.zip', 'model_chembl33_2.zip']
    elif job.chembl_version == '34':
        model_files = ['model_chembl34_1.zip', 'model_chembl34_2.zip']
    else:
        raise ValueError(f"Unsupported ChEMBL version: {job.chembl_version}")

    results = []
    for model in model_files:
        output_file = os.path.join(output_dir, f"{os.path.basename(model)}_result.csv")
        logfile = os.path.join(output_dir, f"{os.path.basename(model)}_log.txt")

        # Command to run inference with CPSign
        cmd = f"java -jar cpsign.jar predict --model {model} --predict-file csv delim=, {smiles_file_path} --output-format csv --output {output_file} --logfile {logfile}"

        # Run the subprocess
        subprocess.run(cmd, shell=True)

        # Read the result file
        df = pd.read_csv(output_file)
        results.append(df)

    # Concatenate and transpose results
    final_result = pd.concat(results, axis=1)
    transposed_result = final_result.transpose()

    # Save the final result to a CSV
    result_file_path = os.path.join(output_dir, 'final_result.csv')
    transposed_result.to_csv(result_file_path, index=False)

    # Save result in Django model
    job.result_file.name = f"results/{job_id}_final_result.csv"

    with open(result_file_path, 'rb') as f:
        result = Result.objects.create(job=job)
        result.result_file.save(f"{job_id}_final_result.csv", f)

    job.result_file.name = f"results/{job_id}_final_result.csv"
    job.status = 'completed'
    job.save()

    job.status = 'completed'
    job.save()

    # Send email if provided
    if job.email:
        send_mail(
            'Your inference job is complete',
            f'Your job is complete. Download the result here: {settings.SITE_URL}/media/{result.result_file.name}',
            'noreply@yourdomain.com',
            [job.email]
        )

    # Optionally clean up temp files
    cleanup_output_files(output_dir)


def cleanup_output_files(output_dir):
    # Delete temporary directory and files
    if os.path.exists(output_dir):
        subprocess.run(f'rm -rf {output_dir}', shell=True)

@shared_task
def cleanup_old_jobs():
    """Scheduled task to clean up result files older than 30 days."""
    old_jobs = InferenceJob.objects.filter(created_at__lt=timezone.now() - timedelta(days=30))
    for job in old_jobs:
        if job.result_file:
            job.result_file.delete()
        job.delete()