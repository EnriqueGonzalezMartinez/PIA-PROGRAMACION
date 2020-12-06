import argparse
from Correo import email
from encrypt import maincrypt
from hash_files import hashValuer
from metadata import gettingMeta
from nmap_scan import chooseScan
from SMS import sendSMS
from webscrapin import scraping
from API_Shodan import API

parser = argparse.ArgumentParser(description="Options of parameter tool:\n0 is for webscrpaing\n"+
                                '1 is for send SMS\n2 is for scan webs or ips\n'+
                                '3 is for getting metadata of images or PDF\n'+
                                '4 is for getting values HASH of files\n'+
                                '5 is for encrypt or decrypt files\n6 is for send email\n'+
                                '7 is for look for possibly vulnerable hosts\n')
# Argumentos que se utilizan en todos los programas
parser.add_argument("-tool", type=int, help="tool that you want use of alls", required=True)
parser.add_argument("-path", type=str, help="absolute path of the file or directory")
# Argumentos de Correo
parser.add_argument("-user", type=str, help="Mail you're going to use to send the email")
parser.add_argument("-pasw", type=str, help="Password of the email you're going to use")
parser.add_argument("-to", type=str, help="Recipient's mail")
parser.add_argument("-subject", type=str, help="Email subject")
parser.add_argument("-message", type=str, help="Email message")
# Argumentos de encrypt
parser.add_argument("-key", type=str, help="path of key")
parser.add_argument("-opc", type=str, help="generate key (yes or no)")
parser.add_argument("-opc2", type=str, help="encrypt or decrypt")
# Argumentos de hash_files es la path que ya esta declarada arriba
# Argumentos de metadata es la path que ya esta declarada
# Argumentos de nmap_scan
parser.add_argument("-target", type=str, help="ip or web")
parser.add_argument("-range", type=str, help="scan range")
# Argumentos de web_scraping
parser.add_argument("-url", type=str, help="website url")
# Argumentos de SMS
parser.add_argument("-SID", type=str, help="account SID (twilio)")
parser.add_argument("-Token", type=str, help="auth TOKEN (twilio)")
parser.add_argument("-sender", type=str, help="sender number (twilio)")
parser.add_argument("-reciver", type=str, help="reciver number")
parser.add_argument("-text", type=str, help="text to be sent")
# Argumentos de API_Shodan
parser.add_argument("-apiKey", type=str, help="API KEY of Shodan")
parser.add_argument("-port", type=str, help="port to scan")
params = parser.parse_args()

if __name__ == "__main__":
    if (params.tool == 0):
        scraping(params.url)
    elif (params.tool == 1):
        sendSMS(params.SID,params.Token,params.sender,params.reciver,params.text)
    elif (params.tool == 2):
        chooseScan(params.target, params.range)
    elif (params.tool == 3):
        gettingMeta(params.path)
    elif (params.tool == 4):
        hashValuer(params.path)
    elif (params.tool == 5):
        maincrypt(params.path,params.key,params.opc,params.opc2)
    elif (params.tool == 6):
        email(params.user, params.pasw, params.to, params.subject, params.message)
    elif (params.tool == 7):
        API(params.apiKey, params.port)
    else:
        print('Option invalid.')