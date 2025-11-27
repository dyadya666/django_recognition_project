from django.urls import path

from .views import UploadAndProcessVideoView, VideoDetailView, VideoProgressView, video_status_api


app_name = 'recognition_video'

urlpatterns = [
    path("", UploadAndProcessVideoView.as_view(), name="home"),
    path("<int:pk>/progress/", VideoProgressView.as_view(), name="progress"),
    path("<int:pk>/status/", video_status_api, name="status_api"),
    path("<int:pk>/", VideoDetailView.as_view(), name="detail"),
]

