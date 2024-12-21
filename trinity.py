from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# Definimos cuántas páginas queremos scrapear:
# Por ejemplo, de la página 1 a la 5
PAGES_TO_SCRAPE = range(1, 60)

# Lista para ir guardando todos los registros de todas las páginas
all_data = []

# Instancia el driver de Chrome (asegúrate de tener 'chromedriver' en tu PATH).
driver = webdriver.Chrome()

for page_number in PAGES_TO_SCRAPE:
    # Construimos la URL inyectando el número de página
    url = (
        "https://stella.catalogue.tcd.ie/iii/encore/plus/"
        f"C__Sart%20History__P{page_number}__Orightresult__U__X0"
        "?lang=eng&suite=cobalt"
    )
    print(f"Scrapeando la página: {url}")

    # Abre la página
    driver.get(url)
    # Espera unos segundos para que cargue completamente
    time.sleep(5)

    # Obtiene el HTML final (ya con JS ejecutado)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    # -------------------------------------------------------------------
    # Buscar cada "registro" en su contenedor.
    # Cada resultado está dentro de <div class="search-result-item searchResult">
    # -------------------------------------------------------------------
    all_records = soup.select('div.search-result-item.searchResult')
    print(f"  Registros encontrados en P{page_number}: {len(all_records)}")

    # Recorrer cada registro y extraer la información
    for record in all_records:
        # --- Título y URL ---
        title_elem = record.select_one("span.title a[id^='recordDisplayLink2Component_']")
        title_text = title_elem.get_text(strip=True) if title_elem else "N/D"
        title_href = title_elem.get('href') if title_elem else "N/D"

        # --- Autores ---
        author_elem = record.select_one("div.dpBibAuthor")
        authors = author_elem.get_text(strip=True) if author_elem else "N/D"

        # --- Categoría (ej: "Academic Journal") ---
        cat_elem = record.select_one("span.itemMediaType")
        category = cat_elem.get_text(strip=True) if cat_elem else "N/D"

        # --- Cita (Volumen, Páginas, etc.) ---
        citations_elem = record.select_one("span.citations")
        citations = citations_elem.get_text(strip=True) if citations_elem else "N/D"

        # --- Año (si existiera dentro de <span class='itemMediaYear'>) ---
        year_elem = record.select_one("span.itemMediaYear")
        year_text = year_elem.get_text(strip=True) if year_elem else "N/D"

        # --- Abstract resumido (miniAbstract) ---
        mini_abstract_elem = record.select_one("div.miniAbstract")
        mini_abstract = mini_abstract_elem.get_text(strip=True) if mini_abstract_elem else "N/D"

        # Agregar el registro a la lista general
        row = {
            "Título": title_text,
            "URL": title_href,
            "Autores": authors,
            "Categoría": category,
            "Citas": citations,
            "Año": year_text,
            "Abstract": mini_abstract
        }
        all_data.append(row)

# Cerrar el navegador al terminar
driver.quit()

# Crear un DataFrame con todos los registros y exportar a Excel
df = pd.DataFrame(all_data)
df.to_excel("art_history_all_pages.xlsx", index=False)

print("Se ha creado el archivo 'art_history_all_pages.xlsx' con los resultados de todas las páginas.")
