from django.urls import path
from . import views


urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('create/', views.votingForm, name='create_voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
    path('list/', views.VotingList.as_view(), name='voting_list'),
    path('statistics/', views.voting_statistics, name='voting_statistics')
]
