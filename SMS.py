from twilio.rest import Client
import logging

def sendSMS(accountSID,authToken,sender,recipient,text):
    try:
        if accountSID != None or authToken != None or text != None:
              twilioCli = Client(accountSID,authToken)
              #ingresar numero de Twilio
              senderNumber = sender
              #Al destinatario se le agrega +52
              recipientNumber = f"+52{recipient}"
              #Texto que desea enviar
              msg = text
        else:
             print("Error sending message")
             exit()

        
        message = twilioCli.messages.create(to = recipientNumber,
                                                from_ = senderNumber,
                                                body = msg)
        print("message sent successfully")
    except Exception as e:
        print("Error sending message")
        logg(e)


def logg(e):
    #cambiar el logger dependiendo del programa y se establece nivel 
    logger = logging.getLogger('Send SMS')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('debug.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    #se le asigna un formato
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.error(e)
