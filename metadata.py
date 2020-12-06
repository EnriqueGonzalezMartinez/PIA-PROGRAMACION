import os
import logging
from PIL import Image
from PIL.ExifTags import TAGS
from PyPDF2 import PdfFileReader

def gettingMeta(path):
        # Se compurba que la path sea a una carpeta
        if (os.path.isdir(path)):
            # Se enlista el contenido de la carpeta
            ls = os.listdir(path)
            # Se pasa un filto para que solo queden los .jpg, .png o .pdf
            imgs = [path +'/'+ x for x in ls if x.endswith('.jpg') or x.endswith('.png')]
            pdfs = [path +'/'+ x for x in ls if x.endswith('.pdf')]
            # Se verifica que haya .jpg, .png o .pdf en las listas
            if (imgs != [] or pdfs != []):
                for img in imgs:   
                    metaImg(img)
                for pdf in pdfs:
                    metaPdf(pdf)
            else:
                print('No .pdf, .jpg, .png found in folder.')
        # Se comprueba que la path sea un archivo .jpg
        elif (os.path.isfile(path) and path.endswith('.jpg')):
            metaImg(path)
        elif (os.path.isfile(path) and path.endswith('.pdf')):
            metaPdf(path)
        else:
            print('The path does not point to a .pdf or .jpg or .png file.')


def metaImg(path):
    # Imagename recive el path de la imagen 
    imagename = path
    # Se lee la data de la imagen
    image = Image.open(imagename)
    # Con el metodo getexif() obtenemos la metadata de la imagen
    exifdata = image.getexif()
    # Se saca el nombre de la imagen
    lt = imagename.rfind('.')
    name = imagename[:lt] + '.txt'
    name1 = imagename[imagename.rfind('/'):]
    print(f"Getting the metadata of the image: {name1}")
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
    pdfFile = PdfFileReader(open(path,'rb'))
    info = pdfFile.getDocumentInfo()
    lt = path.rfind('.')
    name = path[:lt] + '.txt'
    name1 = path[path.rfind('/'):]
    print(f'Getting metadata from PDF: {name1}')
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
