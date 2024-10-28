# Este es el archivo principal que ejecutará la aplicación.
# Importará los módulos necesarios y controlará el flujo del programa.

import pygame
import os
from image_loader import cargar_imagen_ruta
from pygame_ui import pedir_peso_pygame
from audio_handler import inicializar_audio

def main():
    """
    Función principal que coordina la ejecución de la interfaz gráfica para solicitar el peso del usuario 
    y mostrar una imagen animada si el peso es mayor a 100 kg.
    
    La función realiza los siguientes pasos:
    1. Solicita al usuario que ingrese su peso a través de una interfaz de Pygame.
    2. Si el peso ingresado es mayor a 100 kg, carga y muestra una imagen animada, 
       y reproduce un archivo de audio en bucle.
    3. Si el usuario cierra la ventana sin ingresar un peso, se muestra un mensaje en la consola.
    4. Si el peso es 100 kg o menos, se notifica al usuario con un mensaje en la consola.
    """
    # Pedir el peso llamando a la función del módulo pygame_ui
    peso = pedir_peso_pygame()
    if peso is None:
        print("Se cerró la ventana sin ingresar un peso.")
        return

    # Comprobar si el peso supera los 100 kg
    if peso > 100:
        ruta_imagen = 'media/pic.jpg'  # Cargar la imagen
        imagen = cargar_imagen_ruta(ruta_imagen)

        if imagen is None:
            return # Salir si no se pudo cargar la imagen

        # Convertir la imagen a formato compatible con Pygame
        imagen_pygame = pygame.surfarray.make_surface(imagen)
        
        ruta_audio = 'media/music.mp3'  # Ruta de tu archivo de audio
        inicializar_audio(ruta_audio)  #Se llama a la función para inicializar la reproducción del audio

        # Configurar la variable de entorno para centrar la ventana
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        # Crear una ventana de Pygame con las dimensiones de la imagen
        pantalla = pygame.display.set_mode((imagen.shape[1], imagen.shape[0]))
        pygame.display.set_caption("GORD@ DE MIERDA")

        # Bucle principal de Pygame
        ejecutando = True
        angulo = 0
        reloj = pygame.time.Clock() # Control de FPS

        # Variables para el efecto de zoom
        escala = 1.0
        incremento = 0.02 # Cambiar el tamaño de la imagen en cada fotograma
        max_escala = 1.2 # Escala máxima
        min_escala = 0.8 # Escala mínima
        creciendo = True # Indica si estamos acercando o alejando

        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                    # continue # Ignorar el evento de cierre de la ventana

            # Rotar la imagen
            imagen_rotada = pygame.transform.rotate(imagen_pygame, angulo)
            angulo += 1

            # Actualizar la escala para el efecto de zoom
            if creciendo:
                escala += incremento
                if escala >= max_escala:
                    creciendo = False
            else:
                escala -= incremento
                if escala <= min_escala:
                    creciendo = True

            # Escalar la imagen
            imagen_escala = pygame.transform.scale(imagen_rotada, (int(imagen_rotada.get_width() * escala), int(imagen_rotada.get_height() * escala)))
            
            # Centrar la imagen escalada en la pantalla
            rect = imagen_escala.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2))
            pantalla.fill((0, 0, 0))
            pantalla.blit(imagen_escala, rect)

            # Actualizar la pantalla
            pygame.display.flip()
            reloj.tick(60) # Limitar a 60 FPS

        pygame.quit()
    else:
        print("Tu peso no supera los 100 kg.")

if __name__ == "__main__":
    main()
