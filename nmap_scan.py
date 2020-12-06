import nmap
import socket
import logging
from datetime import datetime

def ipValid(target):
    try:
        socket.inet_aton(target)
        return True
    except:
        return False

def webValid(target):
    index = target.find('https://')
    target = target[index + 1:]
    try:
        socket.gethostbyname_ex(target)
        return True
    except:
        return False
        

def chooseScan(target, rango):
    rango = str(rango)
    if rango != None and len(rango) >= 3 and ipValid(target) and rango.find('-') != -1:
       try:
            index = rango.find('-')
            begin = int(rango[:index])
            end = int(rango[index + 1:])
            if begin > end:
                print('Invalid range or attribute set is incorrect.')
                exit()
       except Exception as e:
            logg(e)
            print('Invalid range or attribute set is incorrect.')
            exit()
    elif rango == None and ipValid(target) and rango != '':
        begin, end = 0, 0
        j = target.rfind('.')
        target = target[0:j] +"0/24"
    elif rango == None and webValid(target) and rango != '':
        index = target.find('https://')
        target = target[index + 1:]
        begin, end = 0, 0
    else:
        print('Invalid range or attribute set is incorrect.')
        exit()

    scanner(target,begin,end)

def scanner(target,begin,end):
    scanner = nmap.PortScanner()

    if begin < end:
        nombre = f'Ip scanning({datetime.now()}).txt'
        with open(r"Scan.txt", "w+") as raw:
            for i in range(begin,end+1):
                res = scanner.scan(target,str(i))
                res = res["scan"][target]["tcp"][i]["state"]
                if res != "closed":
                   raw.write("port "+str(i)+" is "+str(res)+"\n")
                   
    else:
        scanner.scan(target)
        nombre = f'Web scanning({datetime.now()}).txt'
        with open(r"Scan.txt", "w+") as raw:
            for host in scanner.all_hosts():
                raw.write("----------------------------------------------------\n")
                raw.write("Host : %s (%s)" % (host, scanner[host].hostname())+ "\n")
                for proto in scanner[host].all_protocols():
                    lport = scanner[host][proto].keys()
                    try:
                        lport.sort()
                    except:
                        pass
                    for port in lport:
                        raw.write('port : %s\tstate : %s' % (port, scanner[host][proto][port]['state'])+"\n")

def logg(e):
    #cambiar el logger dependiendo del programa y se establece nivel 
    logger = logging.getLogger('Scan Nmap')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('debug.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    #se le asigna un formato
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.error(e)

