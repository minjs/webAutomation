import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Emailer():

    smtpserver = 'smtp.gmail.com'
    sender = "busydwmonkey@gmail.com"

    def __init__(self, smtpServer=None):
        if smtpServer is not None:
            self.smtpserver = smtpServer

    def send_email(self, deals, receiver):
        try:
            msg = MIMEMultipart()
            msg['Subject'] = 'Latest deals'
            msg['From'] = self.sender
            msg['To'] = ", ".join(receiver)

            text = str(deals)

            part1 = MIMEText(text, 'plain')
            #part2 = MIMEText(html, 'html')

            msg.attach(part1)
            #s = smtplib.SMTP('localhost', 1025)
            server = smtplib.SMTP(self.smtpserver, 587) #port 465 or 587
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login('busydwmonkey@gmail.com', 'Mei750810@monkey')
            server.sendmail(self.sender, receiver, msg.as_string())
            server.close()
        except Exception as e:
            logging.error("send email exception", e)


