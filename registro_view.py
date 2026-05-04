import PySimpleGUI as sg

from gui_helpers import (
    COLORES,
    FUENTE_SECCION,
    FUENTE_TEXTO,
    actualizar_mensaje,
    boton_peligro,
    boton_primario,
    boton_secundario,
    crear_encabezado,
)
from login import obtener_registros


ENCABEZADOS_REGISTRO = [
    "ID",
    "Fecha",
    "Hora",
    "Estado",
    "Usuario",
    "Placa",
    "CUI",
    "NIT",
    "Propietario",
    "Uso",
    "Tipo",
    "Vehiculo",
    "Color",
    "Tarjeta",
    "Serie",
    "Motor",
]


def _obtener_contexto_modo(nombre_rol, nombre_usuario, modo):
    contexto = {
        "propietario": (
            "Consulta de propietarios",
            f"{nombre_rol}: {nombre_usuario} | Filtra por CUI, NIT o nombre del propietario.",
        ),
        "vehiculo": (
            "Consulta de vehiculos",
            f"{nombre_rol}: {nombre_usuario} | Filtra por placa, uso, marca, color o numero de tarjeta.",
        ),
        "tarjeta": (
            "Consulta de tarjetas",
            f"{nombre_rol}: {nombre_usuario} | Filtra por numero de tarjeta, placa o propietario.",
        ),
        "general": (
            "Consulta de registros",
            f"{nombre_rol}: {nombre_usuario} | Filtra por placa, propietario, uso, marca, color o numero de tarjeta.",
        ),
    }
    return contexto.get(modo, contexto["general"])


def _actualizar_detalle(window, fila):
    if not fila:
        window["-DETALLE-"].update("")
        return

    (
        id_registro,
        fecha_registro,
        hora_registro,
        estado,
        usuario,
        placa,
        cui,
        nit,
        propietario,
        uso,
        tipo,
        vehiculo,
        color,
        tarjeta,
        serie,
        motor,
        asientos,
        ejes,
        cilindros,
        cilindrada,
        peso,
    ) = fila

    detalle = (
        f"Registro: {id_registro}\n"
        f"Fecha y hora: {fecha_registro} {hora_registro}\n"
        f"Estado actual de la tarjeta: {estado}\n"
        f"Usuario que registro el movimiento: {usuario}\n"
        f"Placa: {placa}\n"
        f"CUI: {cui}\n"
        f"NIT: {nit}\n"
        f"Propietario: {propietario}\n"
        f"Uso: {uso}\n"
        f"Tipo: {tipo}\n"
        f"Vehiculo: {vehiculo}\n"
        f"Serie: {serie}\n"
        f"Motor: {motor}\n"
        f"Asientos: {asientos}\n"
        f"Ejes: {ejes}\n"
        f"Cilindros: {cilindros if cilindros is not None else ''}\n"
        f"C.C.: {cilindrada if cilindrada is not None else ''}\n"
        f"Ton.: {peso if peso is not None else ''}\n"
        f"Color: {color}\n"
        f"No. tarjeta: {tarjeta}"
    )
    window["-DETALLE-"].update(detalle)


def _cargar_registros(window, filtros=None):
    try:
        filas = obtener_registros(filtros)
    except Exception as error:
        window["-TABLA-"].update(values=[])
        _actualizar_detalle(window, None)
        actualizar_mensaje(
            window,
            "-MSG-REGISTROS-",
            f"No fue posible cargar los registros: {error}",
            COLORES["error"],
        )
        return []

    filas_visibles = [fila[: len(ENCABEZADOS_REGISTRO)] for fila in filas]
    window["-TABLA-"].update(values=filas_visibles)
    _actualizar_detalle(window, filas[0] if filas else None)

    if filas:
        actualizar_mensaje(
            window,
            "-MSG-REGISTROS-",
            f"Se encontraron {len(filas)} registro(s).",
            COLORES["exito"],
        )
    else:
        actualizar_mensaje(
            window,
            "-MSG-REGISTROS-",
            "No hay registros para los filtros actuales.",
            COLORES["alerta"],
        )
    return filas


