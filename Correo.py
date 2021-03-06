import smtplib
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email import encoders

def email(user,pasw,to,subject,message,path):

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = to
    msg.attach(MIMEText(message, 'plain'))

    if path != None:
        x = path.rfind('/')
        if x >= 0:
            #nombre del archivo
            fileName= path[x+1:]
        else:
            fileName = path
        # agregar al cuerpo del mensaje

        if os.path.isfile(path):
            try:
                if fileName.endswith(".jpg") or fileName.endswith(".png"):
                     with open(path,'rb') as file:
                        image = MIMEImage(file.read())
                        image.add_header('Content-Disposition', f'attachment; filename = {fileName}' )
                        msg.attach(image)
                else:
                     # Abrimos el archivo que vamos a adjuntar
                     with open(path,'rb') as archivo_adjunto:
                        # Creamos un objeto MIME base
                        adjunto_MIME = MIMEBase('application', 'octet-stream')
                        # Y le cargamos el archivo adjunto
                        adjunto_MIME.set_payload((archivo_adjunto).read())
                        encoders.encode_base64(adjunto_MIME)
                        adjunto_MIME.add_header('Content-Disposition', f'attachment; filename = {fileName}')
                        msg.attach(adjunto_MIME)
            except Exception as e:
                print("Error attaching file")
                logg(e)
        else:
            print("Error attaching file or path invalid")

    # crear el servidor dependiendo del tipo de correo
    serv = check_Server(user)
    # Inicio de sesion para enviar el correo
    with smtplib.SMTP(serv) as server:
        try:
            server.starttls()
            server.login(msg['From'], pasw)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            print(f'Mail send to {msg["To"]} with succeed.')
        except Exception as e:
            print('The email or password is incorrect')
            logg(e)


def check_Server(user):
    x = user.find("@")
    y = user.rfind(".")
    serv = user[x+1:y]

    if serv == "gmail":
        server = 'smtp.gmail.com:587'
    elif serv == "hotmail" or serv == "live":
        server = 'smtp.office365.com:587'
    elif serv == "outlook":
        server = 'smtp-mail.outlook.com:587'
    elif serv == "yahoo":
        server = 'smtp.mail.yahoo.com:587'
    else:
         print("invalid mail")
         server = None
    return server

def logg(e):
    #cambiar el logger dependiendo del programa y se establece nivel 
    logger = logging.getLogger('Email')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('debug.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    #se le asigna un formato
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.error(e)
