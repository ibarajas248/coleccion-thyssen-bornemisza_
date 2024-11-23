import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la página
url = 'https://www.artic.edu/collection'

# Realizar la solicitud HTTP
response = requests.get(url)
response.raise_for_status()  # Asegurarse de que la solicitud fue exitosa

# Analizar el contenido de la página
soup = BeautifulSoup(response.text, 'html.parser')

# Lista para almacenar los datos
data = []

# Encontrar todas las tarjetas de obras de arte
for li in soup.select('li.m-listing'):
    # Extraer los datos
    title = li.select_one('.title').get_text(strip=True) if li.select_one('.title') else None
    artist = li.select_one('.subtitle').get_text(strip=True) if li.select_one('.subtitle') else None
    year = li.select_one('a[data-gtm-0-start-year]').get('data-gtm-0-start-year') if li.select_one(
        'a[data-gtm-0-start-year]') else None
    url_artwork = li.select_one('a.m-listing__link').get('href') if li.select_one('a.m-listing__link') else None

    # Agregar los datos a la lista
    data.append({
        'Title': title,
        'Artist': artist,
        'Year': year,
        'Artwork URL': url_artwork
    })

# Crear un DataFrame de pandas
df = pd.DataFrame(data)

# Guardar el DataFrame en un archivo Excel
df.to_excel('artworks.xlsx', index=False)

print('Scraping completado. El archivo Excel ha sido generado como artworks.xlsx.')
