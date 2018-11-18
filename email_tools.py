import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Emailer():

    def __init__(self, username, server, port=587, password=""):
        """Initalizes a emailer that uses smtp to send messages"""
        self.username = username
        self.server = server
        self.port = int(port)
        self.password = password
        self.mailer = smtplib.SMTP()

    def send_email(self, to, sender, subject, message,
                   content_type='text/plain'):
        msg = MIMEMultipart('alternative')
        msg['To'] = to
        msg['From'] = sender
        msg['Subject'] = subject
        content = MIMEText(message, 'html')
        msg.attach(content)
        self.mailer.connect(self.server, self.port)
        self.mailer.starttls()
        self.mailer.login(self.username, self.password)
        self.mailer.sendmail(sender, to, msg.as_string())
        self.mailer.quit()
