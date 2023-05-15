from rest_framework import serializers
from rest_framework.exceptions import APIException

from core.constants import JobType
from core.models import Application, Job, JobTitle
from core.services import (
    remove_html_tags,
    send_job_created_mail,
    send_job_updated_mail,
)


class JobTitileSerializer(serializers.ModelSerializer):
    plain_title_text = serializers.SerializerMethodField(
        method_name="get_plain_title_text"
    )

    class Meta:
        model = JobTitle
        fields = "__all__"

    def get_plain_title_text(self, instance: JobTitle):
        return remove_html_tags(instance.rich_title_text)


class JobSerializer(serializers.ModelSerializer):
    job_title = JobTitileSerializer()

    class Meta:
        model = Job
        fields = "__all__"

    def validate_type(self, value: str):
        allowed_values: list[str] = JobType.values()

        if value not in allowed_values:
            raise APIException(f"Allowed values for type: {allowed_values}")

        return value

    def create(self, validated_data: dict):
        # Validate the data using serializers
        job_title_serializer = JobTitileSerializer(
            data=validated_data["job_title"]
        )
        job_title_serializer.is_valid(raise_exception=True)
        job_title = job_title_serializer.create(
            job_title_serializer.validated_data
        )

        # Create the instance in the database
        validated_data["job_title"] = job_title
        instance: Job = super().create(validated_data)

        # Send the email
        send_job_created_mail(
            job_id=instance.id,  # type: ignore
        )

        # Create the application based on the job instance
        # NOTE: We can create it directly since we are sure about the correct
        #       job instance creation
        Application.objects.create(
            user=self.context["request"].user, job=instance
        )

        return instance

    def update(self, instance: Job, validated_data: dict):
        # Save the old text value for seding via the email
        old_job_title: str = instance.job_title.rich_title_text

        # Validate the data using serializers
        job_title_serializer = JobTitileSerializer(
            data=validated_data["job_title"]
        )
        job_title = JobTitle.objects.get(id=instance.job_title.id)
        job_title_serializer.is_valid(raise_exception=True)
        job_title_serializer.update(
            job_title, validated_data=validated_data["job_title"]
        )

        # Update the instance in the database
        validated_data["job_title"] = job_title
        updated_insatnce = super().update(instance, validated_data)

        # Send the email
        send_job_updated_mail(
            job_id=instance.id,  # type: ignore
            old_title_rich_text=old_job_title,
            new_title_rich_text=job_title.rich_title_text,
        )

        return updated_insatnce


class ApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)

    class Meta:
        model = Application
        fields = "__all__"
