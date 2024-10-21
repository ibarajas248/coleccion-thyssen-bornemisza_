import os
import requests
from bs4 import BeautifulSoup


# Función para descargar imágenes desde los enlaces
def download_image(image_url, image_name):
    try:
        # Obtener el contenido de la imagen
        img_data = requests.get(image_url).content

        # Crear un nombre de archivo para la imagen
        image_filename = f"imagenes/{image_name}.jpg"

        # Crear el directorio si no existe
        os.makedirs(os.path.dirname(image_filename), exist_ok=True)

        # Guardar la imagen
        with open(image_filename, 'wb') as img_file:
            img_file.write(img_data)

        print(f'Imagen descargada: {image_filename}')
    except Exception as e:
        print(f'Error al descargar la imagen: {e}')


# Función para raspar las imágenes de una página específica
def scrape_images_from_page(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Buscar todas las etiquetas <a> con la clase 'snippet__media'
        image_links = soup.find_all('a', class_='snippet__media js-snippet-link')

        for link in image_links:
            try:
                # Extraer la URL de la imagen desde el atributo 'srcset'
                img_tag = link.find('img', class_='snippet__img')
                if img_tag and 'srcset' in img_tag.attrs:
                    # Obtener la URL de mayor resolución (normalmente la última en 'srcset')
                    srcset = img_tag['srcset'].split(', ')
                    highest_res_url = srcset[-1].split(' ')[0]  # Obtener la primera parte antes del espacio (URL)

                    # Obtener el nombre del archivo basado en el 'alt' o el 'data-title'
                    image_name = img_tag['alt'] if 'alt' in img_tag.attrs else link['data-title']

                    # Descargar la imagen
                    download_image(highest_res_url, image_name)

            except Exception as e:
                print(f'Error al procesar la imagen: {e}')
    else:
        print(f'Error al realizar la solicitud: {response.status_code}')


# URL de ejemplo para raspar
url = 'https://www.museothyssen.org/buscador/tipo/obra?page=1'  # Puedes cambiar esta URL

# Llamar a la función para raspar las imágenes
scrape_images_from_page(url)
