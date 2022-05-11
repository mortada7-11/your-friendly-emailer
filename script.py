import csv
import smtplib
import ssl
from datetime import datetime
from getpass import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtpServer = "smtp.gmail.com"
sslPort = 465
tlsPort = 587
context = ssl.create_default_context()
server = None


def textMessage(subj: str, sender: str, receiver: str, innerMessage: str):
    return f"""\
From: {sender}
To: {receiver}
Subject: {subj}
Date: {datetime.now().strftime("%d/%m/%Y %H:%M")}

{innerMessage}\n"""


def htmlMessage(subj: str, sender: str, receiver: str, text: str, htmlPath: str):
    innerMessage = MIMEMultipart("alternative")
    innerMessage["Subject"] = subj
    innerMessage["From"] = sender
    innerMessage["To"] = receiver
    innerMessage["Date"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    innerMessage.attach(MIMEText(f"\n{text}", "plain"))
    with open(htmlPath) as file:
        innerMessage.attach(MIMEText(file.read(), "html"))
    return innerMessage.as_string()


def sslMode():
    return smtplib.SMTP_SSL(smtpServer, sslPort, context=context)


def tlsMode():
    innerServer = smtplib.SMTP(smtpServer, tlsPort)
    innerServer.ehlo()
    innerServer.starttls(context=context)
    innerServer.ehlo()
    return innerServer


if __name__ == '__main__':
    try:
        menuRes = '0'
        # server = sslMode()
        server = tlsMode()
        logRes = None
        senderEmail = ""
        while not logRes:
            senderEmail = input("Email :")
            password = getpass("Password :")
            try:
                logRes = server.login(senderEmail, password)
            except Exception as e:
                print("\nUsername and Password does not match.\n")
        print("\nLogged in successfully.\n")
        while menuRes != '3':
            menuRes = input("""\
1 ==> Send an email.
2 ==> Send multiple emails.
3 ==> Quit.

response <== """)
            match menuRes:
                case '1':
                    receiverEmail = input("\nRecipient :")
                    subject = input("Subject :")
                    # message = textMessage(subject, senderEmail, receiverEmail, input("Message :"))
                    message = htmlMessage(subject, senderEmail, receiverEmail, input("Message :"), input("HTML path :"))
                    server.sendmail(senderEmail, receiverEmail, message)
                    print("\nYour message has been sent successfully.\n")
                case '2':
                    subject = input("Subject :")
                    # message = textMessage(input("Message :"))
                    message = input("Message :")
                    html = input("HTML :")
                    with open(input("CSV path :")) as f:
                        reader = csv.reader(f)
                        next(reader)
                        for email, fullName in reader:
                            print(f"\nSending email to {fullName}.")
                            server.sendmail(senderEmail, email, htmlMessage(subject, senderEmail, email, message, html))
                    print("\nAll emails has been sent successfully.\n")
                case '3':
                    pass
                case _:
                    print("\nplease choose either 1 or 2.\n")
        print("\nQuiting.")
    except Exception as e:
        print(e)
    finally:
        if not server:
            server.quit()
