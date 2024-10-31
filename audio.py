# Este módulo se encargará de manejar la música y los efectos de sonido.

import pygame

def inicializar_audio(ruta_audio):
    """
    Inicializa el sistema de audio de Pygame y carga y reproduce una pista de audio en bucle.

    Args:
        ruta_audio (str): La ruta del archivo de audio que se desea cargar y reproducir.
                          Debe ser un archivo de formato compatible con Pygame (como .mp3 o .wav).
    """
    pygame.mixer.init()
    pygame.mixer.music.load(ruta_audio)
    pygame.mixer.music.play(-1) # Reproduce el audio en bucle
