from django.db import models
from auth_app.models import CustomUser

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    tags = models.JSONField(default=list)  # Ex: ["React", "JavaScript"]
    salary = models.CharField(max_length=20)
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, default='Open')  # "Open", "Closed"
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
