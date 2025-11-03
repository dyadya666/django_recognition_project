from django.urls import path

from . import views


app_name = "recognition_images"

urlpatterns = [
    path("", views.UploadAndClassifyView.as_view(), name="home")
]

