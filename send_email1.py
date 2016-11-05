import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from time import gmtime, strftime
import time
from dateutil.relativedelta import relativedelta
import datetime

def send(str):
    from_email = 'your_gmail.com'
    to_email = 'your_gmail.com'
    msg = MIMEMultipart('alternative')
    msg['From'] = 'your_gmail.com'
    msg['To'] = 'your_gmail.com'
    msg['Subject'] = 'Status Update'

    html = " <html> <head></head> <body> <p>Hi</p><br> {} </body> </html>".format(str)
    part2 = MIMEText(html, 'html')
    msg.attach(part2)

    username = 'your_gmail.com'
    password = 'your_app_password'
    server = smtplib.SMTP_SSL('smtp.gmail.com:465')
    try:
        server.login(username, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
    except Exception:
        print("send mail exception!")
        return
#send("ahloha")
