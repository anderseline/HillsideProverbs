import random as rand
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

def chooseSaying():
    path = '..\\res\\sayings_list.txt'
    f = open(path, 'r')
    lines = f.readlines()
    lim = len(lines)
    ind = rand.randrange(0, lim)
    sayings = []
    for l in lines:
        sayings.append(l)
    sayings_cleaned = []
    for s in sayings:
        sayings_cleaned.append(
            s.replace('\n', '')
        )
    saying = sayings_cleaned[ind]
    return saying

def formatEmail(daily_saying):
    path = '..\\res\\mail_info\\formatting.html'
    return open(path).read().format(
        daily_saying = daily_saying
    )

def sendEmail(daily_saying):
    port = 465
    acct_path = '..\\res\\mail_info\\account_info.txt'
    with open(acct_path, 'r') as f:
        lines = f.readlines()
        send_email = lines[0]
        password = lines[1]
    recipients = []
    recipients_path = '..\\res\\mail_info\\recipients.txt'
    with open(recipients_path, 'r') as f:
        lines = f.readlines()
        for l in lines:
            recipients.append(l)
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Weekly Proverb'
    message['From'] = formataddr(('Hillside Proverbs', send_email))
    message['To'] = ', '.join(recipients)
    message['Bcc'] = ''

    body = MIMEText(daily_saying, 'plain')
    html_string = formatEmail(daily_saying)

    formatting = MIMEText(html_string, 'html')

    message.attach(body)
    message.attach(formatting)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(send_email, password)
        server.sendmail(
            send_email, recipients, message.as_string()
        )

def main():
    daily_saying = chooseSaying()
    sendEmail(daily_saying)

if __name__ == '__main__':
    main()