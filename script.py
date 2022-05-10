import smtplib
import ssl
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
    senderEmail = input("Email :")
    password = getpass("Password :")
    try:
        menuRes = '0'
        while menuRes != '2':
            server = sslMode()
            server.login(senderEmail, password)
            print("Logged in successfully.")
            menuRes = input("""\
1 ==> Send an email.
2 ==> Quit.
""")
            match menuRes:
                case '1':
                    receiverEmail = input("Recipient :")
                    subject = input("Subject :")
                    message = f"""\
Subject :{subject}
                    
{input('Message :')}
"""
                    server.sendmail(senderEmail, receiverEmail, message)
                    print("Your message has been sent successfully.")

                case _:
                    menuRes = input("please choose either 1 or 2.\n\n")
        print("Quiting.")
    except Exception as e:
        print(e)
    finally:
        if not server:
            server.quit()
