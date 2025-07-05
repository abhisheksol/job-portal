from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_email = serializers.EmailField(source='job.posted_by.email', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'job', 'job_title', 'company_email',
            'resume',
            'status',
            'applied_on'
        ]
        read_only_fields = ['id', 'job_title', 'company_email', 'status', 'applied_on']

class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status']

