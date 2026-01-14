from django.db import models


class UploadedDocument(models.Model):
    file = models.FileField(upload_to="documents/")
    extracted_text = models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
