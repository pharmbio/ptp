from django import forms
from .models import InferenceJob

CHEMBL_CHOICES = [
    ('31', 'ChEMBL 31'),
    ('32', 'ChEMBL 32'),
    ('33', 'ChEMBL 33'),
    ('34', 'ChEMBL 34'),
    # Add more versions as needed
]


class InferenceJobForm(forms.ModelForm):
    email = forms.EmailField(required=False, help_text="Optional: Get notified when the job is complete.")
    chembl_version = forms.ChoiceField(choices=CHEMBL_CHOICES, required=True, label="ChEMBL Version")

    class Meta:
        model = InferenceJob
        fields = ['smiles_file', 'email', 'chembl_version']