from datetime import datetime

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
from login import (
    FECHA_EMISION_MINIMA,
    FECHA_VENCIMIENTO_FIJA,
    TIPOS_VEHICULO,
    USOS_VEHICULO,
    buscar_propietario_por_cui,
    calcular_estado_tarjeta,
    registrar_tarjeta_circulacion,
)


def _actualizar_estado_visual(window, fecha_emision_texto, fecha_venc_texto):
    fecha_emision_texto = fecha_emision_texto.strip()
    fecha_venc_texto = fecha_venc_texto.strip()

    if not fecha_emision_texto or not fecha_venc_texto:
        window["-ESTADO-VISTA-"].update(
            "Estado pendiente de fechas",
            text_color=COLORES["texto_suave"],
        )
        return

    try:
        fecha_emision = datetime.strptime(fecha_emision_texto, "%Y-%m-%d").date()
        fecha_venc = datetime.strptime(fecha_venc_texto, "%Y-%m-%d").date()
    except ValueError:
        window["-ESTADO-VISTA-"].update(
            "Revisa el formato de fechas",
            text_color=COLORES["alerta"],
        )
        return

    if fecha_emision < FECHA_EMISION_MINIMA:
        window["-ESTADO-VISTA-"].update(
            "No activa: emision antes de 2025-08-01",
            text_color=COLORES["error"],
        )
        return

    if fecha_emision > FECHA_VENCIMIENTO_FIJA:
        window["-ESTADO-VISTA-"].update(
            "No activa: emision despues de 2026-07-31",
            text_color=COLORES["error"],
        )
        return

    if calcular_estado_tarjeta(fecha_emision, fecha_venc):
        texto = "Estado actual: ACTIVA"
        color = COLORES["exito"]
    else:
        texto = "Estado actual: NO ACTIVA"
        color = COLORES["error"]

    window["-ESTADO-VISTA-"].update(texto, text_color=color)


