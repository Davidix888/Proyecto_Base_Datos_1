from auth_backend import obtener_roles_registrados, validar_inicio_sesion
from catalog_backend import (
    obtener_colores,
    obtener_lineas_por_modelo,
    obtener_marcas,
    obtener_modelos_por_marca,
)
from db_connection import DB_CONFIG, obtener_conexion
from propietario_backend import registrar_propietario
from mantenimiento_backend import (
    actualizar_tarjeta_existente,
    buscar_tarjeta_para_mantenimiento,
)
from registro_backend import obtener_registros
from tarjeta_circulacion_backend import (
    FECHA_EMISION_MINIMA,
    FECHA_VENCIMIENTO_FIJA,
    TIPOS_VEHICULO,
    USOS_VEHICULO,
    buscar_propietario_por_cui,
    calcular_estado_tarjeta,
    registrar_tarjeta_circulacion,
)


__all__ = [
    "DB_CONFIG",
    "obtener_conexion",
    "validar_inicio_sesion",
    "obtener_roles_registrados",
    "registrar_propietario",
    "buscar_tarjeta_para_mantenimiento",
    "actualizar_tarjeta_existente",
    "obtener_registros",
    "obtener_marcas",
    "obtener_modelos_por_marca",
    "obtener_lineas_por_modelo",
    "obtener_colores",
    "buscar_propietario_por_cui",
    "FECHA_EMISION_MINIMA",
    "FECHA_VENCIMIENTO_FIJA",
    "TIPOS_VEHICULO",
    "USOS_VEHICULO",
    "calcular_estado_tarjeta",
    "registrar_tarjeta_circulacion",
]
