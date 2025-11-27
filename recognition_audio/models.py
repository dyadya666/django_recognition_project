from django.db import models


class UploadedAudio(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('done', 'Done'),
        ('error', 'Error'),
    ]
    audio = models.FileField(upload_to="uploads/audio")
    uploaded_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=dict(STATUS_CHOICES)['pending'])
    result = models.JSONField(null=True, blank=True)
    error = models.TextField(blank=True, default='')

    def __str__(self):
        return f'Audio {self.pk} - {self.status}'
