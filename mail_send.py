import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imaplib
import time
import sqlite3
from base import messages

conn = sqlite3.connect('mail.db')
cursor = conn.cursor()
cursor.execute(f'SELECT email, number FROM "mail_table"')
data = cursor.fetchall()
mail = [row[0] for row in data]
number = [row[1] for row in data]
conn.close()

fromaddr = " "  # почта
secpass = " "  # пароль, получаемый в mail.ru

for email, numb in zip(mail, number):
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = email
    msg['Subject'] = "Тема сообщения"

    body = messages[numb]
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    server.login(fromaddr, secpass)
    text = msg.as_string()
    server.sendmail(fromaddr, email, text)
    server.quit()

    imap_server = imaplib.IMAP4_SSL('imap.mail.ru')
    imap_server.login(fromaddr, secpass)
    imap_server.select('Send')  # Сохранение письма в папку Send
    imap_server.append('Send', '', imaplib.Time2Internaldate(time.time()), text.encode('UTF-8'))
    imap_server.logout()
