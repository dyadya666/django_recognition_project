from django.urls import path

from .views import DocumentUploadView, DocumentDetailView, ocr_status


app_name = "recognition_ocr"

urlpatterns = [
    path("", DocumentUploadView.as_view(), name="ocr_upload"),
    path("<int:pk>/", DocumentDetailView.as_view(), name="ocr_detail"),
    path("status/<int:pk>/", ocr_status, name="ocr_status"),
]
