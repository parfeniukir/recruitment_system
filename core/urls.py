from django.urls import path
from rest_framework.routers import DefaultRouter

from core.api import ApplicationsListAPI, JobsAPISet

router = DefaultRouter()
router.register("jobs", JobsAPISet, basename="jobs")

application_urls = [
    path("applications/", ApplicationsListAPI.as_view()),
]

# Define urlpatterns
urlpatterns = router.urls + application_urls
