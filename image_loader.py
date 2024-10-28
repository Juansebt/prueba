# Este módulo se encargará de cargar y procesar imágenes.

import cv2

def cargar_imagen_ruta(ruta):
    """
    Función para cargar la imagen desde OpenCV y convertirla a RGB.
    
    Args:
        ruta (str): La ruta del archivo de la imagen que se desea cargar.

    Returns:
        numpy.ndarray: La imagen cargada en formato RGB como un arreglo de Numpy,
                       o None si no se pudo cargar la imagen.
    
    Raises:
        None: Esta función no lanza excepciones, pero imprimirá un mensaje de error
              si no se puede cargar la imagen.
    """
    imagen = cv2.imread(ruta)
    if imagen is None:
        print(f"Error: No se pudo cargar la imagen desde {ruta}")
        return None
    imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    return imagen
