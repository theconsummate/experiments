from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import json

def send(subject, message, config_file_path = "config.json"):
    # load params
    params = json.load(open(config_file_path))

    # create message object instance
    msg = MIMEMultipart()

    # message = "Thank you"

    # setup the parameters of the message
    password = params["hlrs-password"]
    msg['From'] = params["hlrs-email"]
    if isinstance(params["gmail"], str):
        msg['To'] = params["gmail"]
    else:
        msg['To'] = ", ".join(params["gmail"])
    msg['Subject'] = subject

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    #create server
    server = smtplib.SMTP_SSL('mail.hlrs.de:465')

    # server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)


    # send the message via the server.
    server.sendmail(msg['From'], params['gmail'], msg.as_string())

    server.quit()

    print("successfully sent email to %s:" % (msg['To']))


if __name__ == '__main__':
    send("hello", "nice message", "config.json")
