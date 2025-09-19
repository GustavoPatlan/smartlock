from dotenv import load_dotenv
from pathlib import Path
import mysql.connector, os

# Carga las variables del archivo .env
dotenv_path = Path('secret/.env')
load_dotenv(dotenv_path=dotenv_path)

def conexion():
    conn = mysql.connector.connect(
        host = os.getenv("DBHOST"),
        user = os.getenv("DBUSER"),
        password = os.getenv("DBPASSWORD"),
        database = os.getenv("DBDATABASE")
    )
    return conn

# Usuarios
def encontrar_usuario(correo):
    conn=conexion()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE CORREO = %s", (correo,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def asignar_locker(codigo, casillero, correo):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET LOCKER = %s, " \
                                        "CODIGO = %s, " \
                                        "CNOMBRE = %s, " \
                                        "ZONA = %s, " \
                                        "CIUDAD = %s, " \
                                        "ESTADO = %s " \
                   "WHERE CORREO = %s", (casillero[1], codigo, casillero[2], casillero[3], casillero[4], casillero[5], correo))
    cursor.execute(f"UPDATE casilleros SET DISPONIBILIDAD = 'OCUPADO' WHERE IDE = '{casillero[0]}'")
    conn.commit()
    cursor.close()
    conn.close()

def actualizar_llave_usuario(correo, key):
    conn=conexion()
    cursor=conn.cursor()
    cursor.execute("UPDATE usuarios SET LLAVE = %s WHERE CORREO = %s", (key, correo))
    conn.commit()
    cursor.close()
    conn.close()

def agregar_usuario(correo, nombre, apellido, key):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (CORREO, NOMBRES, APELLIDOS, LLAVE) VALUES (%s, %s, %s, %s)",
                   (correo, nombre, apellido, key))
    conn.commit()
    cursor.close()
    conn.close()

def actualizar_usuario(correo_nuevo, nombre, apellido, correo):
    conn=conexion()
    cursor=conn.cursor()
    cursor.execute("UPDATE usuarios SET CORREO = %s, NOMBRES = %s, APELLIDOS = %s WHERE CORREO = %s",
                   (correo_nuevo, nombre, apellido, correo))
    conn.commit()
    cursor.close()
    conn.close()

def eliminar_usuario(correo):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE CORREO = %s", (correo,))
    conn.commit()
    cursor.close()
    conn.close()

# Casilleros
def encontrar_locker():
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM casilleros WHERE DISPONIBILIDAD = 'LIBRE'")
    resultado = cursor.fetchone()
    cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado

def encontrar_locker_abrir(correo):
    conn=conexion()
    cursor=conn.cursor()
    cursor.execute("SELECT LOCKER, CNOMBRE, ZONA, CIUDAD, ESTADO FROM usuarios WHERE CORREO = %s", (correo,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def encontrar_locker_pantalla(codigo, info):
    conn=conexion()
    cursor=conn.cursor()
    cursor.execute("SELECT LOCKER FROM usuarios WHERE CODIGO = %s AND " \
                                                      "CNOMBRE = %s AND " \
                                                      "ZONA = %s AND " \
                                                      "CIUDAD = %s AND " \
                                                      "ESTADO = %s",
                    (codigo, info[0], info[1], info[2], info[3],))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def encontrar_locker_correo(correo, info):
    conn=conexion()
    cursor=conn.cursor()
    cursor.execute("SELECT CORREO FROM usuarios WHERE LOCKER = %s AND " \
                                                      "CNOMBRE = %s AND " \
                                                      "ZONA = %s AND " \
                                                      "CIUDAD = %s AND " \
                                                      "ESTADO = %s",
                    (correo, info[0], info[1], info[2], info[3],))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def liberar_locker(correo, info):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET LOCKER = 'SIN ASIGNAR', " \
                                        "CODIGO = 'SIN ASIGNAR', " \
                                        "CNOMBRE = 'SIN ASIGNAR', " \
                                        "ZONA = 'SIN ASIGNAR', " \
                                        "CIUDAD = 'SIN ASIGNAR', " \
                                        "ESTADO = 'SIN ASIGNAR' " \
                   f"WHERE CORREO = '{correo}'")
    cursor.execute(f"UPDATE casilleros SET DISPONIBILIDAD = 'LIBRE' WHERE LOCKER = %s AND " \
                                                                          "CNOMBRE = %s AND " \
                                                                          "ZONA = %s AND " \
                                                                          "CIUDAD = %s AND " \
                                                                          "ESTADO = %s", (info[0], info[1], info[2], info[3], info[4],))
    conn.commit()
    cursor.close()
    conn.close()

# Historial
def agregar_solicitud(correo, horario, espacio, info):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO registros (CORREO, HORA, FECHA, ESPACIO, CASILLERO, UBICACION) VALUES (%s, %s, %s, %s, %s, %s)",
                   (correo, horario[0], horario[1], espacio, info[0], info[2]+','+info[3]))
    conn.commit()
    cursor.close()
    conn.close()

def encontrar_solicitud(correo):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registros WHERE CORREO = %s ORDER BY FECHA ASC, HORA ASC", (correo,))
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado