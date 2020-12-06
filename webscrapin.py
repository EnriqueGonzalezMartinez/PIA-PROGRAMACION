import os
import re
import requests
import logging
from bs4 import BeautifulSoup as bs

def scraping(url):
    # Se lanza una peticion al sitio web y se saca su html
    try:
        req = requests.get(url)
        soup = bs(req.content, 'html.parser')
        # Expreciones para buscar informacion en las webs
        expreciones = [re.compile(r'[\w.-]+@[\w.-]+\.[a-zA-Z]{2,6}'), re.compile(r'facebook.com/\w*'), 
                    re.compile(r'twetter.com/\w*'), 
                    re.compile(r'\(\d{2}\)\d{4}-\d{4}|\(\d{2}\) \d{4} \d{4}|\(\d{2}\)\d{8}|\d{6}-\d{4}|\d{6} \d{4}')]
        dir = url[url.find('/w') + 1:url.rfind('/')]
        os.makedirs(dir, exist_ok=True)
        # Se crea el archivo data.txt
        with open(f'{dir}/data.txt','w+') as file:
            for exp in expreciones:
                # Se busca la informacion en el html de la web
                search = exp.findall(str(soup))
                for sh in search:
                    file.write(f'{sh}\n')
            print('The data file was data.txt')
        # Busca las etiquetas img con src
        images = soup.find_all('img', src=True)
        # Se crea una lista con los elementos de images que terminan con .jpg
        imag = [x['src'] for x in images if x['src'].endswith('.jpg')]
        for img in imag:
            # Posicion del ultimo '/' de la url
            lst = url.rfind('/')
            # Se asegura que la direccion de las imagenes a descargar este completa
            # de no ser asi la completa, despues descarga las imagenes
            if img.find(url[:lst]) == -1:
                img = url[:lst] + img
            # Se crea el nombre de la imagen
            last = img.rfind('/')
            img_name = img[last + 1:]
            with open(f'{dir}/'+ img_name,'wb') as file:
                try:
                    file.write(requests.get(img).content)
                    print('It is downloaded:'+ img_name)
                except Exception as e:
                    os.remove(f'{dir}/'+ img_name)
                    logg(e)
    except Exception as e:
        print('The URL is incorrect try again.')
        logg(e)


def logg(e):
    #cambiar el logger dependiendo del programa y se establece nivel 
    logger = logging.getLogger('WebScraping')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('debug.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    #se le asigna un formato
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.error(e)
