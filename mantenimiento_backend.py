from datetime import datetime

import psycopg

from db_connection import obtener_conexion
from tarjeta_circulacion_backend import (
    FECHA_EMISION_MINIMA,
    FECHA_VENCIMIENTO_FIJA,
    TIPOS_VEHICULO,
    USOS_VEHICULO,
    _limpiar_texto_catalogo,
    _obtener_o_crear_color,
    calcular_estado_tarjeta,
)


def buscar_tarjeta_para_mantenimiento(busqueda):
    busqueda = busqueda.strip().upper()
    if not busqueda:
        return None

    consulta = """
        SELECT
            t.no_tarjeta,
            t.estado,
            TO_CHAR(t.fecha_emision, 'YYYY-MM-DD') AS fecha_emision,
            TO_CHAR(t.fecha_vencimiento, 'YYYY-MM-DD') AS fecha_vencimiento,
            t.anio,
            p.cui,
            p.nit,
            p.nombre,
            v.uso,
            v.placa,
            v.tipo,
            ma.marca,
            li.linea,
            v.chasis,
            v.vin,
            v.serie,
            v.motor,
            v.asientos,
            v.ejes,
            v.cilindros,
            v.cilindrada,
            v.peso,
            c.color,
            mo.modelo
        FROM tarjeta t
        JOIN vehiculo v ON v.no_tarjeta = t.no_tarjeta
        JOIN propietario p ON p.cui = v.cui
        JOIN color c ON c.id_color = v.id_color
        JOIN linea li ON li.id_linea = v.id_linea
        JOIN modelo mo ON mo.id_modelo = li.id_modelo
        JOIN marca ma ON ma.id_marca = mo.id_marca
        WHERE UPPER(t.no_tarjeta) = %s OR UPPER(v.placa) = %s
        LIMIT 1
    """

    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(consulta, (busqueda, busqueda))
            fila = cursor.fetchone()

    if not fila:
        return None

    (
        no_tarjeta,
        estado_guardado,
        fecha_emision,
        fecha_vencimiento,
        anio,
        cui,
        nit,
        nombre,
        uso,
        placa,
        tipo,
        marca,
        linea,
        chasis,
        vin,
        serie,
        motor,
        asientos,
        ejes,
        cilindros,
        cilindrada,
        peso,
        color,
        modelo,
    ) = fila

    fecha_emision_dt = datetime.strptime(fecha_emision, "%Y-%m-%d").date()
    fecha_venc_dt = datetime.strptime(fecha_vencimiento, "%Y-%m-%d").date()
    estado_actual = bool(estado_guardado) and calcular_estado_tarjeta(
        fecha_emision_dt,
        fecha_venc_dt,
    )

    return {
        "no_tarjeta": no_tarjeta,
        "estado_guardado": bool(estado_guardado),
        "estado_actual": estado_actual,
        "fecha_emision": fecha_emision,
        "fecha_vencimiento": fecha_vencimiento,
        "anio": anio,
        "cui": cui.strip(),
        "nit": nit.strip(),
        "nombre": nombre.strip(),
        "uso": (uso or "").strip(),
        "placa": placa,
        "tipo": (tipo or "").strip(),
        "marca": marca.strip(),
        "linea": linea.strip(),
        "chasis": chasis.strip(),
        "vin": vin.strip(),
        "serie": serie.strip(),
        "motor": (motor or "").strip(),
        "asientos": asientos,
        "ejes": ejes,
        "cilindros": cilindros,
        "cilindrada": cilindrada,
        "peso": peso,
        "color": color.strip(),
        "modelo": modelo.strip(),
    }


