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
    index = target.find('//')
    ind = target.rfind('/')
    if index + 1 != ind:
        target = target[index + 2:ind]
    else:
        target = target[index + 2:]
    try:
        socket.gethostbyname_ex(target)
        return True
    except:
        return False
        

def chooseScan(target, rango):
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
    elif rango == None and ipValid(target):
        begin, end = 0, 0
        j = target.rfind('.')
        target = target[:j] +".0/24"
    elif rango == None and webValid(target):
        index = target.find('//')
        ind = target.rfind('/')
        if index + 1 != ind:
            target = target[index + 2:ind]
        else:
            target = target[index + 2:]
        begin, end = 0, 0
    else:
        print('Invalid range or attribute set is incorrect.')
        exit()

    scanner(target,begin,end)
    print('Scan Finished.')


def scanner(target,begin,end):
    scanner = nmap.PortScanner()
    if begin < end:
        date = str(datetime.now()).replace(':','-')
        p = date.find('.')
        nombre = f'Web scanning({date[:p]}).txt'
        print('Scanning...')
        with open(nombre, "w+") as raw:
            for i in range(begin,end+1):
                res = scanner.scan(target,str(i))
                res = res["scan"][target]["tcp"][i]["state"]
                if res != "closed":
                   raw.write("port "+str(i)+" is "+str(res)+"\n")
                   
    else:
        print('Scanning...')
        scanner.scan(target)
        date = str(datetime.now()).replace(':','-')
        p = date.find('.')
        nombre = f'Web scanning({date[:p]}).txt'
        with open(nombre, "w+") as raw:
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
