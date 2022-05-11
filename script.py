import smtplib
import ssl
from datetime import datetime
from getpass import getpass

smtpServer = "smtp.gmail.com"
sslPort = 465
tlsPort = 587
context = ssl.create_default_context()
server = None


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
        while menuRes != '2':
            menuRes = input("""\
1 ==> Send an email.
2 ==> Quit.

response <== """)
            match menuRes:
                case '1':
                    receiverEmail = input("\nRecipient :")
                    subject = input("Subject :")
                    message = f"""\
From: {senderEmail}
To: {receiverEmail}
Subject: {subject}
Date: {datetime.now().strftime( "%d/%m/%Y %H:%M" )}

{input('Message: ')}\n"""
                    server.sendmail(senderEmail, receiverEmail, message)
                    print("\nYour message has been sent successfully.\n")
                case '2':
                    pass
                case _:
                    print("\nplease choose either 1 or 2.\n")
        print("\nQuiting.")
    except Exception as e:
        print(e)
    finally:
        if not server:
            server.quit()
