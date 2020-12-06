import os
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
            ls = [path +'/'+ x for x in ls if x.endswith('.jpg') or x.endswith('.png')]
            # Se verifica que haya .jpg en la lista
            if (ls != []):
                for img in ls:   
                    metaImg(img)
            else:
                print('No se encontraron .jpg en la carpeta.')
        # Se comprueba que la path sea un archivo .jpg
        elif (os.path.isfile(path) and path.endswith('.jpg')):
            metaImg(path)
        else:
            print('La ruta no dirige a un archivo .jpg o es incorrecta.')

    elif (opc == '2'):
        if (os.path.isdir(path)):
            ls = os.listdir(path)
            ls = [path +'/'+ x for x in ls if x.endswith('.pdf')]
            if (ls != []):
                for pdf in ls:
                    metaPdf(pdf)
            else:
                print('No se encontro archivos .pdf en la carpeta.')
        elif(os.path.isfile(path) and path.endswith('.pdf')):
            metaPdf(path)
        else:
            print('La ruta no dirige a un archivo .pdf o es incorrecta.')
    else:
        print('Esa no es una opcion valida intente de nuevo.')


def metaImg(path):
    print(f"Sacando la metadata de la imagen: {path}")
    # Imagename recive el path de la imagen 
    imagename = path
    # Se lee la data de la imagen
    image = Image.open(imagename)
    # Con el metodo getexif() obtenemos la metadata de la imagen
    exifdata = image.getexif()
    # Se saca el nombre de la imagen
    lt = imagename.rfind('.')
    name = imagename[:lt] + '.txt'
    print(f'Se creo el archivo: {name}')
    with open(name,'w') as file:
        for tag_id in exifdata:
            # se consige el tag name
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            # decodifica bytes 
            if isinstance(data, bytes):
                data = data.decode()
            file.write(f"{tag}: {data}\n")


def metaPdf(path):
    print(f'Scando metadata del PDF: {path}')
    pdfFile = PdfFileReader(open(path,'rb'))
    info = pdfFile.getDocumentInfo()
    lt = path.rfind('.')
    name = path[:lt] + '.txt'
    with open(name,'w') as file:
        for meta in info:
            file.write(f'{meta:14} : {info[meta]}\n')

