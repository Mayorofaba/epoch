"""SendGrid API example matching the official snippet.

Reads `SENDGRID_API_KEY` from the environment or `.streamlit/secrets.toml`.
Replace recipient/from as needed. Do NOT commit your API key.
"""
import os
from pathlib import Path

try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
except Exception:
    raise RuntimeError("sendgrid package not installed. Run `pip install sendgrid`.")


def _read_key_from_secrets():
    path = Path(__file__).parent / '.streamlit' / 'secrets.toml'
    if not path.exists():
        return None
    for line in path.read_text(encoding='utf-8').splitlines():
        if 'SENDGRID_API_KEY' in line and '=' in line:
            parts = line.split('=', 1)
            if len(parts) == 2:
                val = parts[1].strip().strip('"').strip("'")
                return val
    return None


def send_test():
    api_key = os.environ.get('SENDGRID_API_KEY') or _read_key_from_secrets()
    if not api_key:
        print('SENDGRID_API_KEY not set in environment or .streamlit/secrets.toml')
        return

    from_email = os.environ.get('SMTP_USER', 'from_email@example.com')
    to_email = os.environ.get('RECIPIENT_EMAIL', 'to@example.com')

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>'
    )

    try:
        sg = SendGridAPIClient(api_key)
        # sg.set_sendgrid_data_residency("eu")  # uncomment for EU subuser
        response = sg.send(message)
        print(response.status_code)
        try:
            print(response.body)
        except Exception:
            pass
        print(response.headers)
    except Exception as e:
        print('Send failed:', e)


if __name__ == '__main__':
    send_test()
