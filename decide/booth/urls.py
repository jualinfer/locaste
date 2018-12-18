from django.urls import path
from .views import BoothView


urlpatterns = [
    path('<int:voting_id>/<str:custom_url>', BoothView.as_view()),
    path('<int:voting_id>/', BoothView.as_view()),
]
