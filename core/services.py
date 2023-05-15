import re


def send_job_created_mail(job_id):
    print("JOB CREATED")


def send_job_updated_mail(
    job_id: int, old_title_rich_text: str, new_title_rich_text: str
):
    print("JOB UPDATED")
    print("OLD JOD TITLE: {}".format(old_title_rich_text))
    print("NEW JOB TITLE: {}".format(new_title_rich_text))


def remove_html_tags(text: str) -> str:
    clean_text = re.sub("<.*?>", "", text)
    return clean_text
