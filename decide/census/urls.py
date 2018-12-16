from django.urls import path, include
from .views import CensusView
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('view/<int:voting_id>/', CensusView.as_view(), name='census_view'),
]
