from django.db import models
#from django.contrib.auth.models import User

class InferenceJob(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    smiles_file = models.FileField(upload_to='uploads/')
    chembl_version = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class Result(models.Model):
    job = models.OneToOneField(InferenceJob, on_delete=models.CASCADE)
    result_file = models.FileField(upload_to='results/')
    created_at = models.DateTimeField(auto_now_add=True)