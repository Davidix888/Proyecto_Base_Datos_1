import getpass
import os

import psycopg


DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "dbname": "proyecto_tarjeta_circulacion",
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}


def obtener_conexion():
    return psycopg.connect(**DB_CONFIG)


def validar_login(nombre_usuario, contrasena):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_usuario, rol
                FROM usuario
                WHERE nombre_usuario = %s AND "contraseÑa" = %s
                """,
                (nombre_usuario, contrasena),
            )
            return cursor.fetchone()


def main():
    if not DB_CONFIG["password"]:
        DB_CONFIG["password"] = getpass.getpass("Password de PostgreSQL: ").strip()

    nombre_usuario = input("Usuario del sistema: ").strip()
    contrasena = getpass.getpass("Contrasena del sistema: ").strip()

    try:
        usuario = validar_login(nombre_usuario, contrasena)
    except psycopg.Error as error:
        print(f"Error al consultar la base de datos: {error}")
        return

    if usuario:
        id_usuario, rol = usuario
        print("Login correcto")
        print(f"ID de usuario: {id_usuario}")
        print(f"Rol: {rol}")
    else:
        print("Usuario o contrasena incorrectos")


if __name__ == "__main__":
    main()
