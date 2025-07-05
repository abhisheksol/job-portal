from django.urls import path
from .views import ApplyToJobView, MyApplicationsView, UpdateApplicationStatusView, JobApplicationsView

urlpatterns = [
    path('', ApplyToJobView.as_view(), name='apply-job'),
    path('my/', MyApplicationsView.as_view(), name='my-applications'),
    path('<int:application_id>/status/', UpdateApplicationStatusView.as_view(), name='update-status'),
    path('job/<int:job_id>/', JobApplicationsView.as_view(), name='job-applications'),
]
