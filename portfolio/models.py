from django.db import models

# Create your models here.
from django.db import models
from django.contrib.postgres.fields import JSONField  # optional if using Postgres
from django.utils import timezone

class PortfolioItem(models.Model):
    """
    A canonical portfolio entry: project or GitHub repo or personal service.
    """
    title = models.CharField(max_length=200)
    short_description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    github_url = models.URLField(blank=True, null=True)
    extra_data = models.JSONField(blank=True, null=True)  # stores metadata (stars, language)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ScrapeTask(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("RUNNING", "Running"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]
    url = models.URLField()
    triggered_by = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    result = models.JSONField(null=True, blank=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_running(self):
        self.status = "RUNNING"
        self.started_at = timezone.now()
        self.save()