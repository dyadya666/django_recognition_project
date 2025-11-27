from django.db import models


class UploadedVideo(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('done', 'Done'),
        ('error', 'Error'),
    ]
    video = models.FileField(upload_to='uploads/videos/')
    upload_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result = models.JSONField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-upload_date']

    def __str__(self):
        return f'Video {self.pk} - {self.status}'
