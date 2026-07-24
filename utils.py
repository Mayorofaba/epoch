import os
import smtplib
from email.message import EmailMessage
import joblib
from typing import Optional
import os


def load_pipeline(models_dir="models"):
    path = os.path.join(models_dir, "severity_pipeline.joblib")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found at {path}. Run train_model.py first.")
    return joblib.load(path)


def send_email_smtp(
    subject: str,
    body: str,
    recipient: str,
    smtp_host: Optional[str] = None,
    smtp_port: Optional[int] = None,
    smtp_user: Optional[str] = None,
    smtp_password: Optional[str] = None,
):
    smtp_host = smtp_host or os.environ.get("SMTP_HOST")
    smtp_port = int(smtp_port or os.environ.get("SMTP_PORT", 587))
    smtp_user = smtp_user or os.environ.get("SMTP_USER")
    smtp_password = smtp_password or os.environ.get("SMTP_PASSWORD")

    if not all([smtp_host, smtp_port, smtp_user, smtp_password]):
        raise ValueError("SMTP configuration is incomplete. Set SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD.")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = recipient
    msg.set_content(body)

    # Use SSL for port 465, otherwise use STARTTLS
    if smtp_port == 465:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)


def send_email_sendgrid(
    subject: str,
    body: str,
    recipient: str,
    from_email: Optional[str] = None,
    api_key: Optional[str] = None,
):
    """Send email via SendGrid Web API. Requires `sendgrid` package."""
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
    except Exception as e:
        raise RuntimeError("sendgrid package not installed. Run `pip install sendgrid`.") from e

    api_key = api_key or os.environ.get("SENDGRID_API_KEY")
    if not api_key:
        raise ValueError("SENDGRID_API_KEY not set in environment or not provided.")

    message = Mail(
        from_email=from_email or os.environ.get("SMTP_USER") or "no-reply@example.com",
        to_emails=recipient,
        subject=subject,
        plain_text_content=body,
    )

    client = SendGridAPIClient(api_key)
    response = client.send(message)
    return response.status_code, response.body, response.headers
