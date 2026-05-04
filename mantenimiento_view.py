import PySimpleGUI as sg

from gui_helpers import (
    COLORES,
    FUENTE_SECCION,
    FUENTE_TEXTO,
    actualizar_mensaje,
    boton_primario,
    boton_secundario,
    crear_encabezado,
)
from login import TIPOS_VEHICULO, USOS_VEHICULO, buscar_tarjeta_para_mantenimiento, actualizar_tarjeta_existente


def _cargar_tarjeta(window, datos):
    if not datos:
        return

    window["-NO_TARJETA-"].update(datos["no_tarjeta"])
    window["-FECHA_EMISION-"].update(datos["fecha_emision"])
    window["-FECHA_VENCIMIENTO-"].update(datos["fecha_vencimiento"])
    window["-ANIO-"].update(str(datos["anio"]))
    window["-CUI-"].update(datos["cui"])
    window["-NIT-"].update(datos["nit"])
    window["-NOMBRE-"].update(datos["nombre"])
    window["-USO-"].update(datos["uso"])
    window["-PLACA-"].update(datos["placa"])
    window["-TIPO-"].update(datos["tipo"])
    window["-MARCA-"].update(datos["marca"])
    window["-LINEA-"].update(datos["linea"])
    window["-CHASIS-"].update(datos["chasis"])
    window["-VIN-"].update(datos["vin"])
    window["-SERIE-"].update(datos["serie"])
    window["-MOTOR-"].update(datos["motor"])
    window["-ASIENTOS-"].update(str(datos["asientos"]))
    window["-EJES-"].update(str(datos["ejes"]))
    window["-CILINDROS-"].update("" if datos["cilindros"] is None else str(datos["cilindros"]))
    window["-CILINDRADA-"].update("" if datos["cilindrada"] is None else str(datos["cilindrada"]))
    window["-PESO-"].update("" if datos["peso"] is None else str(datos["peso"]))
    window["-COLOR-"].update(datos["color"])
    window["-MODELO-"].update(datos["modelo"])
    window["-ACTIVA-"].update(value=datos["estado_guardado"])

    estado_texto = "ACTIVA" if datos["estado_actual"] else "NO ACTIVA"
    estado_color = COLORES["exito"] if datos["estado_actual"] else COLORES["error"]
    window["-ESTADO-ACTUAL-"].update(
        f"Estado actual de la tarjeta: {estado_texto}",
        text_color=estado_color,
    )


