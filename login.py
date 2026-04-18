import psycopg

# Conexión a la base de datos
conexion = psycopg.connect(
        host="localhost",
        port="5432",
        dbname="proyecto_tarjeta_circulacion",
        user="postgres",
        password="Cruzita_2005"
    )

#Nombre y contraseña del usuario para iniciar sesión
nombre_usuario = "ldixquiac"
contraseña = "Cruzita_2005"

# Consulta para verificar el nombre de usuario y contraseña
cur = conexion.cursor()
cur.execute("""SELECT id_usuario, rol
               FROM usuario
               WHERE nombre_usuario = %s AND contraseÑa = %s""",
            (nombre_usuario, contraseña))

# Obtener el resultado de la consulta
usuario = cur.fetchone()

#Revisar si existe el usuario
if usuario:
    print("Bienvenido")
    print(usuario)

else:
    print("Usuario o contraseña incorrectos")

#Cerrar la conexión a la base de datos
cur.close()
conexion.close()