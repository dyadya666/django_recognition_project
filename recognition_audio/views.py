from django.shortcuts import redirect
from django.views import generic

from .forms import UploadAudioForm
from .models import UploadedAudio
from .utils import classify_audio


class UploadAudioView(generic.CreateView):
    model = UploadedAudio
    form_class = UploadAudioForm
    template_name = 'recognition_audio/upload.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.status = dict(UploadedAudio.STATUS_CHOICES)['processing']
        obj.save()
        try:
            result = classify_audio(obj.audio.path)
            obj.result = result
            obj.status = dict(UploadedAudio.STATUS_CHOICES)['done']
        except Exception as e:
            obj.status = dict(UploadedAudio.STATUS_CHOICES)['error']
            obj.error = str(e)
        
        obj.save()

        return redirect('recognition_audio:detail', pk=obj.pk)
    

class AudioDetailView(generic.DetailView):
    model = UploadedAudio
    template_name = 'recognition_audio/detail.html'
    context_object_name = 'audio'
    
