import PySimpleGUI as sg

from gui_helpers import (
    COLORES,
    FUENTE_SECCION,
    FUENTE_TEXTO,
    actualizar_mensaje,
    boton_peligro,
    boton_secundario,
    crear_encabezado,
)
from registro_view import abrir_visor_registros


def abrir_panel_consultor(id_usuario, nombre_usuario):
    layout = [
        *crear_encabezado(
            "Panel de consultor",
            "Consulta la informacion registrada sin alterar los datos del sistema.",
        ),
        [sg.Text("")],
        [
            sg.Frame(
                "Sesion actual",
                [
                    [sg.Text("Usuario", size=(12, 1), font=FUENTE_TEXTO), sg.Text(nombre_usuario, font=FUENTE_SECCION)],
                    [sg.Text("Rol", size=(12, 1), font=FUENTE_TEXTO), sg.Text("CONSULTOR", font=FUENTE_SECCION, text_color=COLORES["primario"])],
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
                "Consultas disponibles",
                [
                    [boton_secundario("Consultar propietario", size=(26, 1))],
                    [boton_secundario("Consultar vehiculo", size=(26, 1))],
                    [boton_secundario("Consultar tarjeta", size=(26, 1))],
                    [boton_secundario("Consultar registros", size=(26, 1))],
                ],
                title_color=COLORES["primario_oscuro"],
                font=FUENTE_SECCION,
                border_width=1,
                relief=sg.RELIEF_SOLID,
                pad=((10, 10), (0, 8)),
            )
        ],
        [sg.Text("", key="-MSG-CONSULTOR-", size=(52, 2), justification="center", font=FUENTE_TEXTO)],
        [boton_peligro("Cerrar sesion", size=(16, 1))],
    ]

    window = sg.Window(
        "Panel de Consultor",
        layout,
        size=(520, 450),
        modal=True,
        element_justification="center",
        margins=(18, 16),
    )

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Cerrar sesion"):
            break

        if event == "Consultar propietario":
            exito, mensaje = abrir_visor_registros(
                "CONSULTOR",
                nombre_usuario,
                modo="propietario",
            )
            color = COLORES["exito"] if exito else COLORES["alerta"]
            actualizar_mensaje(window, "-MSG-CONSULTOR-", mensaje, color)
        elif event == "Consultar vehiculo":
            exito, mensaje = abrir_visor_registros(
                "CONSULTOR",
                nombre_usuario,
                modo="vehiculo",
            )
            color = COLORES["exito"] if exito else COLORES["alerta"]
            actualizar_mensaje(window, "-MSG-CONSULTOR-", mensaje, color)
        elif event == "Consultar tarjeta":
            exito, mensaje = abrir_visor_registros(
                "CONSULTOR",
                nombre_usuario,
                modo="tarjeta",
            )
            color = COLORES["exito"] if exito else COLORES["alerta"]
            actualizar_mensaje(window, "-MSG-CONSULTOR-", mensaje, color)
        elif event == "Consultar registros":
            exito, mensaje = abrir_visor_registros("CONSULTOR", nombre_usuario)
            color = COLORES["exito"] if exito else COLORES["alerta"]
            actualizar_mensaje(window, "-MSG-CONSULTOR-", mensaje, color)

    window.close()
