import getpass
import os

import psycopg


def main():
    db_password = os.getenv("DB_PASSWORD")

    if not db_password:
        db_password = getpass.getpass("Password de PostgreSQL: ").strip()

    try:
        conexion = psycopg.connect(
            host="localhost",
            port="5432",
            dbname="proyecto_tarjeta_circulacion",
            user=os.getenv("DB_USER", "postgres"),
            password=db_password,
        )

        print("Conexion exitosa a la base de datos")

        cursor = conexion.cursor()
        cursor.execute("SELECT version();")

        resultado = cursor.fetchone()
        print("Version de PostgreSQL:", resultado[0])

        cursor.close()
        conexion.close()
        print("Conexion cerrada")

    except Exception as error:
        print("Error al conectar a la base de datos:", error)


if __name__ == "__main__":
    main()
