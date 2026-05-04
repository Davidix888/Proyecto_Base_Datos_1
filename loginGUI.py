import PySimpleGUI as sg

from gui_helpers import actualizar_mensaje, aplicar_tema, crear_layout_login
from login import validar_inicio_sesion
from operator_views import abrir_panel_operador


aplicar_tema()


def cargar_resumen_roles(window):
    actualizar_mensaje(
        window,
        "-ROLES-",
        "Flujo unificado: cualquier usuario valido accede al panel operativo.",
        "#d9ead3",
    )



def main():
    window = sg.Window(
        "Sistema de tarjetas de circulacion",
        crear_layout_login(),
        size=(700, 430),
        resizable=False,
        element_justification="center",
        finalize=True,
        margins=(18, 16),
    )
    window["-USER-"].set_focus()
    cargar_resumen_roles(window)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Salir"):
            break

        if event == "Iniciar sesion":
            nombre_usuario = values["-USER-"].strip()
            contrasena = values["-PASS-"].strip()

            if not nombre_usuario or not contrasena:
                actualizar_mensaje(
                    window,
                    "-MSG-",
                    "Por favor, ingresa usuario y contrasena.",
                    "#ffd966",
                )
                continue

            try:
                usuario = validar_inicio_sesion(nombre_usuario, contrasena)
            except Exception as error:
                actualizar_mensaje(
                    window,
                    "-MSG-",
                    f"Error al consultar la base: {error}",
                    "#ffb3b3",
                )
                continue

            if not usuario:
                actualizar_mensaje(
                    window,
                    "-MSG-",
                    "Usuario o contrasena incorrectos.",
                    "#ffb3b3",
                )
                window["-PASS-"].update("")
                continue

            id_usuario, _rol = usuario

            actualizar_mensaje(window, "-MSG-", "", "#ffd966")
            window.hide()
            abrir_panel_operador(id_usuario, nombre_usuario)

            window.un_hide()
            window["-USER-"].update("")
            window["-PASS-"].update("")
            window["-USER-"].set_focus()
            actualizar_mensaje(window, "-MSG-", "Sesion cerrada.", "#d9ead3")

    window.close()


if __name__ == "__main__":
    main()
