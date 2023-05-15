from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class JobTitle(models.Model):
    rich_title_text = models.TextField()
    rich_subtitle_text = models.TextField()

    class Meta:
        db_table = "job_titles"


class Job(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=2)

    job_title = models.ForeignKey(
        "JobTitle",
        related_name="jobs",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "jobs"


class Application(models.Model):
    job = models.OneToOneField(
        "Job",
        on_delete=models.CASCADE,
        related_name="application",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.RESTRICT
    )

    class Meta:
        db_table = "applications"
