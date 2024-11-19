from datetime import time

import requests
import win32api
import win32print
from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree
from IPython.display import Image, display
import requests
from PIL import Image as PILImage
from io import BytesIO
import time

from matplotlib import pyplot as plt

# Función para raspar los detalles adicionales de una obra
# Función para raspar los detalles adicionales de una obra
# Crear una figura para mostrar las imágenes
fig, ax = plt.subplots()
def scrape_additional_info(link):
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            # Convertir el árbol BeautifulSoup a un árbol lxml para usar XPath
            dom = etree.HTML(str(soup))

            # Buscar el div padre con id 'rs_artwork_description'
            parent_div = soup.find("div", id="rs_artwork_description")
            additional_text = "Información adicional no disponible"

            if parent_div:
                # Buscar dentro del padre el div hijo con clase 'u-mb@xs'
                child_div = parent_div.find("div", class_="u-mb@xs")
                if child_div:
                    additional_text = child_div.get_text(separator="\n").strip()

            # Localizar el tamaño usando XPath
            size_xpath = dom.xpath('//*[@id="main_content"]/div[2]/article/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div')
            size_text = "Tamaño no disponible"
            if size_xpath:
                # Obtener el texto del primer nodo encontrado
                size_text = size_xpath[0].text.strip()

            # Localizar la técnica usando XPath
            tecnica_xpath = dom.xpath('//*[@id="main_content"]/div[2]/article/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/text()')
            tecnica_text = "Técnica no disponible"
            if tecnica_xpath:
                # Obtener el texto del primer nodo encontrado
                tecnica_text = tecnica_xpath[0].strip()

            # Localizar la ubicación usando XPath
            ubicacion_xpath = dom.xpath('//*[@id="main_content"]/div[2]/article/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div')
            ubicacion_text = "Ubicación no disponible"
            if ubicacion_xpath:
                # Obtener el texto del primer nodo encontrado
                ubicacion_text = ubicacion_xpath[0].text.strip()

            # Buscar el div que contiene el enlace de la imagen en el atributo 'data-href'
            image_div = soup.find("div",
                                  class_="u-absolute u-inset-0 u-z-0 u-bg-gray-lightest u-static@print is-hidden js-zoom-map-viewer")
            image_url = "Imagen no disponible"
            if image_div:
                # Extraer el enlace de la imagen desde el atributo 'data-href'
                image_url = image_div.get("data-href", "Imagen no disponible")

            if image_url != "Imagen no disponible":
                try:
                    # Solicitar la imagen desde la URL
                    img_response = requests.get(image_url)
                    if img_response.status_code == 200:
                        img = PILImage.open(BytesIO(img_response.content))

                        # Mostrar la imagen en el mismo visualizador
                        ax.clear()  # Limpiar el eje antes de mostrar la nueva imagen
                        ax.imshow(img)
                        ax.axis('off')  # Opcional: Ocultar los ejes
                        plt.draw()  # Redibujar la imagen
                        plt.pause(0.01)  # Pausa breve para actualizar la ventana de la imagen

                    else:
                        print("No se pudo cargar la imagen.")
                except Exception as e:
                    print(f'Error al cargar la imagen: {e}')

            # Localizar el texto adicional utilizando XPath
            codigo_inventario = dom.xpath(
                '//*[@id="main_content"]/div[2]/article/div[1]/div[2]/div/div/div[2]/div[2]/div[3]')
            codigo_inventario_text = "Texto adicional no disponible"
            if codigo_inventario:
                # Concatenar todo el texto dentro del nodo encontrado
                codigo_inventario_text = " ".join([node.strip() for node in codigo_inventario[0].itertext()])

            # Localizar la sala usando XPath
            sala_xpath = dom.xpath(
                '//*[@id="main_content"]/div[2]/article/div[1]/div[2]/div/div/div[2]/div[2]/div[4]/a')
            sala_text = "Sala no disponible"
            if sala_xpath:
                # Obtener el texto o el enlace del nodo encontrado
                sala_text = sala_xpath[0].text.strip() if sala_xpath[0].text.strip() else sala_xpath[0].get("href",
                                                                                                            "Sala no disponible")


            return {
                "additional_info": additional_text,
                "size_info": size_text,
                "technique_info": tecnica_text,
                "ubicacion_info": ubicacion_text,  # Añadir ubicación aquí
                "image_url": image_url,
                "codigo_inventario_text":codigo_inventario_text,
                "sala_text":sala_text

            }

        except Exception as e:
            print(f'Error al obtener información adicional: {e}')
            return {
                "additional_info": "Error al obtener información adicional",
                "size_info": "Error",
                "technique_info": "Error",
                "ubicacion_info": "Error"  # Si ocurre un error, devolver "Error"
            }
    else:
        print(f'Error al solicitar el enlace {link}: {response.status_code}')
        return {
            "additional_info": "Error al solicitar información adicional",
            "size_info": "Error",
            "technique_info": "Error",
            "ubicacion_info": "Error"  # Si no se puede obtener la información, devolver "Error"
        }



