from db_connection import obtener_conexion


def validar_inicio_sesion(nombre_usuario, contrasena):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_usuario, rol
                FROM usuario
                WHERE nombre_usuario = %s AND clave = %s
                """,
                (nombre_usuario, contrasena),
            )
            return cursor.fetchone()


def obtener_roles_registrados():
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT DISTINCT UPPER(TRIM(rol))
                FROM usuario
                WHERE rol IS NOT NULL
                ORDER BY 1
                """
            )
            return [fila[0] for fila in cursor.fetchall()]
