from django import forms
from .models import UploadedVideo


class UploadVideoForm(forms.ModelForm):
    unsupported_error_message = 'Unsupported video type.'
    too_large_error_message = 'File too large.'

    class Meta:
        model = UploadedVideo
        fields = ['video']

    def clean_video(self):
        uploaded_video = self.cleaned_data.get('video')
        if uploaded_video:
            allowed = ['video/mp4', 'video/quicktime', 'video/x-msvideo', 'video/x-matroska']
            if uploaded_video.content_type not in allowed:
                raise forms.ValidationError(self.unsupported_error_message)
            
            if uploaded_video.size > 200 * 1024 * 1024:
                raise forms.ValidationError(self.too_large_error_message)
            
        return uploaded_video
