from utils import send_email_smtp, send_email_sendgrid
import os

recipient = os.environ.get('RECIPIENT_EMAIL', 'f26202641@gmail.com')

# Test SMTP
try:
    send_email_smtp('Epoch Citizen SMTP verify', 'Test message from Epoch Citizen via SMTP.', recipient)
    print('SMTP: sent')
except Exception as e:
    print('SMTP failed:', repr(e))

# Test SendGrid API
try:
    res = send_email_sendgrid('Epoch Citizen SendGrid verify', 'Test message from Epoch Citizen via SendGrid API.', recipient)
    print('SendGrid status:', res[0])
except Exception as e:
    print('SendGrid failed:', repr(e))
