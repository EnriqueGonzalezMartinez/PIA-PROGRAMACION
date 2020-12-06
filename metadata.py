import os
import logging
from PIL import Image
from PIL.ExifTags import TAGS
from PyPDF2 import PdfFileReader

def sacandoMeta(opc, path):
    # La primera opcion es para saber si se sacara metadata
    # de una imagen o un pedf
    if (opc == '1'):
        # Se compurba que la path sea a una carpeta
        if (os.path.isdir(path)):
            # Se enlista el contenido de la carpeta
            ls = os.listdir(path)
            # Se pasa un filto para que solo queden los .jpg
            ls = [path +'/'+ x for x in ls if x.endswith('.jpg')]
            # Se verifica que haya .jpg en la lista
            if (ls != []):
                for img in ls:   
                    metaImg(img)
            else:
                print('No .jpg found in folder.')
        # Se comprueba que la path sea un archivo .jpg
        elif (os.path.isfile(path) and path.endswith('.jpg')):
            metaImg(path)
        else:
            print('The path does not point to a .jpg file or is incorrect.')

    elif (opc == '2'):
        if (os.path.isdir(path)):
            ls = os.listdir(path)
            ls = [path +'/'+ x for x in ls if x.endswith('.pdf')]
            if (ls != []):
                for pdf in ls:
                    metaPdf(pdf)
            else:
                print('No .pdf files found in the folder.')
        elif(os.path.isfile(path) and path.endswith('.pdf')):
            metaPdf(path)
        else:
            print('The path does not point to a .pdf file or is incorrect.')
    else:
        print('That is not a valid option, try again

.')


def metaImg(path):
    print(f"Getting the metadata of the image: {path}")
    # Imagename recive el path de la imagen 
    imagename = path
    # Se lee la data de la imagen
    image = Image.open(imagename)
    # Con el metodo getexif() obtenemos la metadata de la imagen
    exifdata = image.getexif()
    # Se saca el nombre de la imagen
    lt = imagename.rfind('.')
    name = imagename[:lt] + '.txt'
    print(f'The file was created: {name}')
    try:
        with open(name,'w') as file:
            for tag_id in exifdata:
                # se consige el tag name
                tag = TAGS.get(tag_id, tag_id)
                data = exifdata.get(tag_id)
                # decodifica bytes 
                if isinstance(data, bytes):
                    data = data.decode()
                file.write(f"{tag}: {data}\n")
    except Exception as e:
        print("Error getting metadata")
        logg(e)


def metaPdf(path):
    print(f'Getting metadata from PDF: {path}')
    pdfFile = PdfFileReader(open(path,'rb'))
    info = pdfFile.getDocumentInfo()
    lt = path.rfind('.')
    name = path[:lt] + '.txt'
    try:
        with open(name,'w') as file:
            for meta in info:
                file.write(f'{meta:14} : {info[meta]}\n')
    except Exception as e:
        print("Error getting metadata")
        logg(e)

def logg(e):
    #cambiar el logger dependiendo del programa y se establece nivel 
    logger = logging.getLogger('Metadata')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('debug.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    #se le asigna un formato
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.error(e)


sacandoMeta('2',"PIA-PROGRAMACION-main")
