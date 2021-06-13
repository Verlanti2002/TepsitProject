import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def send_mail(nome_dipendente):
    sender_email = "progettotepsitgiugno@gmail.com"
    password = "PaltrinieriVerlanti"

    receiver_email = ["paltrinieri.giacomo@einaudicorreggio.it.com", "verlanti.alessandro@einaudicorreggio.it"]

    message = MIMEMultipart("alternative")
    message["Subject"] = "Un dipendente è stato eliminato dal Database"
    message["From"] = sender_email
    message["To"] = ",".join(receiver_email)

    now = datetime.now()

    text = f"""Attenzione!\n\nIl dipendente {nome_dipendente} è stato eliminato dal database il giorno {now.strftime("%d/%m/%Y")} alle ore {now.strftime("%H:%M:%S")}"""

    part1 = MIMEText(text, "plain")
    message.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


if __name__ == '__main__':
    send_mail("")
