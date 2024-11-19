import requests
from PIL import Image as PILImage
from io import BytesIO
import matplotlib.pyplot as plt
import openai  # Si usas DALL·E, o la librería adecuada para Stable Diffusion

# Configura tu clave API (DALL·E o Stable Diffusion)
openai.api_key = 'tu_api_key_de_openai'

# Crear un único visualizador
fig, ax = plt.subplots(figsize=(12, 6))

# Función para mostrar la imagen
def show_image(image_url):
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

            # Llamar a la IA para generar una imagen nueva basada en la imagen cargada
            generate_ai_image(img)

        else:
            print("No se pudo cargar la imagen.")
    except Exception as e:
        print(f'Error al cargar la imagen: {e}')

# Función para generar una imagen modificada con IA
def generate_ai_image(original_img):
    # Guardar la imagen original en un archivo temporal
    original_img.save("original_image.jpg")

    # Usar la API de OpenAI (DALL·E) para generar una imagen relacionada (o usar otra API como Stable Diffusion)
    try:
        # Puedes subir la imagen a la API o darle la imagen como referencia
        response = openai.Image.create_variation(
            image=open("original_image.jpg", "rb"),  # Subir la imagen original
            n=1,  # Número de variaciones a generar
            size="1024x1024"  # Tamaño de la imagen generada
        )

        # Obtener la URL de la imagen generada
        generated_image_url = response['data'][0]['url']

        # Cargar y mostrar la imagen generada
        generated_img_response = requests.get(generated_image_url)
        if generated_img_response.status_code == 200:
            generated_img = PILImage.open(BytesIO(generated_img_response.content))

            # Mostrar la imagen generada
            ax.clear()  # Limpiar el eje antes de mostrar la nueva imagen generada
            ax.imshow(generated_img)
            ax.axis('off')  # Opcional: Ocultar los ejes
            plt.draw()  # Redibujar la imagen
            plt.pause(0.01)  # Pausa breve para actualizar la ventana de la imagen
        else:
            print("No se pudo generar la imagen.")
    except Exception as e:
        print(f'Error al generar la imagen con IA: {e}')

# Ejemplo de uso
image_url = "https://example.com/your-image-url.jpg"  # Aquí va la URL de la imagen
show_image(image_url)

# Mostrar el visualizador
plt.show()
