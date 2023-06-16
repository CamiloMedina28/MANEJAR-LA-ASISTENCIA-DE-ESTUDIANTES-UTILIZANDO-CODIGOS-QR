import qrcode as qr
import cv2
from pyzbar.pyzbar import decode
import numpy as np


def crearqr(datos: tuple, dir:str):
    """Creación de códigos qr con la información ingresada por el usuario.

    Args:
        datos (tuple): Tupla con los datos para ingresar al código.
        dir (str): Directorio de almacenamiento del código qr.
    """
    try: 
        img = qr.make([datos[0],datos[1], datos[2]])
        with open(f'{dir}/{datos[0]}.png', 'wb') as imagen:
            img.save(imagen)
    except: return 1


def lectura_qr():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        for codes in decode(frame):
            info = codes.data.decode()
            return info
        cv2.imshow("LECTOR DE QR", frame)
        # Leemos teclado
        tecla = cv2.waitKey(5)
        if tecla == 27 or not cv2.getWindowProperty("LECTOR DE QR", cv2.WND_PROP_VISIBLE):
            break
    cv2.destroyAllWindows()
    cap.release()


def lectura_asistencia_qr(): 
    lista = []
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        for codes in decode(frame):
            info = codes.data.decode()
            matriz = np.array([codes.polygon], np.int32)  
            cv2.polylines(frame, [matriz], True, (244,208,63),5)
            lista.append(info)
        cv2.imshow("LECTOR DE QR", frame)
        # Leemos teclado
        tecla = cv2.waitKey(5)
        if tecla == 27 or not cv2.getWindowProperty("LECTOR DE QR", cv2.WND_PROP_VISIBLE):
            break
    cv2.destroyAllWindows()
    cap.release()
    return lista
