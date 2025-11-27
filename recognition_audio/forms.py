from django import forms

from .models import UploadedAudio


class UploadAudioForm(forms.ModelForm):
    class Meta:
        model = UploadedAudio
        fields = ['audio']
