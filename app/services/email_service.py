import emails
from app.config import settings

def send_application_emails(job_title: str, candidate_email: str, recruiter_email: str):
    # Send email to candidate
    candidate_message = emails.Message(
        subject=f'Job Application Confirmation - {job_title}',
        html=f'<p>Your application for the position of {job_title} has been received.</p>',
        mail_from=settings.smtp_username
    )
    candidate_message.send(
        to=candidate_email,
        smtp={
            "host": settings.smtp_host,
            "port": settings.smtp_port,
            "user": settings.smtp_username,
            "password": settings.smtp_password,
            "tls": True
        }
    )

    # Send email to recruiter
    recruiter_message = emails.Message(
        subject=f'New Job Application Received - {job_title}',
        html=f'<p>A new application has been received for the position of {job_title}.</p>',
        mail_from=settings.smtp_username
    )
    recruiter_message.send(
        to=recruiter_email,
        smtp={
            "host": settings.smtp_host,
            "port": settings.smtp_port,
            "user": settings.smtp_username,
            "password": settings.smtp_password,
            "tls": True
        }
    ) 