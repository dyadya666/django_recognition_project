from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.urls import reverse

from .forms import UploadVideoForm
from .models import UploadedVideo
from .utils import extract_keyframes, classify_frames, cleanup_paths

from recognition_images.utils import classify_image


class UploadAndProcessVideoView(generic.CreateView):
    model = UploadedVideo
    form_class = UploadVideoForm
    template_name = 'recognition_video/upload.html'
    STATUS_DONE = 'done'
    STATUS_ERROR = 'error'
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.status = self.STATUS_PENDING
        obj.save()
        try:
            frames = extract_keyframes(obj.video.path)
            results = classify_frames(frames, classify_image)
            obj.result = [{'frame': r['frame'], 'label': r['result']} for r in results]
            obj.status = self.STATUS_DONE
        except Exception as e:
            obj.status = self.STATUS_ERROR
            obj.error = str(e)
        finally:
            obj.save()
            cleanup_paths(frames)

        return redirect('recognition_video:progress', pk=obj.pk)


class VideoDetailView(generic.DetailView):
    model = UploadedVideo
    template_name = 'recognition_video/detail.html'
    context_object_name = 'video'


class VideoProgressView(generic.TemplateView):
    template_name = 'recognition_video/progress.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs.get('pk')
        print(f'pk: {pk}')
        obj = get_object_or_404(UploadedVideo, pk=pk)
        context['object'] = obj
        context['detail_url'] = reverse("recognition_video:detail", args=[obj.pk])

        return context


def video_status_api(request, pk):
    obj = get_object_or_404(UploadedVideo, pk=pk)

    return JsonResponse({
        'status': obj.status,
        'result': obj.result or [],
        'error': obj.error or '',
    })
