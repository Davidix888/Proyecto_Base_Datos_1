from db_connection import obtener_conexion


def obtener_marcas():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_marca, marca
                FROM marca
                ORDER BY marca
                """
            )
            return cursor.fetchall()


def obtener_modelos_por_marca(id_marca):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_modelo, modelo
                FROM modelo
                WHERE id_marca = %s
                ORDER BY modelo
                """,
                (id_marca,),
            )
            return cursor.fetchall()


def obtener_lineas_por_modelo(id_modelo):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_linea, linea
                FROM linea
                WHERE id_modelo = %s
                ORDER BY linea
                """,
                (id_modelo,),
            )
            return cursor.fetchall()


def obtener_colores():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_color, color
                FROM color
                ORDER BY color
                """
            )
            return cursor.fetchall()