def abrir_formulario_tarjeta_circulacion(id_usuario, nombre_usuario):
    layout = [
        *crear_encabezado(
            "Registro de tarjeta de circulacion",
            f"Operador: {nombre_usuario} | ID: {id_usuario}",
        ),
        [sg.Text("")],
        [
            sg.Frame(
                "Propietario",
                [
                    [
                        sg.Text("CUI", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-CUI-", size=(18, 1), font=FUENTE_TEXTO),
                        boton_secundario("Buscar CUI", size=(12, 1)),
                    ],
                    [
                        sg.Text("NIT", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-NIT-", size=(32, 1), font=FUENTE_TEXTO),
                    ],
                    [
                        sg.Text("Nombre", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-NOMBRE-", size=(32, 1), font=FUENTE_TEXTO),
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
                "Tarjeta",
                [
                    [
                        sg.Text("No. tarjeta", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-NO_TARJETA-", size=(16, 1), font=FUENTE_TEXTO),
                        sg.Text(
                            "Estado calculado automaticamente",
                            font=FUENTE_TEXTO,
                            text_color=COLORES["texto_suave"],
                        ),
                    ],
                    [
                        sg.Text("Fecha emision", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(
                            key="-FECHA_EMISION-",
                            size=(14, 1),
                            font=FUENTE_TEXTO,
                            enable_events=True,
                        ),
                        sg.Text(
                            "Valida entre 2025-08-01 y 2026-07-31",
                            font=FUENTE_TEXTO,
                            text_color=COLORES["texto_suave"],
                        ),
                    ],
                    [
                        sg.Text("Anio", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-ANIO-", size=(8, 1), font=FUENTE_TEXTO),
                        sg.Text("Fecha venc.", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Text(
                            "2026-07-31",
                            size=(14, 1),
                            font=FUENTE_SECCION,
                            text_color=COLORES["acento"],
                        ),
                    ],
                    [
                        sg.Text(
                            "Estado pendiente de fechas",
                            key="-ESTADO-VISTA-",
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
                "Vehiculo",
                [
                    [
                        sg.Text("Uso", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Combo(
                            values=list(USOS_VEHICULO),
                            key="-USO-",
                            size=(24, 1),
                            readonly=True,
                            font=FUENTE_TEXTO,
                        ),
                        sg.Text("Placa", size=(8, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-PLACA-", size=(16, 1), font=FUENTE_TEXTO),
                    ],
                    [
                        sg.Text("Tipo", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Combo(
                            values=list(TIPOS_VEHICULO),
                            key="-TIPO-",
                            size=(24, 1),
                            readonly=True,
                            font=FUENTE_TEXTO,
                        ),
                        sg.Text("Marca", size=(8, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-MARCA-", size=(16, 1), font=FUENTE_TEXTO),
                    ],
                    [
                        sg.Text("Linea", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-LINEA-", size=(24, 1), font=FUENTE_TEXTO),
                        sg.Text("Modelo", size=(8, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-MODELO-", size=(16, 1), font=FUENTE_TEXTO),
                    ],
                    [
                        sg.Text("Chasis", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-CHASIS-", size=(24, 1), font=FUENTE_TEXTO),
                        sg.Text("VIN", size=(8, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-VIN-", size=(16, 1), font=FUENTE_TEXTO),
                    ],
                    [
                        sg.Text("Serie", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-SERIE-", size=(24, 1), font=FUENTE_TEXTO),
                        sg.Text("Motor", size=(8, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-MOTOR-", size=(16, 1), font=FUENTE_TEXTO),
                    ],
                    [
                        sg.Text("Asientos", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-ASIENTOS-", size=(8, 1), font=FUENTE_TEXTO),
                        sg.Text("Ejes", size=(8, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-EJES-", size=(8, 1), font=FUENTE_TEXTO),
                        sg.Text("Cilindros", size=(10, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-CILINDROS-", size=(8, 1), font=FUENTE_TEXTO),
                    ],
                    [
                        sg.Text("C.C.", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-CILINDRADA-", size=(12, 1), font=FUENTE_TEXTO),
                    ],
                    [
                        sg.Text("Color", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-COLOR-", size=(24, 1), font=FUENTE_TEXTO),
                        sg.Text("Ton.", size=(8, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-PESO-", size=(16, 1), font=FUENTE_TEXTO),
                    ],
                ],
                title_color=COLORES["primario_oscuro"],
                font=FUENTE_SECCION,
                border_width=1,
                relief=sg.RELIEF_SOLID,
            )
        ],
        [
            sg.Text(
                "",
                key="-MSG-TARJETA-",
                size=(74, 3),
                text_color=COLORES["texto_suave"],
                justification="center",
                font=FUENTE_TEXTO,
            )
        ],
        [boton_primario("Guardar tarjeta", key="-GUARDAR-", size=(16, 1)), boton_secundario("Cancelar", size=(12, 1))],
    ]

    window = sg.Window(
        "Registro de tarjeta de circulacion",
        layout,
        size=(930, 690),
        modal=True,
        finalize=True,
        resizable=False,
        margins=(18, 16),
    )
    window["-CUI-"].set_focus()
    window["-ESTADO-VISTA-"].update(
        "Estado pendiente de fechas",
        text_color=COLORES["texto_suave"],
    )

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Cancelar"):
            window.close()
            return False, "Registro de tarjeta cancelado."

        if event == "Buscar CUI":
            propietario = buscar_propietario_por_cui(values["-CUI-"])
            if propietario:
                cui, nit, nombre = propietario
                window["-CUI-"].update(cui.strip())
                window["-NIT-"].update(nit.strip())
                window["-NOMBRE-"].update(nombre.strip())
                actualizar_mensaje(
                    window,
                    "-MSG-TARJETA-",
                    "Propietario encontrado. Puedes continuar con la tarjeta.",
                    "#d9ead3",
                )
            else:
                window["-NIT-"].update("")
                window["-NOMBRE-"].update("")
                actualizar_mensaje(
                    window,
                    "-MSG-TARJETA-",
                    "No existe un propietario con ese CUI. Puedes registrarlo aqui mismo.",
                    "#ffd966",
                )

        elif event == "-FECHA_EMISION-":
            _actualizar_estado_visual(
                window,
                values["-FECHA_EMISION-"],
                str(FECHA_VENCIMIENTO_FIJA),
            )

        elif event == "-GUARDAR-":
            datos = {
                "cui": values["-CUI-"],
                "nit": values["-NIT-"],
                "nombre": values["-NOMBRE-"],
                "no_tarjeta": values["-NO_TARJETA-"],
                "fecha_emision": values["-FECHA_EMISION-"],
                "anio": values["-ANIO-"],
                "fecha_vencimiento": str(FECHA_VENCIMIENTO_FIJA),
                "placa": values["-PLACA-"],
                "vin": values["-VIN-"],
                "chasis": values["-CHASIS-"],
                "serie": values["-SERIE-"],
                "motor": values["-MOTOR-"],
                "ejes": values["-EJES-"],
                "peso": values["-PESO-"],
                "asientos": values["-ASIENTOS-"],
                "cilindros": values["-CILINDROS-"],
                "cilindrada": values["-CILINDRADA-"],
                "color": values["-COLOR-"],
                "uso": values["-USO-"],
                "tipo": values["-TIPO-"],
                "marca": values["-MARCA-"],
                "modelo": values["-MODELO-"],
                "linea": values["-LINEA-"],
            }

            exito, mensaje = registrar_tarjeta_circulacion(datos, id_usuario)
            color = "#d9ead3" if exito else "#ffb3b3"
            actualizar_mensaje(window, "-MSG-TARJETA-", mensaje, color)

            if exito:
                window.close()
                return True, mensaje
