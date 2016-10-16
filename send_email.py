import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from_email = 'test@gmail.com'
to_email = 'test@gmail.com'
msg = MIMEMultipart('alternative')
msg['From'] = 'test@gmail.com'
msg['To'] = 'test@gmail.com'
msg['Subject'] = 'A HTML EMAIL Test'

html = """
<html>
    <head></head>
    <body>
        <p>Hi</p><br>
        Hello world
    </body>
</html>
"""
part2 = MIMEText(html, 'html')
msg.attach(part2)

username = 'test@gmail.com'
password = 'passwd'
server = smtplib.SMTP_SSL('smtp.gmail.com:465')
server.login(username, password)
server.sendmail(from_email, to_email, msg.as_string())
server.quit()
