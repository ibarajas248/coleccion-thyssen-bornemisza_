import requests
from bs4 import BeautifulSoup
import pandas as pd

# Función para raspar los datos de una sola página
def scrape_page(page_number):
    url = f'https://www.museothyssen.org/buscador/tipo/obra?page={page_number}'

    # Realizar la solicitud HTTP
    response = requests.get(url)

    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Crear objeto BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar todos los div con la clase 'snippet__body'
        snippets = soup.find_all('div', class_='snippet__body')

        # Lista para almacenar los datos
        data = []

        # Extraer información de cada snippet
        for snippet in snippets:
            try:
                # Encontrar el enlace
                link = snippet.find('a', class_='snippet__caption js-snippet-link')['href']
                title = snippet.find('div', class_='snippet__title').get_text(strip=True)
                subtitle = snippet.find('div', class_='snippet__subtitle').get_text(strip=True)
                text = snippet.find('div', class_='snippet__text').get_text(strip=True)

                # Añadir los datos a la lista
                data.append({
                    'Autor': title,
                    'Título': subtitle,
                    'Fecha': text,
                    'Enlace': f'https://www.museothyssen.org{link}'
                })
            except Exception as e:
                print(f'Error al procesar un snippet: {e}')
        return data
    else:
        print(f'Error al realizar la solicitud a la página {page_number}: {response.status_code}')
        return []

# Número total de páginas a raspar
total_pages = 5  # Cambia este valor según el número de páginas que deseas raspar

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
df.to_excel('museo_obras.xlsx', index=False)

print('Archivo Excel creado con éxito.')
