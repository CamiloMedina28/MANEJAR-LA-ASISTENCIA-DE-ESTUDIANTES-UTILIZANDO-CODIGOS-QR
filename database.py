import sqlite3
from os import remove
import os
from datetime import datetime
ruta = './base de datos/base_de_datos.db'
if os.path.isdir('./base de datos'):
    pass
else:
    os.mkdir('./base de datos')

def ver_fechas():
    try:
        conexion = sqlite3.connect(ruta)
        cursor = conexion.cursor()
    except: return 1
    else:
        datos = cursor.execute("PRAGMA table_info('estudiantes')").fetchall()
        lista = [x[1] for x in datos if x[1] != 'ID' and x[1] != 'NOMBRE' and x[1] != 'CURSO']
        return lista
    

def conexion_base_de_datos() -> str:
    """Conexión con la base de datos (base_de_datos.db)

    Returns:
        string: Si la conexión fue exitosa se indicqa al usuario que el proceso se logró.
    """
    conexion = sqlite3.connect(ruta)
    cursor = conexion.cursor()

    try:
        cursor.execute('''CREATE TABLE estudiantes(ID INTEGER PRIMARY KEY, NOMBRE VARCHAR(80) NOT NULL,CURSO INT NOT NULL)''')
        return "La base de datos fue creada exitosamente"
    except: return "La conexión con la base de datos fue exitosa"


def borrar_registro(id:int, directorio:str) -> int:
    """Borra registros de la base de datos. 

    Args:
        id (int): id de usuario
        directorio (str): directorio en donde están almacenados los códigos qr de los estudiantes.

    Returns:
        int: retorna uno en caso tal el programa no haya sido exitoso, en el caso contrario retorna un cero. 
    """
    try:
        remove(f'{directorio}/{id}.png')
    except: return 1
    try:
        conexion = sqlite3.connect(ruta)
        cursor = conexion.cursor()
    except: return 1
    else:
        try:
            cursor.execute(f"DELETE FROM estudiantes WHERE ID={id}")
            conexion.commit()
            return 0 
        except: return 1


def crear_registro(id:int, nombre:str, curso:int) -> int:
    """Crear un nuevo registro en la base de datos

    Args:
        id (int): id del estudiante
        nombre (str): nombre del estudiante
        curso (int): curso del estudiante

    Returns:
        int: 0 proceso logrado, 1 proceso fallido
    """
    try:
        conexion = sqlite3.connect(ruta)
        cursor = conexion.cursor()
    except: return 1
    else:
        try:
            datos = id,nombre,curso
            cursor.execute("INSERT INTO estudiantes(ID,NOMBRE,CURSO) VALUES (?,?,?)", (datos))
            conexion.commit()
            return 0
        except: return 1


def actualizar(id:int, nombre:str, curso:int) -> int:
    """Actualizar un registro en la base de datos.

    Args:
        id (int): id del estudiante
        nombre (str): nombre del estudiante
        curso (int): curso del estudiante

    Returns:
        int: 1 proceso fallido, 0 proceso logrado
    """
    try:
        conexion = sqlite3.connect(ruta)
        cursor = conexion.cursor()
    except: return 1
    else:
        try:
            datos = nombre,curso
            cursor.execute(f"UPDATE estudiantes SET NOMBRE=?, CURSO=? WHERE ID={id}", (datos))
            conexion.commit()
            return 0
        except: return 1
        
        
def consultar(id: int) -> int:
    """Consultar información del estudiantes inscrita en la base de datos usando el id.

    Args:
        id (int): id del estudiante

    Returns:
        int: 1 proceso fallido, 0 proceso logrado
    """
    try:
        conexion = sqlite3.connect(ruta)
        cursor = conexion.cursor()
    except: return 1
    else:
        try:
            datos = cursor.execute(f"SELECT ID,NOMBRE,CURSO FROM estudiantes WHERE ID={id}")
            for i in datos: return i
        except: return 1


def llamar_asistencia(id:int):
    """Desarrollar el llamado de asistencia tomando la fecha actual.

    Args:
        id (int): id dedl estudiante

    Returns:
        int: 1 proceso fallido, 0 proceso logrado
    """
    try: 
        conexion = sqlite3.connect(ruta)
        cursor = conexion.cursor()
    except: return 1
    else:
        now = datetime.now()
        nombre_de_la_columna = 'fecha_'+str(now.year)+"_"+str(now.month)+"_"+str(now.day)
        try:
            cursor.execute(f"ALTER TABLE estudiantes ADD {nombre_de_la_columna} INT DEFAULT 0")
        except: pass
        try:
            datos = cursor.execute(f"SELECT ID,NOMBRE,CURSO FROM estudiantes WHERE ID={id}")
        except: return 1
        else:
            nombre_de_la_columna += '=?'
            instruccion = f"UPDATE estudiantes SET {nombre_de_la_columna} WHERE ID={id}"
            cursor.execute(instruccion, (1,))
            conexion.commit()


def ver_asistencia(id:int):
    """Ver la asistencia de un estudiante utilizando el id - qr

    Args:
        id (int): Ingresar el id del estudiante.

    Returns:
        int: 1 proceso fallido, 0 proceso logrado
    """
    try: 
        conexion = sqlite3.connect(ruta)
        cursor = conexion.cursor()
    except: return 1
    else:
        lista = ver_fechas()
        if ver_fechas == 1:return 1
        else:
            registro = []
            try:
                for i in range(len(lista)): 
                    valor = cursor.execute(f"SELECT {lista[i]} FROM estudiantes WHERE ID={id}")
                    for x in valor:
                        x = str(x).strip('(),')
                        registro.append(x)
            except: return 1 
            else:
                diccionario_respuestas = {}
                for i,j in zip(lista,registro):
                    diccionario_respuestas[i] = j
                resultados_formateados = []
                for k,v in diccionario_respuestas.items():
                    string = f"Para la fecha {k} el estudiante {'no asistió' if v == '0' else 'asistió'}"
                    resultados_formateados.append(string)
                return resultados_formateados


def alterar_asistencia_segun_fecha(id:int, fecha:str):
    try: 
        conexion = sqlite3.connect(ruta)
        cursor = conexion.cursor()
    except: return 1
    else:
        valor = cursor.execute(f"SELECT {fecha} fROM estudiantes WHERE ID={id}")
        for i in valor: string = i
        string = str(string).strip('(),')
        if int(string) == 1: 
            value = 0
        elif int(string) == 0:
            value = 1
        cursor.execute(f"UPDATE estudiantes SET {fecha}=? WHERE ID={id}", (value,))
        conexion.commit()

