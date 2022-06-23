from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
from smtplib import SMTP, SMTP_SSL
import ssl

from flaskr.config import SMTP_SERVER, SMTP_PORT, SMTP_USE_SSL, SMTP_SENDER_NAME, SMTP_SENDER_EMAIL, SMTP_USERNAME, SMTP_PASSWORD

def send_email(subject: str, message: str, to_addr: str):
    if to_addr is None or len(to_addr) == 0 or to_addr.isspace():
        raise ValueError("arg 'to_addr' is empty")

    msg = MIMEText(message, 'html')
    msg["Subject"] = subject
    msg['From'] = formataddr((str(Header(SMTP_SENDER_NAME, 'utf-8')), SMTP_SENDER_EMAIL))
    msg["To"] = to_addr

    if SMTP_USE_SSL:
        server = SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=ssl.create_default_context())
    else:
        server = SMTP(SMTP_SERVER, SMTP_PORT)
        if server.has_extn('STARTTLS'):
            server.starttls()

    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()
