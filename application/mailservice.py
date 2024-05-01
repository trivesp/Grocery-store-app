from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = "localhost"
SMTP_PORT = 1025
SENDER_EMAIL = 'trivedhansivaprakash@gmail.com'
SENDER_PASSWORD = 'kavithasivaprakash'


def send_message(to, subject, content_body):
    msg = MIMEMultipart()
    msg["To"] = "21f1001724@ds.study.iitm.ac.in"
    msg["Subject"] = 'TEST'
    msg["From"] = 'trivedhansivaprakash@gmail.com'
    msg.attach(MIMEText(content_body, 'html'))
    client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
    client.send_message(msg=msg)
    client.quit()