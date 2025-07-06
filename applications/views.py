from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Application
from .serializers import ApplicationSerializer
from django.shortcuts import get_object_or_404
from jobs.models import Job
from .serializers import ApplicationStatusUpdateSerializer
from .tasks import send_application_status_email
import logging
from rest_framework import status as drf_status


logger = logging.getLogger(__name__)

class ApplyToJobView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(candidate=self.request.user)

class MyApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logger.debug(f"Current user for /my/ applications: {self.request.user} {self.request.user.id}")
        return Application.objects.filter(candidate=self.request.user)



class UpdateApplicationStatusView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'application_id'

    def patch(self, request, *args, **kwargs):
        application = self.get_object()
        old_status = application.status  # optional: track old status if needed

        serializer = self.get_serializer(application, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # 🔄 Updates the application status

        logger.info(f"Application {application.id} status changed from {old_status} to {serializer.data['status']}")

        # ✅ After saving, send email via Celery
        new_status = serializer.data['status']
        subject = f"Your Job Application Status: {new_status}"
        message = f"Hello {application.candidate.username},\n\nYour application status has been updated to: {new_status}.\n\nThank you!"
        send_application_status_email.delay(application.candidate.email, subject, message)

        return Response({
            "message": f"Application status updated to {new_status}"
        }, status=drf_status.HTTP_200_OK)
    

class JobApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        job = get_object_or_404(Job, id=job_id)

        # Only allow recruiters who posted this job
        if job.posted_by != self.request.user:
            return Application.objects.none()

        return Application.objects.filter(job=job)