def actualizar_tarjeta_existente(datos, id_usuario):
    try:
        no_tarjeta = datos["no_tarjeta"].strip().upper()
        placa = datos["placa"].strip().upper()
        cui = datos["cui"].strip()
        nit = datos["nit"].strip().upper()
        nombre = " ".join(datos["nombre"].strip().split())
        serie = datos["serie"].strip().upper()
        uso = _limpiar_texto_catalogo(datos["uso"])
        tipo = _limpiar_texto_catalogo(datos["tipo"])
        motor = datos["motor"].strip().upper()
        color = _limpiar_texto_catalogo(datos["color"])
        activa_por_solvente = bool(datos.get("activa_por_solvente", True))

        if not all([no_tarjeta, placa, cui, nit, nombre, serie, uso, tipo, motor, color]):
            return False, "Completa los datos obligatorios para el mantenimiento."

        if not cui.isdigit() or len(cui) != 13:
            return False, "El CUI debe tener exactamente 13 digitos."

        if len(nit) < 7:
            return False, "El NIT debe tener al menos 7 caracteres."

        if len(nit) > 13:
            return False, "El NIT no puede tener mas de 13 caracteres."

        if len(nombre) > 100:
            return False, "El nombre no puede tener mas de 100 caracteres."

        if len(serie) != 17:
            return False, "La serie debe tener exactamente 17 caracteres."

        if len(motor) != 14:
            return False, "El motor debe tener exactamente 14 caracteres."

        if len(color) > 150:
            return False, "El color no puede tener mas de 150 caracteres."

        if uso not in USOS_VEHICULO:
            return False, "Selecciona un uso valido para el vehiculo."

        if tipo not in TIPOS_VEHICULO:
            return False, "Selecciona un tipo valido para el vehiculo."

    except KeyError as error:
        return False, f"Falta un dato obligatorio: {error}"

    try:
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                def cancelar(mensaje):
                    conexion.rollback()
                    return False, mensaje

                cursor.execute(
                    "SELECT 1 FROM usuario WHERE id_usuario = %s",
                    (id_usuario,),
                )
                if not cursor.fetchone():
                    return cancelar("El usuario que realiza el mantenimiento no existe.")

                cursor.execute(
                    """
                    SELECT t.fecha_emision, t.fecha_vencimiento
                    FROM tarjeta t
                    JOIN vehiculo v ON v.no_tarjeta = t.no_tarjeta
                    WHERE t.no_tarjeta = %s AND v.placa = %s
                    """,
                    (no_tarjeta, placa),
                )
                tarjeta = cursor.fetchone()
                if not tarjeta:
                    return cancelar("No existe una tarjeta con esa placa y numero.")

                fecha_emision, fecha_vencimiento = tarjeta

                cursor.execute(
                    "SELECT nit, nombre FROM propietario WHERE cui = %s",
                    (cui,),
                )
                propietario = cursor.fetchone()

                if propietario:
                    nit_bd, nombre_bd = propietario
                    if nit_bd.strip().upper() != nit or nombre_bd.strip() != nombre:
                        return cancelar(
                            "El CUI ya existe con datos distintos. Revisa NIT y nombre."
                        )
                else:
                    cursor.execute(
                        """
                        SELECT cui
                        FROM propietario
                        WHERE UPPER(TRIM(nit)) = %s
                        """,
                        (nit,),
                    )
                    propietario_nit = cursor.fetchone()
                    if propietario_nit:
                        return cancelar(
                            "El NIT ya pertenece a otro propietario registrado."
                        )

                    cursor.execute(
                        """
                        INSERT INTO propietario (cui, nit, nombre)
                        VALUES (%s, %s, %s)
                        """,
                        (cui, nit, nombre),
                    )

                id_color = _obtener_o_crear_color(cursor, color)
                estado_final = activa_por_solvente and calcular_estado_tarjeta(
                    fecha_emision,
                    fecha_vencimiento,
                )

                cursor.execute(
                    """
                    UPDATE vehiculo
                    SET cui = %s,
                        serie = %s,
                        id_color = %s,
                        uso = %s,
                        tipo = %s,
                        motor = %s
                    WHERE placa = %s AND no_tarjeta = %s
                    """,
                    (cui, serie, id_color, uso, tipo, motor, placa, no_tarjeta),
                )

                cursor.execute(
                    """
                    UPDATE tarjeta
                    SET estado = %s
                    WHERE no_tarjeta = %s
                    """,
                    (estado_final, no_tarjeta),
                )

                cursor.execute("SELECT COALESCE(MAX(id_registro), 0) + 1 FROM registro")
                id_registro = cursor.fetchone()[0]
                ahora = datetime.now()

                cursor.execute(
                    """
                    INSERT INTO registro
                    (id_registro, fecha_registro, hora_registro, estado, id_usuario, placa)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        id_registro,
                        ahora.date(),
                        ahora.time().replace(microsecond=0),
                        estado_final,
                        id_usuario,
                        placa,
                    ),
                )

        if not activa_por_solvente:
            return True, "Tarjeta actualizada y marcada como no activa por impago."

        if not calcular_estado_tarjeta(
            fecha_emision,
            fecha_vencimiento,
            datetime.now().date(),
        ):
            return True, "Tarjeta actualizada. Actualmente aparece como no activa por vigencia."

        return True, "Tarjeta actualizada correctamente."
    except psycopg.errors.UniqueViolation as error:
        if getattr(error.diag, "constraint_name", "") == "unq_nit":
            return False, "El NIT ya pertenece a otro propietario registrado."
        return False, "No fue posible actualizar la tarjeta porque existe un dato unico repetido."
    except psycopg.Error as error:
        return False, f"No fue posible actualizar la tarjeta: {error}"
