import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart

from flask import Flask


class MailClient:
    def __init__(self, app: Flask = None):
        self.host = None
        self.port = None
        self.username = None
        self.password = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.host = app.config['SMTP_HOST']
        self.port = app.config['SMTP_PORT']
        self.username = app.config['SMTP_USERNAME']
        self.password = app.config['SMTP_PASSWORD']

    def send(self, to: str, subject: str, content: MIMENonMultipart):
        msg = MIMEMultipart('alternative')
        msg['subject'] = subject
        msg.attach(content)
        with smtplib.SMTP_SSL(self.host, self.port) as s:
            s.login(self.username, self.password)
            s.sendmail(self.username, to, msg.as_string())


mailer = MailClient()
