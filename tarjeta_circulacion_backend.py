from datetime import datetime
from decimal import Decimal, InvalidOperation

import psycopg

from db_connection import obtener_conexion

FECHA_EMISION_MINIMA = datetime(2025, 8, 1).date()
FECHA_VENCIMIENTO_FIJA = datetime(2026, 7, 31).date()
USOS_VEHICULO = (
    "PARTICULAR",
    "COMERCIAL",
    "ALQUILER",
    "TRANSPORTE URBANO",
    "MOTOCICLETA",
    "CARGA PESADA",
    "ESPECIALES",
)
TIPOS_VEHICULO = (
    "AUTOMOVIL",
    "CAMIONETA",
    "PICK-UP",
    "PANEL",
    "MOTOCICLETA",
    "CAMION",
    "AUTOBUS",
    "CABEZAL",
)


def buscar_propietario_por_cui(cui):
    cui = cui.strip()

    if not cui:
        return None

    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT cui, nit, nombre
                FROM propietario
                WHERE cui = %s
                """,
                (cui,),
            )
            return cursor.fetchone()


def _limpiar_texto_catalogo(valor):
    return " ".join(valor.strip().upper().split())


def _obtener_siguiente_id(cursor, tabla, columna_id):
    cursor.execute(f"SELECT COALESCE(MAX({columna_id}), 0) + 1 FROM {tabla}")
    return cursor.fetchone()[0]


def _obtener_o_crear_marca(cursor, marca):
    cursor.execute(
        """
        SELECT id_marca
        FROM marca
        WHERE UPPER(TRIM(marca)) = %s
        """,
        (marca,),
    )
    fila = cursor.fetchone()
    if fila:
        return fila[0]

    id_marca = _obtener_siguiente_id(cursor, "marca", "id_marca")
    cursor.execute(
        """
        INSERT INTO marca (id_marca, marca)
        VALUES (%s, %s)
        """,
        (id_marca, marca),
    )
    return id_marca


def _obtener_o_crear_modelo(cursor, modelo, id_marca):
    cursor.execute(
        """
        SELECT id_modelo
        FROM modelo
        WHERE UPPER(TRIM(modelo)) = %s AND id_marca = %s
        """,
        (modelo, id_marca),
    )
    fila = cursor.fetchone()
    if fila:
        return fila[0]

    id_modelo = _obtener_siguiente_id(cursor, "modelo", "id_modelo")
    cursor.execute(
        """
        INSERT INTO modelo (id_modelo, modelo, id_marca)
        VALUES (%s, %s, %s)
        """,
        (id_modelo, modelo, id_marca),
    )
    return id_modelo


def _obtener_o_crear_linea(cursor, linea, id_modelo):
    cursor.execute(
        """
        SELECT id_linea
        FROM linea
        WHERE UPPER(TRIM(linea)) = %s AND id_modelo = %s
        """,
        (linea, id_modelo),
    )
    fila = cursor.fetchone()
    if fila:
        return fila[0]

    id_linea = _obtener_siguiente_id(cursor, "linea", "id_linea")
    cursor.execute(
        """
        INSERT INTO linea (id_linea, linea, id_modelo)
        VALUES (%s, %s, %s)
        """,
        (id_linea, linea, id_modelo),
    )
    return id_linea


def _obtener_o_crear_color(cursor, color):
    cursor.execute(
        """
        SELECT id_color
        FROM color
        WHERE UPPER(TRIM(color)) = %s
        """,
        (color,),
    )
    fila = cursor.fetchone()
    if fila:
        return fila[0]

    id_color = _obtener_siguiente_id(cursor, "color", "id_color")
    cursor.execute(
        """
        INSERT INTO color (id_color, color)
        VALUES (%s, %s)
        """,
        (id_color, color),
    )
    return id_color


def calcular_estado_tarjeta(fecha_emision, fecha_vencimiento, fecha_referencia=None):
    fecha_referencia = fecha_referencia or datetime.now().date()
    return (
        FECHA_EMISION_MINIMA <= fecha_emision <= FECHA_VENCIMIENTO_FIJA
        and fecha_vencimiento == FECHA_VENCIMIENTO_FIJA
        and fecha_emision <= fecha_referencia <= fecha_vencimiento
    )


def registrar_tarjeta_circulacion(datos, id_usuario):
    try:
        cui = datos["cui"].strip()
        nit = datos["nit"].strip().upper()
        nombre = " ".join(datos["nombre"].strip().split())
        no_tarjeta = datos["no_tarjeta"].strip().upper()
        placa = datos["placa"].strip().upper()
        vin = datos["vin"].strip().upper()
        chasis = datos["chasis"].strip().upper()
        serie = datos["serie"].strip().upper()
        motor = datos["motor"].strip().upper()
        marca = _limpiar_texto_catalogo(datos["marca"])
        modelo = _limpiar_texto_catalogo(datos["modelo"])
        linea = _limpiar_texto_catalogo(datos["linea"])
        color = _limpiar_texto_catalogo(datos["color"])
        uso = _limpiar_texto_catalogo(datos["uso"])
        tipo = _limpiar_texto_catalogo(datos["tipo"])

        if not all(
            [
                cui,
                nit,
                nombre,
                no_tarjeta,
                datos["fecha_emision"],
                datos["fecha_vencimiento"],
                datos["anio"],
                placa,
                vin,
                chasis,
                serie,
                motor,
                datos["ejes"],
                datos["peso"],
                datos["asientos"],
                datos["cilindros"],
                marca,
                modelo,
                linea,
                color,
                uso,
                tipo,
            ]
        ):
            return False, "Completa todos los campos obligatorios de la tarjeta."

        if not cui.isdigit() or len(cui) != 13:
            return False, "El CUI debe tener exactamente 13 digitos."

        if len(nit) < 7:
            return False, "El NIT debe tener al menos 7 caracteres."

        if len(nit) > 13:
            return False, "El NIT no puede tener mas de 13 caracteres."

        if len(nombre) > 100:
            return False, "El nombre no puede tener mas de 100 caracteres."

        if len(no_tarjeta) > 12:
            return False, "El numero de tarjeta no puede tener mas de 12 caracteres."

        if len(placa) > 7:
            return False, "La placa no puede tener mas de 7 caracteres."

        if len(vin) != 17 or len(chasis) != 17 or len(serie) != 17:
            return False, "VIN, chasis y serie deben tener exactamente 17 caracteres."

        if len(motor) != 14:
            return False, "El motor debe tener exactamente 14 caracteres."

        if any(len(valor) > 150 for valor in (marca, modelo, linea, color)):
            return False, "Marca, modelo, linea y color no pueden pasar de 150 caracteres."

        if uso not in USOS_VEHICULO:
            return False, "Selecciona un uso valido para el vehiculo."

        if tipo not in TIPOS_VEHICULO:
            return False, "Selecciona un tipo valido para el vehiculo."

        fecha_emision = datetime.strptime(datos["fecha_emision"], "%Y-%m-%d").date()
        fecha_vencimiento = FECHA_VENCIMIENTO_FIJA
        anio = int(datos["anio"])
        ejes = int(datos["ejes"])
        asientos = int(datos["asientos"])
        cilindros = int(datos["cilindros"])
        peso = Decimal(str(datos["peso"]))
        cilindrada = (
            Decimal(str(datos["cilindrada"])) if str(datos["cilindrada"]).strip() else None
        )
        if fecha_emision < FECHA_EMISION_MINIMA:
            return False, "La fecha de emision no puede ser anterior a 2025-08-01."

        if fecha_emision > FECHA_VENCIMIENTO_FIJA:
            return False, "La fecha de emision no puede ser posterior a 2026-07-31."

        if fecha_vencimiento < datetime.now().date():
            return False, "La fecha de vencimiento no puede estar vencida."

        if anio < 1900 or anio > 2100:
            return False, "El anio debe estar en un rango valido."

        if ejes <= 0 or asientos <= 0 or cilindros <= 0:
            return False, "Ejes, asientos y cilindros deben ser mayores que cero."

        if peso < 0:
            return False, "El peso no puede ser negativo."

        if peso > Decimal("999.9"):
            return False, "El peso no puede ser mayor que 999.9 segun la base de datos."

        if cilindrada is not None and cilindrada <= 0:
            return False, "La cilindrada debe ser mayor que cero cuando se ingrese."

        estado = calcular_estado_tarjeta(fecha_emision, fecha_vencimiento)

    except ValueError:
        return False, "Revisa los campos numericos y las fechas con formato YYYY-MM-DD."
    except InvalidOperation:
        return False, "Peso y cilindrada deben ser valores numericos validos."

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
                    return cancelar("El usuario que registra la tarjeta no existe.")

                cursor.execute("SELECT nit, nombre FROM propietario WHERE cui = %s", (cui,))
                propietario = cursor.fetchone()

                if propietario:
                    nit_bd, nombre_bd = propietario
                    if nit_bd.strip().upper() != nit or nombre_bd.strip() != nombre:
                        return cancelar(
                            (
                                "El CUI ya existe con datos distintos. Revisa NIT y nombre."
                            )
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

                cursor.execute(
                    "SELECT 1 FROM tarjeta WHERE no_tarjeta = %s", (no_tarjeta,)
                )
                if cursor.fetchone():
                    return cancelar("Ya existe una tarjeta con ese numero.")

                cursor.execute("SELECT 1 FROM vehiculo WHERE placa = %s", (placa,))
                if cursor.fetchone():
                    return cancelar("Ya existe un vehiculo con esa placa.")

                id_marca = _obtener_o_crear_marca(cursor, marca)
                id_modelo = _obtener_o_crear_modelo(cursor, modelo, id_marca)
                id_linea = _obtener_o_crear_linea(cursor, linea, id_modelo)
                id_color = _obtener_o_crear_color(cursor, color)

                cursor.execute("SELECT 1 FROM color WHERE id_color = %s", (id_color,))
                if not cursor.fetchone():
                    return cancelar("El color seleccionado no existe en la base.")

                cursor.execute("SELECT 1 FROM linea WHERE id_linea = %s", (id_linea,))
                if not cursor.fetchone():
                    return cancelar("La linea seleccionada no existe en la base.")

                cursor.execute(
                    """
                    INSERT INTO tarjeta
                    (no_tarjeta, estado, fecha_emision, anio, fecha_vencimiento)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (no_tarjeta, estado, fecha_emision, anio, fecha_vencimiento),
                )

                cursor.execute(
                    """
                    INSERT INTO vehiculo
                    (placa, vin, chasis, serie, ejes, peso, asientos,
                     cilindrada, id_color, id_linea, no_tarjeta, cui, uso, tipo, motor, cilindros)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        placa,
                        vin,
                        chasis,
                        serie,
                        ejes,
                        peso,
                        asientos,
                        cilindrada,
                        id_color,
                        id_linea,
                        no_tarjeta,
                        cui,
                        uso,
                        tipo,
                        motor,
                        cilindros,
                    ),
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
                        estado,
                        id_usuario,
                        placa,
                    ),
                )

        return True, "Tarjeta de circulacion registrada correctamente."
    except psycopg.errors.UniqueViolation as error:
        if getattr(error.diag, "constraint_name", "") == "unq_nit":
            return False, "El NIT ya pertenece a otro propietario registrado."
        return False, "No fue posible registrar la tarjeta porque ya existe un dato unico repetido."
    except psycopg.Error as error:
        return False, f"No fue posible registrar la tarjeta: {error}"
