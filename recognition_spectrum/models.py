from django.db import models


class UploadedSignal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('done', 'Done'),
        ('error', 'Error'),
    ]
    file = models.FileField(upload_to='uploads/signals/')
    upload_date = models.DateTimeField(auto_now_add=True)
    spectrum_image_path = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    spectrum_elements = models.JSONField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
