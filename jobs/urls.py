from django.urls import path
from .views import JobListCreateView, JobRetrieveUpdateDestroyView, MyJobsView

urlpatterns = [
    path('', JobListCreateView.as_view(), name='job-list-create'),
    path('<int:pk>/', JobRetrieveUpdateDestroyView.as_view(), name='job-detail'),
    path('my/', MyJobsView.as_view(), name='my-jobs'),
]
