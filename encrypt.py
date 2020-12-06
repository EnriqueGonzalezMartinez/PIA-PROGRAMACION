from cryptography.fernet import Fernet
import os
from datetime import datetime
#parser = argparse.ArgumentParser()
#parser.add_argument("-archivo", type=str, help="url del sitio web", required=True)
#parser.add_argument("-mensaje", type=str, help="url del sitio web", required=True)
#parser.add_argument("-clave", type=str, help="url del sitio web")
#parser.add_argument("-path", type=str, help="url del sitio web", required=True)
#parser.add_argument("-opc", type=str, help="url del sitio web", required=True)
#parser.add_argument("-opc2", type=str, help="url del sitio web", required=True)
#params = parser.parse_args()
nombre = ''

def main(path,clave,opc,opc2):
    pwd = os.getcwd().replace('\\','/')
    if path == pwd:
        print('It is not possible to encrypt or decrypt the folder in which the script runs.')
        exit()
    op = [desencriptar,encriptar]
    if opc == 'yes' and clave == None and opc2 == 'encriptar':
        generar_clave()
        clave = leer_clave(nombre)
    elif opc == 'no':
        try:
            clave = leer_clave(clave)
        except:
            print('Invalid key or A key was not entered.')
            exit()
    else:
        print('Invalid option.')
        exit()
    if opc2 == 'desencriptar':
        index = 0
    elif opc2 == 'encriptar':
        index = 1
    else:
        print('Invalid option.')
        exit()
    if os.path.isfile(path):
        try:
            op[index](path,clave)
            if index == 0:
                print(f'The file {path} was decrypted.')
            elif index == 1:
                print(f'The file {path} was crypted.')
        except:
             print(f'the file could not be encrypted or desencrypted: {path}')
    elif os.path.isdir(path):
        ls = os.listdir(path)
        ls = [path+'/'+x for x in ls]
        for file in ls:
            try:
                op[index](file,clave)
                if index == 0:
                    print(f'The file {file} was decrypted.')
                elif index == 1:
                    print(f'The file {file} was crypted.')
            except:
                print(f'the file could not be encrypted or desencrypted: {file}')
    else:
        print('The path is invalid.')
    

def generar_clave():
    global nombre
    clave = Fernet.generate_key()
    name = str(datetime.now())
    name = name[:name.rfind('.')]
    name = name.replace(':','-')
    nombre = f'clave({name}).key'
    with open(nombre, "wb") as archivo_clave:
        archivo_clave.write(clave)

def leer_clave(path):
   return open(path,"rb").read()


def encriptar(path,clave):
    f = Fernet(clave)
    with open(path, "rb") as file:
        data_file = file.read()
    data_encrypted = f.encrypt(data_file)
    with open(path,'wb') as file:
        file.write(data_encrypted)


def desencriptar(path,clave):
    f = Fernet(clave)
    with open(path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(path,'wb') as file:
        file.write(decrypted_data)
