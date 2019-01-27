import smtplib
import codecs
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pyodbc
from os.path import basename
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from email.mime.application import MIMEApplication


#Default value population
ExchangeServer = "localhost"
DefaultEmail="semani@wsgc.com"

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)
from_user='semani@wsgc.com'
to_user='semani@wsgc.com'
filename = "data.csv"
attachment= open(filename, "rb")
msg = MIMEMultipart()
# send email
def sendEmail(subject,to_user, msg, from_user="pgodavarthi@wsgc.com"):
    '''message="""\
    Subject: %s
    %s
    """ %(from_user,to_user,subject,msg)
    '''
#filename = "data.csv"
#attachment= open(filename, "rb")

    msg = MIMEMultipart()
    message = MIMEMultipart('alternative')
    if from_user!='': 
        message['From'] = from_user
    else:
        message['From'] = DefaultEmail
    
    if to_user!='': 
        message['To'] = to_user
    else:
        message['To'] = DefaultEmail

    if subject!='': 
        message['Subject'] = subject
    else:
        message['Subject'] = "Python Script: <Unknown Message>"
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((open("data.csv", "rb")).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename=%s" % filename)

    msg.attach(part)
server = smtplib.SMTP(ExchangeServer)
server.sendmail(from_user,to_user,'Success!')
server.quit()
