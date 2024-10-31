# Este módulo manejará la interfaz de usuario de Pygame.

import numpy as np
import pygame
import cv2
from constants import *

def dibujar_boton_redondeado(pantalla, rect, color, texto, fuente):
    """
    Función para dibujar un botón con esquinas redondeadas
    
    Args:
        pantalla (pygame.Surface): La superficie de Pygame donde se dibujará el botón.
        rect (pygame.Rect): Un objeto Rect que define la posición y el tamaño del botón.
        color (tuple): Un color en formato RGB que determina el color del botón.
        texto (str): El texto que se mostrará en el botón.
        fuente (pygame.font.Font): Un objeto de fuente de Pygame utilizado para renderizar el texto.
    """
    # Dibujar el fondo del botón
    pygame.draw.rect(pantalla, color, rect, border_radius=7)
    texto_superficie = fuente.render(texto, True, COLOR_TEXTO)
    texto_rect = texto_superficie.get_rect(center=rect.center) # Centrar el texto en el botón
    pantalla.blit(texto_superficie, texto_rect) # Mostrar el texto centrado en el botón

def pedir_peso():
    """
    Función para mostrar una interfaz gráfica en Pygame para solicitar al usuario que ingrese su peso en kilogramos.

    Returns:
        float or None: El peso ingresado por el usuario en kilogramos si es válido, o None si se cierra la ventana.
    """
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Ingresar peso")

    fuente = pygame.font.Font(None, 50)
    fuente_indicacion = pygame.font.Font(None, 40)  # Fuente para la indicación
    fuente_boton = pygame.font.Font(None, 40)

    # Cuadro de texto y variables de entrada
    cuadro = pygame.Rect(50, 100, 300, 50)
    cuadro_color = COLOR_CUADRO
    texto = ''
    activo = True
    terminado = False
    peso = None
    
    # Definir botón de enviar
    boton = pygame.Rect(150, 180, 100, 50) # Posición y tamaño del botón

    while not terminado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Verificar si se hace clic en el cuadro de texto
                if cuadro.collidepoint(evento.pos):
                    activo = True
                    cuadro_color = COLOR_CUADRO_ACTIVO
                else:
                    activo = False
                    cuadro_color = COLOR_CUADRO
                # Verificar si se hace clic en el botón de enviar
                if boton.collidepoint(evento.pos):
                    try:
                        peso = float(texto)
                        terminado = True  # Terminar cuando se presiona el botón de enviar
                    except ValueError:
                        texto = '' # Limpiar si el texto no es un número válido

            if evento.type == pygame.KEYDOWN and activo:
                # Validar que solo se puedan ingresar números y un punto decimal
                if evento.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                else:
                    # Solo permitir dígitos o un único punto decimal
                    if evento.unicode.isdigit() or (evento.unicode == '.' and '.' not in texto):
                        texto += evento.unicode

        # Dibujar pantalla
        pantalla.fill(COLOR_FONDO)
        
        # Renderizar la indicación
        indicacion_superficie = fuente_indicacion.render("Ingrese su peso en KG:", True, COLOR_TEXTO)
        pantalla.blit(indicacion_superficie, (50, 30)) # Mostrar indicación arriba del campo de texto
        
        # Renderizar el texto actual en el cuadro de entrada
        texto_superficie = fuente.render(texto, True, COLOR_TEXTO)
        pantalla.blit(texto_superficie, (cuadro.x + 10, cuadro.y + 10))

        # Dibujar el cursor si el cuadro está activo
        if activo:
            # Posicionar el cursor después del texto ingresado
            cursor_x = cuadro.x + 10 + texto_superficie.get_width() + 5
            pygame.draw.rect(pantalla, COLOR_TEXTO, (cursor_x, cuadro.y + 10, 2, fuente.get_height() - 10))

        # Dibujar cuadro de texto
        pygame.draw.rect(pantalla, cuadro_color, cuadro, 2)
        
        # Detectar el estado del mouse
        mouse_pos = pygame.mouse.get_pos()
        boton_color = COLOR_BOTON_HOVER if boton.collidepoint(mouse_pos) else COLOR_BOTON_NORMAL # Cambiar color al pasar el mouse
        
        # Dibujar el botón de enviar con esquinas redondeadas
        dibujar_boton_redondeado(pantalla, boton, boton_color, "Enviar", fuente_boton)

        # Actualizar la pantalla
        pygame.display.flip()

    return peso

# Función para mostrar la ventana de carga
def mostrar_loading(pantalla, ruta_video):
    """
    Muestra una ventana de carga en Pygame utilizando un video como indicador de progreso.

    Args:
        pantalla (pygame.Surface): La superficie de Pygame donde se mostrará el video. Debe estar previamente inicializada.
        ruta_video (str): Ruta del archivo de video que se utilizará para la animación de carga.
    """
    # Usar OpenCV para capturar el video
    captura_video = cv2.VideoCapture(ruta_video)
    
    pygame.display.set_caption("Procesando datos...")
    
    if not captura_video.isOpened():
        print(f"No se pudo abrir el archivo de video: {ruta_video}")
        return
    
    while True:
        # Leer un frame del video
        ret, frame = captura_video.read()
        if not ret:
            break  # Salir si no hay más frames o falla la lectura
        
        # Invertir la imagen para corregir el sentido (opcional, dependiendo del video)
        frame = cv2.flip(frame, 1)

        # Convertir el frame a formato RGB para Pygame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pygame = pygame.surfarray.make_surface(np.rot90(frame_rgb))

        # Ajustar el tamaño del frame al tamaño de la ventana de carga
        frame_escalado = pygame.transform.scale(frame_pygame, (400, 250))

        # Dibujar el frame del video en la ventana
        pantalla.blit(frame_escalado, (0, 0))
        pygame.display.flip()

        # Procesar eventos para evitar que la ventana se congele
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                captura_video.release()
                pygame.quit()
                return

        # Añadir un pequeño retraso para simular la velocidad del video
        pygame.time.delay(10)

    captura_video.release()
    