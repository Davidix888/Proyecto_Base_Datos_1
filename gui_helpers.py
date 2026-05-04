import PySimpleGUI as sg


FUENTE_TITULO = ("Segoe UI", 20, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 10)
FUENTE_SECCION = ("Segoe UI", 11, "bold")
FUENTE_TEXTO = ("Segoe UI", 10)
FUENTE_BOTON = ("Segoe UI", 10, "bold")

COLORES = {
    "primario": "#0E7A57",
    "primario_oscuro": "#8EDCC1",
    "acento": "#5DBB91",
    "fondo": "#061612",
    "superficie": "#102723",
    "borde": "#1B3B35",
    "texto": "#EAF3F0",
    "texto_suave": "#A4BBB5",
    "exito": "#76D672",
    "alerta": "#E2B93B",
    "error": "#F06A78",
    "peligro": "#8B1E1E",
    "boton_secundario": "#183A34",
}


def aplicar_tema():
    if "TarjetaProfesional" not in sg.theme_list():
        sg.theme_add_new(
            "TarjetaProfesional",
            {
                "BACKGROUND": COLORES["fondo"],
                "TEXT": COLORES["texto"],
                "INPUT": COLORES["superficie"],
                "TEXT_INPUT": COLORES["texto"],
                "SCROLL": COLORES["superficie"],
                "BUTTON": ("white", COLORES["primario"]),
                "PROGRESS": ("#D1826B", "#CC8019"),
                "BORDER": 1,
                "SLIDER_DEPTH": 0,
                "PROGRESS_DEPTH": 0,
            },
        )
    sg.theme("TarjetaProfesional")


def crear_encabezado(titulo, subtitulo):
    return [
        [
            sg.Text(
                titulo,
                font=FUENTE_TITULO,
                text_color=COLORES["primario_oscuro"],
                justification="center",
                expand_x=True,
            )
        ],
        [
            sg.Text(
                subtitulo,
                font=FUENTE_SUBTITULO,
                text_color=COLORES["texto_suave"],
                justification="center",
                expand_x=True,
            )
        ],
    ]


def boton_primario(texto, key=None, size=(18, 1), bind_return_key=False):
    return sg.Button(
        texto,
        key=key,
        size=size,
        font=FUENTE_BOTON,
        bind_return_key=bind_return_key,
        button_color=("white", COLORES["primario"]),
        border_width=0,
    )


def boton_secundario(texto, key=None, size=(14, 1)):
    return sg.Button(
        texto,
        key=key,
        size=size,
        font=FUENTE_BOTON,
        button_color=("white", COLORES["boton_secundario"]),
        border_width=0,
    )


def boton_peligro(texto, key=None, size=(14, 1)):
    return sg.Button(
        texto,
        key=key,
        size=size,
        font=FUENTE_BOTON,
        button_color=("white", COLORES["peligro"]),
        border_width=0,
    )


def crear_layout_login():
    return [
        *crear_encabezado(
            "Sistema de tarjetas de circulacion",
            "Accede con tu usuario para ingresar al panel segun tu rol.",
        ),
        [sg.Text("")],
        [
            sg.Frame(
                "Acceso al sistema",
                [
                    [
                        sg.Text("Usuario", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(key="-USER-", size=(30, 1), font=FUENTE_TEXTO),
                    ],
                    [
                        sg.Text("Contrasena", size=(12, 1), font=FUENTE_TEXTO),
                        sg.Input(
                            password_char="*",
                            key="-PASS-",
                            size=(30, 1),
                            font=FUENTE_TEXTO,
                        ),
                    ],
                    [
                        boton_primario(
                            "Iniciar sesion",
                            size=(16, 1),
                            bind_return_key=True,
                        ),
                        boton_secundario("Salir", size=(12, 1)),
                    ],
                ],
                title_color=COLORES["primario_oscuro"],
                font=FUENTE_SECCION,
                pad=((20, 20), (6, 10)),
                border_width=1,
                relief=sg.RELIEF_SOLID,
            )
        ],
        [
            sg.Frame(
                "Roles detectados",
                [
                    [
                        sg.Text(
                            "",
                            key="-ROLES-",
                            size=(60, 2),
                            justification="center",
                            text_color=COLORES["texto_suave"],
                            font=FUENTE_TEXTO,
                        )
                    ]
                ],
                title_color=COLORES["primario_oscuro"],
                font=FUENTE_SECCION,
                border_width=1,
                relief=sg.RELIEF_SOLID,
                pad=((20, 20), (0, 8)),
            )
        ],
        [
            sg.Text(
                "",
                key="-MSG-",
                size=(60, 2),
                justification="center",
                text_color=COLORES["texto_suave"],
                font=FUENTE_TEXTO,
            )
        ],
    ]


def actualizar_mensaje(window, key, mensaje, color):
    window[key].update(mensaje, text_color=color)
