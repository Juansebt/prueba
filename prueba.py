import cv2
import pygame
import numpy as np

def cargar_imagen_ruta(ruta):
    # Cargar imagen usando OpenCV
    imagen = cv2.imread(ruta)
    if imagen is None:
        print(f"Error: No se pudo cargar la imagen desde {ruta}")
        return None
    # Convertir BGR (OpenCV) a RGB (Pygame)
    imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    return imagen

def main():
    # Inicializar Pygame
    pygame.init()

    # Pedir el peso al usuario
    try:
        peso = float(input("Ingrese su peso: "))
    except ValueError:
        print("Error: Por favor ingresa un número válido.")
        return

    # Comprobar si el peso supera los 100 kg
    if peso > 100:
        # Cargar la imagen
        ruta_imagen = 'pic.jpg'  # Reemplaza con la ruta de tu imagen
        imagen = cargar_imagen_ruta(ruta_imagen)

        if imagen is None:
            return  # Salir si no se pudo cargar la imagen

        # Convertir la imagen a formato compatible con Pygame
        imagen_pygame = pygame.surfarray.make_surface(imagen)

        # Crear una ventana de Pygame con las dimensiones de la imagen
        pantalla = pygame.display.set_mode((imagen.shape[1], imagen.shape[0]))

        # Bucle principal de Pygame
        ejecutando = True
        angulo = 0
        reloj = pygame.time.Clock()  # Control de FPS

        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False

            # Rotar la imagen
            imagen_rotada = pygame.transform.rotate(imagen_pygame, angulo)
            angulo += 1

            # Centrar la imagen en la pantalla
            rect = imagen_rotada.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2))
            pantalla.fill((0, 0, 0))  # Limpiar la pantalla antes de dibujar
            pantalla.blit(imagen_rotada, rect)

            # Actualizar la pantalla
            pygame.display.flip()

            # Limitar a 60 FPS
            reloj.tick(60)

        pygame.quit()
    else:
        print("Tu peso no supera los 100 kg.")

if __name__ == "__main__":
    main()
