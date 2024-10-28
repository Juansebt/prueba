import cv2
import pygame
import numpy as np

# Función para cargar la imagen desde OpenCV y convertirla a RGB
def cargar_imagen_ruta(ruta):
    imagen = cv2.imread(ruta)
    if imagen is None:
        print(f"Error: No se pudo cargar la imagen desde {ruta}")
        return None
    imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    return imagen

# Función para mostrar un cuadro de entrada en Pygame para obtener el peso del usuario
def pedir_peso_pygame():
    pygame.init()
    pantalla = pygame.display.set_mode((400, 200))
    pygame.display.set_caption("Ingrese su peso")

    # Definir fuente y colores
    fuente = pygame.font.Font(None, 50)
    fuente_indicacion = pygame.font.Font(None, 40)  # Fuente para la indicación
    color_texto = (255, 255, 255)
    color_fondo = (0, 0, 0)
    color_cuadro = (200, 200, 200)
    color_cuadro_activo = (255, 255, 255)

    # Cuadro de texto y variables de entrada
    cuadro = pygame.Rect(50, 100, 300, 50)
    cuadro_color = color_cuadro
    texto = ''
    activo = True
    terminado = False
    peso = None

    while not terminado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None

            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Activar el cuadro de texto si el usuario hace clic en él
                if cuadro.collidepoint(evento.pos):
                    activo = True
                    cuadro_color = color_cuadro_activo
                else:
                    activo = False
                    cuadro_color = color_cuadro

            if evento.type == pygame.KEYDOWN:
                if activo:
                    if evento.key == pygame.K_RETURN:
                        try:
                            peso = float(texto)
                            terminado = True  # Terminar cuando se ingrese el peso
                        except ValueError:
                            texto = ''  # Limpiar si el texto no es un número válido
                    elif evento.key == pygame.K_BACKSPACE:
                        texto = texto[:-1]
                    else:
                        texto += evento.unicode

        # Dibujar pantalla
        pantalla.fill(color_fondo)

        # Renderizar la indicación
        indicacion_superficie = fuente_indicacion.render("Ingrese su peso:", True, color_texto)
        pantalla.blit(indicacion_superficie, (50, 30))  # Mostrar indicación arriba del campo de texto

        # Renderizar el texto actual en el cuadro de entrada
        texto_superficie = fuente.render(texto, True, color_texto)
        pantalla.blit(texto_superficie, (cuadro.x + 10, cuadro.y + 10))

        # Dibujar el cursor si el cuadro está activo
        if activo:
            # Posicionar el cursor después del texto ingresado
            cursor_x = cuadro.x + 10 + texto_superficie.get_width() + 5
            pygame.draw.rect(pantalla, color_texto, (cursor_x, cuadro.y + 10, 2, fuente.get_height() - 10))

        # Dibujar cuadro de texto
        pygame.draw.rect(pantalla, cuadro_color, cuadro, 2)

        # Actualizar la pantalla
        pygame.display.flip()

    return peso

# Función principal
def main():
    # Pedir el peso usando una pantalla Pygame
    peso = pedir_peso_pygame()
    if peso is None:
        print("Se cerró la ventana sin ingresar un peso.")
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
