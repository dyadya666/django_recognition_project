from django.db import models


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/images/')
    upload_date = models.DateTimeField(auto_now_add=True)
    result = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.image.name} > {self.result}'
