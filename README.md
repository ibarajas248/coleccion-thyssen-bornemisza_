# Proyecto de Web Scraping de Obras de la Colección del Museo Thyssen-Bornemisza

## Descripción del Proyecto

El objetivo de este proyecto es llevar a cabo un proceso de web scraping para recopilar información detallada sobre las obras de la colección del Museo Thyssen-Bornemisza, que se encuentra en Madrid, España. Este museo es conocido por su rica y variada colección de arte, que abarca desde el Renacimiento hasta el siglo XX, incluyendo obras de maestros como Van Gogh, Monet y Rembrandt.

La recopilación de datos a través de técnicas de scraping permitirá crear una base de datos estructurada que facilitará la consulta, análisis y visualización de la información relacionada con cada obra. Este proyecto tiene como finalidad proporcionar a investigadores, estudiantes, historiadores del arte y entusiastas del arte una herramienta accesible y funcional para explorar la vasta colección del museo, promoviendo así la apreciación y el estudio del patrimonio artístico.


![image](https://github.com/user-attachments/assets/54d90901-4765-452d-8c16-024e8910109c)

### Justificación

El acceso a información sobre obras de arte puede ser limitado o poco estructurado en muchos casos. A través de este proyecto, se busca mitigar este problema al crear una base de datos que no solo recolecte información, sino que también la presente de manera organizada y fácilmente accesible. Además, esta base de datos permitirá realizar análisis estadísticos, identificar patrones en la colección y facilitar estudios comparativos entre diferentes obras y autores.

### Objetivos Específicos

1. **Extracción de Datos:** Desarrollar un script en Python que scrapee las páginas web del museo para extraer información clave sobre cada obra de arte, como el título, autor, año de creación, técnica, dimensiones, imagen, y una breve descripción.
   
2. **Estructuración de Datos:** Organizar los datos extraídos en un formato estructurado y almacenarlos en una base de datos relacional, como SQLite o MySQL. Esto facilitará las consultas y el análisis posterior.

3. **Interfaz de Consulta:** Crear una interfaz de usuario sencilla que permita a los usuarios consultar y explorar la base de datos de manera interactiva, facilitando la búsqueda de información específica sobre las obras.

4. **Documentación y Recursos:** Producir documentación detallada que explique el proceso de scraping, la estructura de la base de datos y cómo utilizar la interfaz de consulta, asegurando que otros puedan replicar el proyecto o extenderlo en el futuro.

### Metodología

1. **Definición del Alcance:**
   - Identificar las páginas del museo que contienen información sobre las obras de la colección.
   - Definir los campos a extraer y cómo se relacionan entre sí.

2. **Tecnologías Utilizadas:**
   - **Python**: Lenguaje de programación para realizar el scraping.
   - **BeautifulSoup**: Biblioteca para analizar y manipular documentos HTML y XML.
   - **Requests**: Para realizar solicitudes HTTP.
   - **Pandas**: Para la manipulación de datos y creación de DataFrames.
   - **SQLite/MySQL**: Para el almacenamiento de datos estructurados en una base de datos.

3. **Proceso de Scraping:**
   - Enviar solicitudes a las páginas de la colección del museo y analizar el contenido HTML para extraer la información relevante.
   - Descargar las imágenes de cada obra y almacenarlas en un directorio específico.

4. **Estructura de la Base de Datos:**
   - Crear una tabla que almacene información sobre cada obra con columnas como:
     - `id`: Identificador único de la obra.
     - `titulo`: Título de la obra.
     - `autor`: Autor de la obra.
     - `anio`: Año de creación.
     - `tecnica`: Técnica utilizada.
     - `dimensiones`: Dimensiones de la obra.
     - `descripcion`: Descripción breve de la obra.
     - `imagen_url`: URL de la imagen de la obra.

5. **Generación de Reportes:**
   - Crear un archivo Excel con la información estructurada.
   - Generar visualizaciones o reportes basados en la colección, como gráficos que representen la distribución de obras por autor o período.

### Consideraciones Éticas y Legales

Es fundamental tener en cuenta las implicaciones éticas y legales del web scraping. Se debe respetar los términos de uso del sitio web del museo y asegurarse de que el proceso de scraping no afecte negativamente su funcionamiento. Además, se debe prestar especial atención a los derechos de autor relacionados con las imágenes y descripciones de las obras.

### Impacto del Proyecto

Este proyecto no solo facilitará el acceso a la información sobre las obras de arte del Museo Thyssen-Bornemisza, sino que también servirá como un recurso educativo y cultural valioso. Al hacer que la información esté disponible de manera estructurada y accesible, se espera fomentar el interés y la investigación en el campo del arte, promoviendo la conservación y apreciación del patrimonio cultural.
