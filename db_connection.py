import psycopg


DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "dbname": "proyecto_tarjeta_circulacion",
    "user": "postgres",
    "password": "Cruzita_2005",
}


def obtener_conexion():
    return psycopg.connect(**DB_CONFIG)