def abrir_mantenimiento_tarjeta(id_usuario, nombre_usuario):
    layout = [
        *crear_encabezado(
            "Mantenimiento de tarjeta",
            f"Usuario: {nombre_usuario} | Actualiza duenio, serie, motor, uso, tipo, color y estado manual.",
        ),
        [sg.Text("")],
        [
            sg.Frame(
                "Buscar tarjeta",
                [
                    [
                        sg.Text("Placa o No. tarjeta", size=(18, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-BUSQUEDA-", size=(24, 1), font=FUENTE_TEXTO),
                        boton_primario("Buscar", key="-BUSCAR-", size=(12, 1), bind_return_key=True),
                    ]
                ],
                title_color=COLORES["primario_oscuro"],
                font=FUENTE_SECCION,
                border_width=1,
                relief=sg.RELIEF_SOLID,
            )
        ],
        [
            sg.Frame(
                "Datos de la tarjeta",
                [
                    [
                        sg.Text("No. tarjeta", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-NO_TARJETA-", size=(16, 1), font=FUENTE_TEXTO, disabled=True),
                    ],
                    [
                        sg.Text("Fecha emision", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-FECHA_EMISION-", size=(14, 1), font=FUENTE_TEXTO, disabled=True),
                        sg.Text("Fecha venc.", size=(10, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-FECHA_VENCIMIENTO-", size=(14, 1), font=FUENTE_TEXTO, disabled=True),
                        sg.Text("Anio", size=(6, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-ANIO-", size=(8, 1), font=FUENTE_TEXTO, disabled=True),
                    ],
                    [
                        sg.Text(
                            "",
                            key="-ESTADO-ACTUAL-",
                            font=FUENTE_SECCION,
                            text_color=COLORES["texto_suave"],
                        )
                    ],
                ],
                title_color=COLORES["primario_oscuro"],
                font=FUENTE_SECCION,
                border_width=1,
                relief=sg.RELIEF_SOLID,
            )
        ],
        [
            sg.Frame(
                "Nuevo duenio o duenio actual",
                [
                    [sg.Text("CUI", size=(12, 1), font=FUENTE_TEXTO), sg.Input(key="-CUI-", size=(20, 1), font=FUENTE_TEXTO)],
                    [sg.Text("NIT", size=(12, 1), font=FUENTE_TEXTO), sg.Input(key="-NIT-", size=(20, 1), font=FUENTE_TEXTO)],
                    [sg.Text("Nombre", size=(12, 1), font=FUENTE_TEXTO), sg.Input(key="-NOMBRE-", size=(36, 1), font=FUENTE_TEXTO)],
                ],
                title_color=COLORES["primario_oscuro"],
                font=FUENTE_SECCION,
                border_width=1,
                relief=sg.RELIEF_SOLID,
            )
        ],
        [
            sg.Frame(
                "Cambios permitidos",
                [
                    [
                        sg.Text("Uso", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Combo(
                            values=list(USOS_VEHICULO),
                            key="-USO-",
                            size=(18, 1),
                            readonly=True,
                            font=FUENTE_TEXTO,
                        ),
                        sg.Text("Placa", size=(8, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-PLACA-", size=(14, 1), font=FUENTE_TEXTO, disabled=True),
                    ],
                    [
                        sg.Text("Tipo", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Combo(
                            values=list(TIPOS_VEHICULO),
                            key="-TIPO-",
                            size=(18, 1),
                            readonly=True,
                            font=FUENTE_TEXTO,
                        ),
                        sg.Text("Marca", size=(8, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-MARCA-", size=(14, 1), font=FUENTE_TEXTO, disabled=True),
                    ],
                    [
                        sg.Text("Linea", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-LINEA-", size=(18, 1), font=FUENTE_TEXTO, disabled=True),
                        sg.Text("Modelo", size=(8, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-MODELO-", size=(14, 1), font=FUENTE_TEXTO, disabled=True),
                    ],
                    [
                        sg.Text("Chasis", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-CHASIS-", size=(18, 1), font=FUENTE_TEXTO, disabled=True),
                        sg.Text("VIN", size=(8, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-VIN-", size=(14, 1), font=FUENTE_TEXTO, disabled=True),
                    ],
                    [
                        sg.Text("Serie", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-SERIE-", size=(18, 1), font=FUENTE_TEXTO),
                        sg.Text("Motor", size=(8, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-MOTOR-", size=(14, 1), font=FUENTE_TEXTO),
                    ],
                    [
                        sg.Text("Asientos", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-ASIENTOS-", size=(8, 1), font=FUENTE_TEXTO, disabled=True),
                        sg.Text("Ejes", size=(8, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-EJES-", size=(8, 1), font=FUENTE_TEXTO, disabled=True),
                        sg.Text("Cilindros", size=(10, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-CILINDROS-", size=(8, 1), font=FUENTE_TEXTO, disabled=True),
                    ],
                    [
                        sg.Text("C.C.", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-CILINDRADA-", size=(10, 1), font=FUENTE_TEXTO, disabled=True),
                    ],
                    [
                        sg.Text("Color", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-COLOR-", size=(18, 1), font=FUENTE_TEXTO),
                        sg.Text("Ton.", size=(8, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-PESO-", size=(14, 1), font=FUENTE_TEXTO, disabled=True),
                        sg.Checkbox(
                            "Tarjeta activa por solvencia",
                            key="-ACTIVA-",
                            default=True,
                            font=FUENTE_TEXTO,
                        ),
                    ],
                ],
                title_color=COLORES["primario_oscuro"],
                font=FUENTE_SECCION,
                border_width=1,
                relief=sg.RELIEF_SOLID,
            )
        ],
        [sg.Text("", key="-MSG-MANT-", size=(70, 2), justification="center", font=FUENTE_TEXTO)],
        [
            boton_primario("Guardar cambios", key="-GUARDAR-", size=(16, 1)),
            boton_secundario("Cerrar", size=(12, 1)),
        ],
    ]

    window = sg.Window(
        "Mantenimiento de tarjeta",
        layout,
        size=(930, 700),
        modal=True,
        finalize=True,
        resizable=False,
        margins=(18, 16),
    )
    window["-BUSQUEDA-"].set_focus()

    tarjeta_cargada = None

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Cerrar"):
            window.close()
            return False, "Mantenimiento de tarjeta cerrado."

        if event == "-BUSCAR-":
            tarjeta_cargada = buscar_tarjeta_para_mantenimiento(values["-BUSQUEDA-"])
            if not tarjeta_cargada:
                actualizar_mensaje(
                    window,
                    "-MSG-MANT-",
                    "No se encontro una tarjeta con esa placa o numero.",
                    COLORES["alerta"],
                )
                continue

            _cargar_tarjeta(window, tarjeta_cargada)
            actualizar_mensaje(
                window,
                "-MSG-MANT-",
                "Tarjeta cargada. Ya puedes hacer mantenimiento.",
                COLORES["exito"],
            )

        elif event == "-GUARDAR-":
            if not tarjeta_cargada:
                actualizar_mensaje(
                    window,
                    "-MSG-MANT-",
                    "Primero debes buscar una tarjeta para poder actualizarla.",
                    COLORES["alerta"],
                )
                continue

            datos = {
                "no_tarjeta": values["-NO_TARJETA-"],
                "placa": values["-PLACA-"],
                "cui": values["-CUI-"],
                "nit": values["-NIT-"],
                "nombre": values["-NOMBRE-"],
                "serie": values["-SERIE-"],
                "uso": values["-USO-"],
                "tipo": values["-TIPO-"],
                "motor": values["-MOTOR-"],
                "color": values["-COLOR-"],
                "activa_por_solvente": values["-ACTIVA-"],
            }
            exito, mensaje = actualizar_tarjeta_existente(datos, id_usuario)
            color = COLORES["exito"] if exito else COLORES["error"]
            actualizar_mensaje(window, "-MSG-MANT-", mensaje, color)

            if exito:
                tarjeta_cargada = buscar_tarjeta_para_mantenimiento(values["-NO_TARJETA-"])
                if tarjeta_cargada:
                    _cargar_tarjeta(window, tarjeta_cargada)
