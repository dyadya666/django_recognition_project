from django import forms

from .models import UploadedSignal

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadedSignal
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'accept': '.wav,.mp3,.flac'
            }),
        }
        labels = {
            'file': 'Завантажте аудіо/сигнал',
        }