def imprimir_documento(texto):
    """
    Imprime el texto dado en la impresora predeterminada.
    """
    try:
        # Obtener el nombre de la impresora predeterminada
        nombre_impresora = win32print.GetDefaultPrinter()
        print(f"Imprimiendo en la impresora: {nombre_impresora}")

        # Crear un archivo temporal con el contenido a imprimir
        archivo_temp = "documento_a_imprimir.txt"
        with open(archivo_temp, "w", encoding="utf-8") as archivo:
            archivo.write(texto)

        # Usar ShellExecute para enviar el archivo a la impresora
        win32api.ShellExecute(0, "print", archivo_temp, None, ".", 0)
        print("Impresión completada.")
    except Exception as e:
        print(f"Error al imprimir el documento: {e}")

# Función para raspar los datos de una sola página
def scrape_page(page_number):
    url = f'https://www.museothyssen.org/buscador/tipo/obra?page={page_number}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        snippets = soup.find_all('div', class_='snippet__body')
        data = []
        for snippet in snippets:
            try:
                # Obtener el enlace
                link = snippet.find('a', class_='snippet__caption js-snippet-link')['href']
                title = snippet.find('div', class_='snippet__title').get_text(strip=True)
                subtitle = snippet.find('div', class_='snippet__subtitle').get_text(strip=True)
                text = snippet.find('div', class_='snippet__text').get_text(strip=True)
                full_link = link

                # Hacer el segundo scraping para obtener la información adicional
                additional_data = scrape_additional_info(full_link)
                additional_info = additional_data["additional_info"]
                size_info = additional_data["size_info"]
                tecnica = additional_data["technique_info"]
                ubicacion = additional_data["ubicacion_info"]
                image_url = additional_data["image_url"]
                codigo_inventario= additional_data["codigo_inventario_text"]
                sala= additional_data["sala_text"]


                # Añadir los datos a la lista
                data.append({
                    'Autor': title,
                    'Título': subtitle,
                    'Fecha': text,
                    'Enlace': full_link,
                    'Información adicional': additional_info,
                    'Tamaño': size_info,
                    'tecnica': tecnica,
                    'ubicacion': ubicacion,
                    'image_url':image_url,
                    'codigo_inventario':codigo_inventario,
                    'sala':sala

                })

                print("----------------------------")
                print(title)
                print(subtitle)
                print(text)
                print(f'Información adicional: {additional_info}')
                print(f'Tamaño: {size_info}')
                print(f'tecnica: {tecnica}')
                print(f'ubicacion: {ubicacion}')
                print(f'image_url: {image_url}')
                print(f'codigo_inventario: {codigo_inventario}')
                print(f'sala: {sala}')
                print("----------------------------")

                texto_a_imprimir=title


                def imprimir_periodicamente():
                    while True:
                        imprimir_documento(texto_a_imprimir)

                time.sleep(60)



            except Exception as e:
                print(f'Error al procesar un snippet: {e}')

        return data
    else:
        print(f'Error al realizar la solicitud a la página {page_number}: {response.status_code}')

        return []


# Número total de páginas a raspar
total_pages = 1000  # Cambia este valor según el número de páginas que deseas raspar

# Lista para almacenar todos los datos
all_data = []

# Iterar sobre cada página
for page in range(1, total_pages + 1):
    print(f'Scrapeando la página: {page}')
    page_data = scrape_page(page)
    all_data.extend(page_data)  # Agregar los datos de la página actual a la lista general
    print('====================')

# Crear un DataFrame de pandas con los datos
df = pd.DataFrame(all_data)

# Guardar el DataFrame en un archivo Excel
df.to_excel('museo_obras_con_info_adicional.xlsx', index=False)

print('Archivo Excel creado con éxito.')
