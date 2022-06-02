import random as rand
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from Google import Create_Service
import base64

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
    CLIENT_SECRET_FILE = '..\\res\\gmail\\client.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    send_email = 'ders.mailbot@gmail.com'
    recipients = []
    # test use:
    # '..\\res\\mail_info\\recipients_test.txt'
    list_path = '..\\res\\mail_info\\recipients.txt'
    with open(list_path,'r') as f:
        lines = f.readlines()
    for l in lines:
        recipients.append(l.strip())
    recipients = ', '.join(recipients)

    message = MIMEMultipart('alternative')
    message['Subject'] = 'Weekly Proverb'
    message['From'] = formataddr(('HillsideProverbs', send_email))
    message['To'] = send_email
    message['Bcc'] = recipients
    body = MIMEText(daily_saying, 'plain')
    html_string = formatEmail(daily_saying)
    formatting = MIMEText(html_string, 'html')

    message.attach(body)
    message.attach(formatting)
    raw_string = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message = service.users().messages().send(userId='me', body={'raw':raw_string}).execute()

def writeToFile(saying):
    path = '..\\res\\latest_proverb.txt'
    today = date.today()
    with open(path, 'w') as f:
        f.write('%s\t%s' % (
            today, saying
        ))

def main():
    daily_saying = chooseSaying()
    writeToFile(daily_saying)
    sendEmail(daily_saying)

if __name__ == '__main__':
    main()