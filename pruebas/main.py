import time
import win32print
import win32api

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

# Ejemplo de texto a imprimir
texto_a_imprimir = """\
Título: La noche estrellada
Autor: Vincent van Gogh
Fecha: 1889
Ubicación: Museo Thyssen
Técnica: Óleo sobre lienzo
Dimensiones: 73.7 cm × 92.1 cm

¡Este es un ejemplo de impresión desde Python!
"""

# Función para imprimir cada 30 minutos
def imprimir_periodicamente():
    while True:
        imprimir_documento(texto_a_imprimir)
        print("Esperando 30 minutos para la siguiente impresión...")
        time.sleep(60)  # Espera 30 minutos (30 minutos * 60 segundos)

# Llamar a la función para comenzar a imprimir cada 30 minutos
imprimir_periodicamente()
