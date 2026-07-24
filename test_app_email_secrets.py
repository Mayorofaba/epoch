import app
from unittest.mock import patch


def test_send_notification_uses_streamlit_secrets(monkeypatch):
    monkeypatch.delenv("SMTP_HOST", raising=False)
    monkeypatch.delenv("SMTP_PORT", raising=False)
    monkeypatch.delenv("SMTP_USER", raising=False)
    monkeypatch.delenv("SMTP_PASSWORD", raising=False)
    monkeypatch.setattr(
        app.st,
        "secrets",
        {
            "SMTP_HOST": "smtp.gmail.com",
            "SMTP_PORT": "587",
            "SMTP_USER": "user@example.com",
            "SMTP_PASSWORD": "app-password",
            "RECIPIENT_EMAIL": "recipient@example.com",
        },
        raising=False,
    )

    report = {
        "ReportID": "RPT123",
        "ReporterName": "Test User",
        "ReporterContact": "+1234567890",
        "Location": "Test Location",
        "DateTime": "2026-07-24T00:00:00Z",
        "Category": "Public Safety",
        "Description": "Test incident description.",
    }

    with patch("app.send_email_smtp") as mock_send_email:
        mock_send_email.return_value = (True, "Email sent to recipient@example.com")

        success, message = app.send_notification(report, "High")

    mock_send_email.assert_called_once()
    called_kwargs = mock_send_email.call_args.kwargs
    assert called_kwargs["smtp_host"] == "smtp.gmail.com"
    assert called_kwargs["smtp_port"] == "587"
    assert called_kwargs["smtp_user"] == "user@example.com"
    assert called_kwargs["smtp_password"] == "app-password"
    assert called_kwargs["recipient"] == "recipient@example.com"
    assert success is True
    assert message == "Email sent to recipient@example.com"
