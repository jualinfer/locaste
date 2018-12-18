from django.urls import path
from .views import VisualizerView


urlpatterns = [
    path('<int:voting_id>/<str:custom_url>', VisualizerView.as_view()),
    path('<int:voting_id>/', VisualizerView.as_view()),
]
