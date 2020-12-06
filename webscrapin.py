import os
import re
import requests
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
        os.makedirs(url, exist_ok=True)
        # Se crea el archivo data.txt
        with open(url+'/data.txt','w+') as file:
            for exp in expreciones:
                # Se busca la informacion en el html de la web
                search = exp.findall(str(soup))
                for sh in search:
                    file.write(f'{sh}\n')
            print('Se creo el archivo data.txt')
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
            with open('Scraping/'+ img_name,'wb') as file:
                try:
                    file.write(requests.get(img).content)
                    print('Se descargo:'+ img_name)
                except:
                    os.remove('Scraping/'+ img_name)
    except:
        print('La URL es incorrecta intente de nuevo.')



    