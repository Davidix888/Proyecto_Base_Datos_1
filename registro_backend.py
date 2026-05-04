from tarjeta_circulacion_backend import FECHA_EMISION_MINIMA, FECHA_VENCIMIENTO_FIJA

from db_connection import obtener_conexion


def obtener_registros(filtros=None):
    filtros = filtros or {}
    condiciones = []
    parametros = []

    mapa_filtros = {
        "placa": "v.placa",
        "cui": "p.cui",
        "nit": "p.nit",
        "nombre": "p.nombre",
        "uso": "v.uso",
        "tipo": "v.tipo",
        "marca": "ma.marca",
        "color": "c.color",
        "no_tarjeta": "t.no_tarjeta",
    }

    for clave, columna in mapa_filtros.items():
        valor = filtros.get(clave, "").strip()
        if valor:
            condiciones.append(f"{columna} ILIKE %s")
            parametros.append(f"%{valor}%")

    consulta = """
        SELECT
            r.id_registro,
            TO_CHAR(r.fecha_registro, 'YYYY-MM-DD') AS fecha_registro,
            TO_CHAR(r.hora_registro, 'HH24:MI:SS') AS hora_registro,
            CASE
                WHEN t.estado = TRUE
                 AND t.fecha_emision BETWEEN %s AND %s
                 AND CURRENT_DATE BETWEEN t.fecha_emision AND %s
                THEN 'ACTIVA'
                ELSE 'NO ACTIVA'
            END AS estado,
            COALESCE(u.nombre_usuario, '') AS usuario,
            v.placa,
            p.cui,
            p.nit,
            p.nombre,
            COALESCE(v.uso, '') AS uso,
            COALESCE(v.tipo, '') AS tipo,
            CONCAT_WS(' / ', ma.marca, mo.modelo, li.linea) AS vehiculo,
            c.color,
            t.no_tarjeta,
            COALESCE(v.serie, '') AS serie,
            COALESCE(v.motor, '') AS motor,
            v.asientos,
            v.ejes,
            v.cilindros,
            v.cilindrada,
            v.peso
        FROM registro r
        JOIN usuario u ON u.id_usuario = r.id_usuario
        JOIN vehiculo v ON v.placa = r.placa
        JOIN propietario p ON p.cui = v.cui
        JOIN tarjeta t ON t.no_tarjeta = v.no_tarjeta
        JOIN color c ON c.id_color = v.id_color
        JOIN linea li ON li.id_linea = v.id_linea
        JOIN modelo mo ON mo.id_modelo = li.id_modelo
        JOIN marca ma ON ma.id_marca = mo.id_marca
    """

    parametros_estado = [
        FECHA_EMISION_MINIMA,
        FECHA_VENCIMIENTO_FIJA,
        FECHA_VENCIMIENTO_FIJA,
    ]

    if condiciones:
        consulta += "\nWHERE " + " AND ".join(condiciones)

    consulta += "\nORDER BY r.id_registro DESC"

    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(consulta, parametros_estado + parametros)
            return cursor.fetchall()
