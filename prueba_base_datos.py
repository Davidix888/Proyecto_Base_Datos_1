import psycopg

# Conexión a la base de datos
try:
    conexion = psycopg.connect(
        host="localhost",
        port="5432",
        dbname="proyecto_tarjeta_circulacion",
        user="postgres",
        password="Cruzita_2005"
    )

    print("Conexión exitosa a la base de datos")

    cursor = conexion.cursor()
    cursor.execute("SELECT version();")

    resultado = cursor.fetchone()
    print("Versión de PostgreSQL:", resultado[0])

    cursor.close()
    conexion.close()
    print("Conexión cerrada")

except Exception as e:
    print("Error al conectar a la base de datos:", e)