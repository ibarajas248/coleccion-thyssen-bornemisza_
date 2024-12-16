import requests
from bs4 import BeautifulSoup
import pandas as pd


# URL de la página
url_base = 'https://www.artic.edu/collection?page={}'



# Lista para almacenar los datos
data = []
for page in range(1, 200):
    url = url_base.format(page)
    response = requests.get(url)
    response.raise_for_status()  # Asegurarse de que la solicitud fue exitosa

    # Analizar el contenido de la página
    soup = BeautifulSoup(response.text, 'html.parser')


# Encontrar todas las tarjetas de obras de arte
    for li in soup.select('li.m-listing'):
        # Extraer los datos
        title = li.select_one('.title').get_text(strip=True) if li.select_one('.title') else None
        artist = li.select_one('.subtitle').get_text(strip=True) if li.select_one('.subtitle') else None
        year = li.select_one('a[data-gtm-0-start-year]').get('data-gtm-0-start-year') if li.select_one(
            'a[data-gtm-0-start-year]') else None
        url_artwork = li.select_one('a.m-listing__link').get('href') if li.select_one('a.m-listing__link') else None

        # Inicializar la descripción
        description = None
        medium = None
        # Acceder a la página de detalle de la obra de arte si existe una URL
        if url_artwork:
            detail_url = url_artwork  # Completar la URL relativa
            try:
                detail_response = requests.get(detail_url)
                detail_response.raise_for_status()
                detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

                # Extraer la descripción
                try:
                    description_div = detail_soup.select_one('div.o-blocks[itemprop="description"]')
                    if description_div:
                        description = ' '.join(p.get_text(strip=True) for p in description_div.find_all('p'))
                    else:
                        # Buscar en el otro contenedor si no se encuentra la primera descripción
                        article_body_div = detail_soup.select_one('div.o-article__body.o-blocks[itemprop="articleBody"]')
                        if article_body_div:
                            paragraphs = article_body_div.find_all('p', limit=2)  # Extraer los dos primeros <p>
                            description = ' '.join(p.get_text(strip=True) for p in paragraphs)

                        else:
                            description = None  # No se encontró ninguna descripción
                except:
                    pass


                #extraer medio

                try:
                    # Buscar el elemento <dd> con itemprop="material" y su <span> hijo
                    material_span = detail_soup.select_one('dd[itemprop="material"] span.f-secondary')
                    if material_span:
                        # Extraer el texto limpio del <span>
                        material = material_span.get_text(strip=True)
                    else:
                        material = None
                except Exception as e:
                    print(f"Error al extraer el material: {e}")
                    material = None

                try:
                    # Buscar el elemento <dd> con itemprop="size" y su <span> hijo
                    size_span = detail_soup.select_one('dd[itemprop="size"] span.f-secondary')
                    if size_span:
                        # Extraer el texto limpio del <span>
                        size = size_span.get_text(strip=True)
                    else:
                        size = None
                except Exception as e:
                    print(f"Error al extraer el tamaño: {e}")
                    size = None

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0 Safari/537.36"
                }

                try:



                    # Extraer el contenido del panel "Exhibition History"
                    exhibition_history_panel = detail_soup.select_one('#panel_exhibition-history')
                    if exhibition_history_panel:
                        history_text = exhibition_history_panel.get_text(strip=True)
                        print("Exhibition History:")
                        print(history_text)

                except requests.exceptions.RequestException as e:
                    print(f"Error al hacer la petición: {e}")







            except requests.RequestException as e:
                print(f'Error al acceder a {detail_url}: {e}')

        # Agregar los datos a la lista
        data.append({
            'Title': title,
            'Artist': artist,
            'Year': year,
            'Artwork URL': url_artwork,
            'Description': description,
            'Medium': material,
            'size': size,
            'Exhibition History': history_text

        })




# Crear un DataFrame de pandas
df = pd.DataFrame(data)

# Guardar el DataFrame en un archivo Excel
df.to_excel('artworks.xlsx', index=False)

print('Scraping completado. El archivo Excel ha sido generado como artworks.xlsx.')
