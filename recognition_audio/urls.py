from django.urls import path

from .views import UploadAudioView, AudioDetailView


app_name = 'recognition_audio'
urlpatterns = [
    path('', UploadAudioView.as_view(), name='home'),
    path('<int:pk>/', AudioDetailView.as_view(), name='detail'),
]

