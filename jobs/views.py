from rest_framework import generics, permissions
from .models import Job
from .serializers import JobSerializer
from datetime import date

class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Auto-close expired jobs
        Job.objects.filter(expiry_date__lt=date.today(), status="Open").update(status="Closed")
        return Job.objects.filter(status="Open")

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

class JobRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
