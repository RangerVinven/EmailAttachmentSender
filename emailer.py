import argparse
import smtplib, os
import json
from os.path import expanduser
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

parser = argparse.ArgumentParser()
parser.add_argument("-u","--user",help="Set the email account to be used eg example@gmail.com")
parser.add_argument("-p","--password",help="The password for the user email")
parser.add_argument("-r","--recipient",help="Target email address to send attachments")
parser.add_argument("-d","--dir",help="Directory of files")
parser.add_argument("-b","--body",help="Body of the email(s) defaults to nothing")
parser.add_argument("-s","--subject",help="The Subject of the email(s) defaults to nothing")
parser.add_argument("-c","--clear",help="Removes stored data",action="store_true")
args = parser.parse_args()

if args.clear:
    fp = expanduser("~")+"/.emailer"
    if os.path.exists(fp):
      os.remove(fp)
    exit()


if(args.user and args.password and args.recipient and args.dir):
    user = args.user
    password = args.password
    recipient = args.recipient
    directory = args.dir

else:
    home = expanduser("~")+"/" # gets home path (cross platform)
    try:
        f = open(home+".emailer","r")
        data = json.load(f)
        user = data["USER"]
        recipient = data["RECIP"]
        directory = data["DIR"]
        password = input("Password for {}:".format(user))
    except IOError:
        # First time automatic setup
        print("No past account was detected setting one up now:")
        user = input("Email (eg example@google.com):")
        recipient = input("Recipients email address:")
        directory = input("Directory where files are stored:")
        password = input("Password for {}:".format(user))
        with open(home+".emailer", "w") as outfile: 
            data ={"USER":user,"RECIP":recipient,"DIR":directory}
            json.dump(data,outfile)

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
        file = directory+file
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