def abrir_visor_registros(nombre_rol, nombre_usuario, modo="general"):
    titulo, subtitulo = _obtener_contexto_modo(nombre_rol, nombre_usuario, modo)

    layout = [
        *crear_encabezado(
            titulo,
            subtitulo,
        ),
        [sg.Text("")],
        [
            sg.Frame(
                "Filtros",
                [
                    [
                        sg.Text("Placa", size=(10, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-F-PLACA-", size=(14, 1), font=FUENTE_TEXTO),
                        sg.Text("CUI", size=(10, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-F-CUI-", size=(16, 1), font=FUENTE_TEXTO),
                        sg.Text("NIT", size=(10, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-F-NIT-", size=(16, 1), font=FUENTE_TEXTO),
                    ],
                    [
                        sg.Text("Nombre", size=(10, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-F-NOMBRE-", size=(14, 1), font=FUENTE_TEXTO),
                        sg.Text("Uso", size=(10, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-F-USO-", size=(16, 1), font=FUENTE_TEXTO),
                    ],
                    [
                        sg.Text("Tipo", size=(10, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-F-TIPO-", size=(14, 1), font=FUENTE_TEXTO),
                        sg.Text("Marca", size=(10, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-F-MARCA-", size=(16, 1), font=FUENTE_TEXTO),
                        sg.Text("Color", size=(10, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-F-COLOR-", size=(16, 1), font=FUENTE_TEXTO),
                    ],
                    [
                        sg.Text("Tarjeta", size=(10, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-F-TARJETA-", size=(14, 1), font=FUENTE_TEXTO),
                        boton_primario("Buscar", key="-BUSCAR-", size=(12, 1), bind_return_key=True),
                        boton_secundario("Limpiar", key="-LIMPIAR-", size=(12, 1)),
                    ],
                ],
                title_color=COLORES["primario"],
                font=FUENTE_SECCION,
                border_width=1,
                relief=sg.RELIEF_SOLID,
            )
        ],
        [
            sg.Table(
                values=[],
                headings=ENCABEZADOS_REGISTRO,
                key="-TABLA-",
                auto_size_columns=False,
                col_widths=[6, 10, 9, 10, 14, 10, 14, 14, 22, 18, 18, 24, 14, 12, 18, 18],
                justification="left",
                num_rows=14,
                alternating_row_color="#13312B",
                header_background_color=COLORES["primario"],
                header_text_color="white",
                text_color=COLORES["texto"],
                background_color=COLORES["superficie"],
                enable_events=True,
                expand_x=True,
                expand_y=False,
            )
        ],
        [
            sg.Frame(
                "Detalle del registro seleccionado",
                [
                    [
                        sg.Multiline(
                            "",
                            key="-DETALLE-",
                            size=(140, 7),
                            disabled=True,
                            background_color=COLORES["superficie"],
                            text_color=COLORES["texto"],
                            font=FUENTE_TEXTO,
                            no_scrollbar=True,
                        )
                    ]
                ],
                title_color=COLORES["primario"],
                font=FUENTE_SECCION,
                border_width=1,
                relief=sg.RELIEF_SOLID,
            )
        ],
        [
            sg.Text(
                "",
                key="-MSG-REGISTROS-",
                size=(120, 2),
                justification="center",
                font=FUENTE_TEXTO,
                text_color=COLORES["texto_suave"],
            )
        ],
        [boton_peligro("Cerrar", size=(14, 1))],
    ]

    window = sg.Window(
        titulo,
        layout,
        size=(1380, 760),
        modal=True,
        finalize=True,
        resizable=False,
        margins=(18, 16),
    )
    window["-F-PLACA-"].set_focus()
    filas_actuales = _cargar_registros(window)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Cerrar"):
            window.close()
            return True, "Consulta de registros cerrada."

        if event == "-BUSCAR-":
            filtros = {
                "placa": values["-F-PLACA-"],
                "cui": values["-F-CUI-"],
                "nit": values["-F-NIT-"],
                "nombre": values["-F-NOMBRE-"],
                "uso": values["-F-USO-"],
                "tipo": values["-F-TIPO-"],
                "marca": values["-F-MARCA-"],
                "color": values["-F-COLOR-"],
                "no_tarjeta": values["-F-TARJETA-"],
            }
            filas_actuales = _cargar_registros(window, filtros)

        elif event == "-LIMPIAR-":
            for key in (
                "-F-PLACA-",
                "-F-CUI-",
                "-F-NIT-",
                "-F-NOMBRE-",
                "-F-USO-",
                "-F-TIPO-",
                "-F-MARCA-",
                "-F-COLOR-",
                "-F-TARJETA-",
            ):
                window[key].update("")
            filas_actuales = _cargar_registros(window)
        elif event == "-TABLA-" and values["-TABLA-"]:
            indice = values["-TABLA-"][0]
            if 0 <= indice < len(filas_actuales):
                _actualizar_detalle(window, filas_actuales[indice])
