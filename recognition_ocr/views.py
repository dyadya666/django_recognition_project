import django_rq

from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.urls import reverse

from .forms import DocumentUploadForm
from .models import UploadedDocument
from .tasks import run_ocr


class DocumentUploadView(FormView):
    template_name = "recognition_ocr/upload.html"
    form_class = DocumentUploadForm

    def form_valid(self, form):
        self.document = form.save(commit=False)
        self.document.status = "processing"
        self.document.save()
        
        # Відправляємо OCR у фонову чергу
        django_rq.enqueue(run_ocr, self.document.pk)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("recognition_ocr:ocr_detail", kwargs={"pk": self.document.pk})


class DocumentDetailView(DetailView):
    model = UploadedDocument
    template_name = "recognition_ocr/detail.html"


def ocr_status(request, pk):
    doc = UploadedDocument.objects.get(pk=pk)

    return JsonResponse({
        'status': doc.status,
        'text': doc.extracted_text,
        'error': doc.error_message
    })
