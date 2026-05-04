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
from login import registrar_propietario
from mantenimiento_view import abrir_mantenimiento_tarjeta
from registro_view import abrir_visor_registros
from tarjeta_circulacion_view import abrir_formulario_tarjeta_circulacion


def abrir_formulario_propietario():
    layout = [
        *crear_encabezado(
            "Registrar propietario",
            "Ingresa los datos basicos del propietario para dejarlo disponible en el sistema.",
        ),
        [sg.Text("")],
        [
            sg.Frame(
                "Datos del propietario",
                [
                    [sg.Text("CUI", size=(12, 1), font=FUENTE_TEXTO), sg.Input(key="-CUI-", size=(28, 1), font=FUENTE_TEXTO)],
                    [sg.Text("NIT", size=(12, 1), font=FUENTE_TEXTO), sg.Input(key="-NIT-", size=(28, 1), font=FUENTE_TEXTO)],
                    [sg.Text("Nombre", size=(12, 1), font=FUENTE_TEXTO), sg.Input(key="-NOMBRE-", size=(28, 1), font=FUENTE_TEXTO)],
                ],
                title_color=COLORES["primario_oscuro"],
                font=FUENTE_SECCION,
                border_width=1,
                relief=sg.RELIEF_SOLID,
                pad=((12, 12), (0, 8)),
            )
        ],
        [sg.Text("", key="-MSG-PROPIETARIO-", size=(48, 2), justification="center", font=FUENTE_TEXTO)],
        [boton_primario("Guardar", size=(12, 1), bind_return_key=True), boton_secundario("Cancelar", size=(12, 1))],
    ]

    window = sg.Window(
        "Registrar propietario",
        layout,
        size=(520, 320),
        modal=True,
        finalize=True,
        element_justification="center",
        margins=(18, 16),
    )
    window["-CUI-"].set_focus()

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Cancelar"):
            window.close()
            return False, "Registro de propietario cancelado."

        if event == "Guardar":
            exito, mensaje = registrar_propietario(
                values["-CUI-"],
                values["-NIT-"],
                values["-NOMBRE-"],
            )
            color = "#d9ead3" if exito else "#ffb3b3"
            actualizar_mensaje(window, "-MSG-PROPIETARIO-", mensaje, color)

            if exito:
                window.close()
                return True, mensaje


def abrir_panel_operador(id_usuario, nombre_usuario):
    layout = [
        *crear_encabezado(
            "Panel operativo",
            "Gestiona propietarios, tarjetas, mantenimiento y consultas del sistema.",
        ),
        [sg.Text("")],
        [
            sg.Frame(
                "Sesion actual",
                [
                    [sg.Text("Usuario", size=(12, 1), font=FUENTE_TEXTO), sg.Text(nombre_usuario, font=FUENTE_SECCION)],
                    [sg.Text("Acceso", size=(12, 1), font=FUENTE_TEXTO), sg.Text("OPERATIVO", font=FUENTE_SECCION, text_color=COLORES["primario"])],
                    [sg.Text("ID", size=(12, 1), font=FUENTE_TEXTO), sg.Text(str(id_usuario), font=FUENTE_TEXTO)],
                ],
                title_color=COLORES["primario_oscuro"],
                font=FUENTE_SECCION,
                border_width=1,
                relief=sg.RELIEF_SOLID,
                pad=((10, 10), (0, 8)),
            )
        ],
        [
            sg.Frame(
                "Acciones disponibles",
                [
                    [boton_primario("Registrar propietario", size=(26, 1))],
                    [boton_primario("Registrar tarjeta y vehiculo", size=(26, 1))],
                    [boton_secundario("Mantenimiento de tarjeta", size=(26, 1))],
                    [boton_secundario("Ver registros", size=(26, 1))],
                ],
                title_color=COLORES["primario_oscuro"],
                font=FUENTE_SECCION,
                border_width=1,
                relief=sg.RELIEF_SOLID,
                pad=((10, 10), (0, 8)),
            )
        ],
        [sg.Text("", key="-MSG-OPERADOR-", size=(52, 2), justification="center", font=FUENTE_TEXTO)],
        [boton_peligro("Cerrar sesion", size=(16, 1))],
    ]

    window = sg.Window(
        "Panel Operativo",
        layout,
        size=(520, 430),
        modal=True,
        element_justification="center",
        margins=(18, 16),
    )

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Cerrar sesion"):
            break

        if event == "Registrar propietario":
            exito, mensaje = abrir_formulario_propietario()
            color = "#d9ead3" if exito else "#ffd966"
            actualizar_mensaje(window, "-MSG-OPERADOR-", mensaje, color)
        elif event == "Registrar tarjeta y vehiculo":
            exito, mensaje = abrir_formulario_tarjeta_circulacion(
                id_usuario, nombre_usuario
            )
            color = "#d9ead3" if exito else "#ffd966"
            actualizar_mensaje(window, "-MSG-OPERADOR-", mensaje, color)
        elif event == "Mantenimiento de tarjeta":
            exito, mensaje = abrir_mantenimiento_tarjeta(id_usuario, nombre_usuario)
            color = COLORES["exito"] if exito else COLORES["alerta"]
            actualizar_mensaje(window, "-MSG-OPERADOR-", mensaje, color)
        elif event == "Ver registros":
            exito, mensaje = abrir_visor_registros("OPERADOR", nombre_usuario)
            color = COLORES["exito"] if exito else COLORES["alerta"]
            actualizar_mensaje(window, "-MSG-OPERADOR-", mensaje, color)

    window.close()
