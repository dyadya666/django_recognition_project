from django.core.files.storage import FileSystemStorage
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.urls import reverse

from .forms import UploadForm
from .utils import analyze_spectrum, save_spectrogram
from .models import UploadedSignal


class SignalUploadView(FormView):
    template_name = "recognition_spectrum/upload.html"
    form_class = UploadForm
    signal = None

    def form_valid(self, form):
        # Зберігаємо файл
        signal_file = form.cleaned_data['file']
        fs = FileSystemStorage()
        filename = fs.save(signal_file.name, signal_file)
        file_path = fs.path(filename)

        # Створюємо об'єкт моделі
        self.signal = UploadedSignal.objects.create(
            file=filename,
            status='processing'
        )

        # Аналіз спектру
        result = analyze_spectrum(file_path)
        spectrogram_path = save_spectrogram(file_path)

        # Оновлюємо модель
        self.signal.spectrum_elements = result
        self.signal.spectrum_image_path = spectrogram_path
        self.signal.status = 'done'
        self.signal.save()

        return super().form_valid(form)
        
    
    def get_success_url(self):
        # динамічний редирект на detail
        return reverse("recognition_spectrum:detail", args=[self.signal.pk])


class SignalDetailView(DetailView):
    model = UploadedSignal
    template_name = "recognition_spectrum/detail.html"
    context_object_name = "object"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # додаємо додаткові дані для шаблону
        context["file"] = self.object.file.name
        context["result"] = self.object.spectrum_elements
        context["spectrogram"] = self.object.spectrum_image_path

        print(f'get_context_data: {self.object.spectrum_image_path}')
        print(f'get_context_data: {context["spectrogram"]}')

        return context
