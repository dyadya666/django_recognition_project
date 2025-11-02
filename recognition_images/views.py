from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import UploadForm
from .models import UploadedImage
from .utils import classify_image


class UploadAndClassifyView(generic.CreateView):
    model = UploadedImage
    form_class = UploadForm
    template_name = 'recognition_images/upload.html'
    success_url = reverse_lazy('recognition_images:home')

    def form_valid(self, form):
        # зберігаємо файл, щоб отримати доступ до obj.image.path
        obj = form.save(commit=False)
        obj.save()
        try:
            obj.result = classify_image(obj.image.path)
        except Exception as e:
            obj.result = f'Error: {e}'
        
        obj.save()

        return render(self.request, 'recognition_images/result.html', {'object': obj})
    
    def form_invalid(self, form):
        # Повертаємо стандартний рендер із формою та помилками
        return self.render_to_response(self.get_context_data(form=form))
