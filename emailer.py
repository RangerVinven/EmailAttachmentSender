import smtplib, os
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

user = "" #Your Gmail
password = "" #Your password
recipient = "" #Recipient
directory = "" #Directory with files eg "C:\Users\Daniel\Documents\folder\" (remember the \ at the end)

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(user, password)

eBooks = []

for file in [doc for doc in os.listdir(directory)]:
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = recipient
    msg['Subject'] = ""
    body = ""
    msg.attach(MIMEText(body, "plain"))
    try:
        file = "directory"+file
        attachment = open(file, "rb")
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename= "+file)
        msg.attach(part)
        text = msg.as_string()
        server.sendmail(user, recipient, text)
        attachment.close()
        file = file.replace(directory, "")
        print(file + " sent!")
    except:
        file = file.replace(directory, "")
        print(file + " failed to send!")
server.quit()
