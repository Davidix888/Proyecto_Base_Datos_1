import psycopg

from db_connection import obtener_conexion


def registrar_propietario(cui, nit, nombre):
    cui = cui.strip()
    nit = nit.strip().upper()
    nombre = " ".join(nombre.strip().split())

    if not cui or not nit or not nombre:
        return False, "Todos los campos del propietario son obligatorios."

    if not cui.isdigit() or len(cui) != 13:
        return False, "El CUI debe tener exactamente 13 digitos."

    if len(nit) < 7:
        return False, "El NIT debe tener al menos 7 caracteres."

    if len(nit) > 13:
        return False, "El NIT no puede tener mas de 13 caracteres."

    if len(nombre) > 100:
        return False, "El nombre no puede tener mas de 100 caracteres."

    try:
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM propietario WHERE cui = %s",
                    (cui,),
                )
                if cursor.fetchone():
                    return False, "Ya existe un propietario registrado con ese CUI."

                cursor.execute(
                    "SELECT 1 FROM propietario WHERE UPPER(TRIM(nit)) = %s",
                    (nit,),
                )
                if cursor.fetchone():
                    return False, "Ya existe un propietario registrado con ese NIT."

                cursor.execute(
                    """
                    INSERT INTO propietario (cui, nit, nombre)
                    VALUES (%s, %s, %s)
                    """,
                    (cui, nit, nombre),
                )
        return True, "Propietario registrado correctamente."
    except psycopg.errors.UniqueViolation:
        return False, "Ya existe un propietario registrado con ese CUI o NIT."
    except psycopg.Error as error:
        return False, f"No fue posible registrar el propietario: {error}"
