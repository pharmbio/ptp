import os
import subprocess
from celery import shared_task
from .models import InferenceJob, Result
from django.core.mail import send_mail
from django.conf import settings
import pandas as pd
from datetime import timezone
from pathlib import Path

model_dir = os.environ.get("MODEL_DIR", "/app/ext_storage/models")
Path(model_dir).mkdir(parents=True, exist_ok=True)
max_models = os.environ.get("MAX_MODELS", False)

@shared_task
def run_inference(job_id):

    job = InferenceJob.objects.get(id=job_id)
    job.status = 'running'
    job.save()

    # Paths for input and output
    smiles_file_path = job.smiles_file.path
    output_dir = f"/tmp/inference_{job_id}/"
    os.makedirs(output_dir, exist_ok=True)

    print("selected ChEMBL version:", job.chembl_version, flush=True)
    # Select models based on the ChEMBL version

    if str(job.type == 'vennABERS'):
        path = 'vennABERS_models'
    else:
        path = 'conformal_models'

    if str(job.chembl_version) == '31':
        chembl_version = 'chembl_31'
    if str(job.chembl_version) == '32':
        chembl_version = 'chembl_32'
    if str(job.chembl_version) == '33':
        chembl_version = 'chembl_33'
    elif str(job.chembl_version) == '34':
        chembl_version = 'chembl_34'
    else:
        chembl_version = 'chembl_34'
    base = model_dir
    try:
        model_files = [os.path.join(base,chembl_version,path, f) for f in os.listdir(os.path.join(base, chembl_version,path)) if f.endswith('.jar')]
    except Exception as e:
        job.status = 'failed'
        job.save()
        cleanup_output_files(output_dir)
        print("Failed to load models:", e, flush=True)
        return
    results = []
    result_filenames = []
    print("Running inference...", flush=True)
    DEBUG=True

    if DEBUG:
        print("RUNNING IN DEBUG MODE ONLY CALCULATING 3 MODELS", flush=True)
        model_files = model_files#[:5]
    if max_models:
        model_files = model_files[:int(max_models)]

    try:
        for model in model_files:
            print("Running inference for model:", model, flush=True)
            output_file = os.path.join(output_dir, f"{os.path.basename(model)}_result.csv")
            logfile = os.path.join(output_dir, f"{job_id}-{os.path.basename(model)}_log.txt")

            cpsign = '/app/inference/cpsign/cpsign-2.0.0-fatjar.jar'
            # Command to run inference with CPSign
            cmd = f"java -jar {cpsign} predict --model {model} --predict-file csv delim=, {smiles_file_path} --output-format csv --output {output_file} --logfile {logfile}"

            # Run the subprocess
            print("Running command:", cmd, flush=True)
            subprocess.run(cmd, shell=True)
            print("Finished running command", flush=True)

            # Read the result file
            print("Reading result file...", flush=True)
            df = pd.read_csv(output_file)
            print("Finished reading result file", flush=True)

            #d = {'col1': [1, 2], 'col2': [3, 4]}
            #df = pd.DataFrame(data=d)
            result_filenames.append(output_file)
            results.append(df)

    except Exception as e:
        job.status = 'failed'
        job.save()
        cleanup_output_files(output_dir)
        print("Inference failed:", e, flush=True)

    result_file_path = None
    """
    try:
        # Concatenate and transpose results
        print("Concatenating results...", flush=True)
        final_result = pd.concat(results, axis=1)
        transposed_result = final_result.transpose()

        # Save the final result to a CSV
        result_file_path = os.path.join(output_dir, 'final_result.csv')
        transposed_result.to_csv(result_file_path, index=False)

    except Exception as e:
        job.status = 'failed'
        job.save()
        cleanup_output_files(output_dir)
        print("Result processing failed to concatenate results:", e, flush=True)
    """

    print("Concatenating results...", flush=True)
    result_file_path = f"resultfilepath-{job_id}.csv"

    try:
        # Paths for input and output
        original = job.smiles_file.path
        from pathlib import Path
        predictions_path = Path(output_dir)

        original_columns = pd.read_csv(original, nrows=0).columns

        p_i_dictionaries = []
        p_a_dictionaries = []
        targets = []

        i = 0
        original_file = pd.read_csv(original)

        for p in results: #predictions_path.glob('*.csv'):
            print("Processing file:", p, flush=True)

            df = p #d.read_csv(p)

            # Create dictionaries for each row
            p_i_dict = {row[0]: row[-2] for _, row in df.iterrows()}
            p_a_dict = {row[0]: row[-1] for _, row in df.iterrows()}

            p_i_dictionaries.append(p_i_dict)
            p_a_dictionaries.append(p_a_dict)
            targets.append(result_filenames[i].split('/')[-1].split('_')[0])
            i += 1

        df_result = pd.DataFrame()
        df_result['SMILES'] = original_file['SMILES']



        for target, p_i, p_a in zip(targets, p_i_dictionaries, p_a_dictionaries):
            print("joining for target:", target, flush=True)
            df_result[target + '_p_i'] = df_result['SMILES'].map(p_i)
            df_result[target + '_p_a'] = df_result['SMILES'].map(p_a)

        df_result.drop(axis='index', labels=0, inplace=True)
        #print("Finished processing file:", p, flush=True)
        df_result.to_csv(result_file_path, index=False)
        #print("saving to resultfile path", flush=True)

        #df = pd.concat(dfs)

        #df = df.pivot(index='SMILES', columns='stem', values=['pa', 'pi'])
        #df.columns = [stem + '_' + papi for (papi, stem) in df.columns.to_flat_index()]

        #toAdd = oldCols
        #toAdd.set_index("SMILES", inplace=True)

        #df = pd.concat((df, toAdd), axis=1)
        #result_file_path = os.path.join(output_dir, 'final_result.csv')
        #df.to_csv(result_file_path, index=False)

    except Exception as e:
        job.status = 'failed'
        job.save()
        cleanup_output_files(output_dir)
        print("Result processing failed to concatenate results:", e, flush=True)

    from .models import Result
    # Save result in Django model
    #job.result_file.name = f"results/{job_id}_final_result.csv"
    import uuid
    identifier = str(uuid.uuid4())
    if result_file_path:
        with open(result_file_path, 'rb') as f:
            result = Result.objects.create(job=job)
            result.result_file.save(f"{job_id}_{identifier}_result.csv", f)

    #job.result_file.name = f"results/{job_id}_final_result.csv"

    #from .models import Result
    #res = Result.objects.create(job=job, result_file=f"results/{job_id}_final_result.csv")
    #res.save()

    job.status = 'completed'
    job.save()



    # Send email if provided
    if job.email:
        send_mail(
            'Your inference job is complete',
            f'Your job is complete. Download the result here: {settings.SITE_URL}/media/{result.result_file.name}',
            'noreply@pharmb.io',
            [job.email]
        )

    # Optionally clean up temp files
    #cleanup_output_files(output_dir)


def cleanup_output_files(output_dir):
    # Delete temporary directory and files
    if os.path.exists(output_dir):
        subprocess.run(f'rm -rf {output_dir}', shell=True)

@shared_task
def cleanup_old_jobs():
    """Scheduled task to clean up result files older than 30 days."""
    from datetime import timedelta, datetime

    old_jobs = InferenceJob.objects.filter(created_at__lt=datetime.now() - timedelta(days=30))
    for job in old_jobs:
        if job.result_file:
            job.result_file.delete()
        job.delete()