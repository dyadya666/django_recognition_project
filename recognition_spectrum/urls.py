from django.urls import path

from .views import SignalDetailView, SignalUploadView


app_name = "recognition_spectrum"

urlpatterns = [
    path("", SignalUploadView.as_view(), name="home"),
    path("<int:pk>/", SignalDetailView.as_view(), name="detail"),
]
