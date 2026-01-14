from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.urls import reverse

from .forms import DocumentUploadForm
from .models import UploadedDocument
from .utils import extract_text


class DocumentUploadView(FormView):
    template_name = "recognition_ocr/upload.html"
    form_class = DocumentUploadForm

    def form_valid(self, form):
        self.document = form.save(commit=False)
        self.document.status = "processing"
        self.document.save()

        file_path = self.document.file.path
        text = extract_text(file_path)

        self.document.extracted_text = text
        self.document.status = "done"
        self.document.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("recognition_ocr:ocr_detail", kwargs={"pk": self.document.pk})


class DocumentDetailView(DetailView):
    model = UploadedDocument
    template_name = "recognition_ocr/detail.html"
