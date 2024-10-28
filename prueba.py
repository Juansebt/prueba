import cv2
import pygame
import numpy as np

# Inicializar Pygame
pygame.init()

# Pedir el peso al usuario
peso = float(input("Ingrese su peso: "))

# Comprobar si el peso supera los 100 kg
if peso > 100:
    # Cargar la imagen
    imagen = cv2.imread('pic.jpg')  # Reemplaza 'tu_imagen.jpg' con la ruta de tu imagen

    # Convertir la imagen a formato compatible con Pygame
    imagen_pygame = pygame.surfarray.make_surface(imagen)

    # Crear una ventana de Pygame
    pantalla = pygame.display.set_mode((imagen.shape[1], imagen.shape[0]))

    # Bucle principal de Pygame
    ejecutando = True
    angulo = 0
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        # Rotar la imagen
        imagen_rotada = pygame.transform.rotate(imagen_pygame, angulo)
        angulo += 1

        # Centrar la imagen en la pantalla
        rect = imagen_rotada.get_rect(center=(pantalla.get_width()//2, pantalla.get_height()//2))
        pantalla.blit(imagen_rotada, rect)

        pygame.display.flip()

    pygame.quit()
else:
    print("Tu peso no supera los 100 kg.")