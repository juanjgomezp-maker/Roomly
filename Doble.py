import datetime
import unicodedata
import pickle
import os
from Doble import Doble
from Familiar import Familiar
from Simple import Simple
from Reserva import Reserva
from Usuarios import Usuario

# ===========================================================
# normalizar_respuesta
# ===========================================================

def normalizar_respuesta(texto):
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    texto = texto.strip().lower()
    if texto in ["s", "si"]:
        return "si"
    if texto in ["n", "no"]:
        return "no"
    if texto == "enprogreso":
        return "en progreso"
    return texto

# ===========================================================
# validar_texto
# ===========================================================

def validar_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("Entrada no valida. El valor no puede estar vacio.")

# ===========================================================
# validar_fecha
# ===========================================================

def validar_fecha(mensaje):
    while True:
        try:
            fecha = input(mensaje)
            fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d")
            return fecha
        except ValueError:
            print("Fecha invalida. Por favor, ingrese una fecha en el formato YYYY-MM-DD.")

# ===========================================================
# validar_entero
# ===========================================================

def validar_entero(mensaje):
    while True:
        try:
            num = int(input(mensaje).strip())
            return num
        except ValueError:
            print("Entrada no valida. Por favor, ingrese un numero entero.")


# ===========================================================
# validar_tipo_habitacion
# ===========================================================

def validar_tipo_habitacion(mensaje):
    while True:
        tipo = normalizar_respuesta(input(mensaje))
        if tipo in ["simple", "doble", "familiar"]:
            return tipo
        print("Tipo de habitacion no valida. Por favor, ingrese Simple, Doble o Familiar.")

# ======================================================================================================================
# Gestion de huespedes
# ======================================================================================================================

# ===========================================================
# buscar_usuario
# ===========================================================

def buscar_usuario(usuarios, documento):
    for usuario in usuarios:
        if usuario.get_documento() == documento:
            return usuario
    return None

# ===========================================================
# registrar_huesped
# ===========================================================

def registrar_huesped(usuarios, habitaciones, reservas):
    print("\n=== Registrar nuevo huesped ===")
    documento = validar_texto("Documento: ")
    usuario_existente = buscar_usuario(usuarios, documento)
    if usuario_existente:
        print("Ya existe un huesped con ese documento.")
        return usuario_existente

    nombre = validar_texto("Nombre: ")
    telefono = validar_texto("Telefono: ")
    usuario = Usuario(nombre, documento, telefono)
    usuarios.append(usuario)
    print(f"Huesped registrado: {nombre}")
    return usuario


def mostrar_huespedes(usuarios):
    print("\n=== Huespedes registrados ===")
    if not usuarios:
        print("No hay huespedes registrados.")
        return
    for usuario in usuarios:
        print(f"{usuario.get_documento()} - {usuario.get_nombre()} - {usuario.get_telefono()}")

# ===========================================================
# menu_huespedes
# ===========================================================

def menu_huespedes(usuarios, habitaciones, reservas):
    while True:
        print("\n--- Gestion de huespedes ---")
        print("1. Registrar nuevo huesped")
        print("2. Ver huespedes registrados")
        print("3. Volver")
        opcion = validar_entero("Seleccione una opcion: ")
        if opcion == 1:
            registrar_huesped(usuarios, habitaciones, reservas)
        elif opcion == 2:
            mostrar_huespedes(usuarios)
        elif opcion == 3:
            break
        else:
            print("Opcion no valida.")

# ======================================================================================================================
# Gestion de habitaciones
# ======================================================================================================================

# ===========================================================
# mostrar_habitacion
# ===========================================================

def mostrar_habitacion(habitacion):
    print(
        f"Habitacion {habitacion.get_numero()} - Piso {habitacion.get_piso()} - Tipo {habitacion.get_tipo()} - "
        f"Capacidad {habitacion.get_capacidad()} - Precio {habitacion.get_precio()}$ - "
        f"Disponible {'Si' if habitacion.get_disponible() else 'No'}"
    )


def mostrar_habitaciones(habitaciones):
    print("\n=== Habitaciones registradas ===")
    if not habitaciones:
        print("No hay habitaciones registradas.")
        return
    for habitacion in habitaciones:
        mostrar_habitacion(habitacion)

# ===========================================================
# crear_habitacion
# ===========================================================

def crear_habitacion(habitaciones, reservas, usuarios):
    print("\n=== Crear nueva habitacion ===")
    numero = validar_entero("Numero de habitacion: ")
    if any(h.get_numero() == numero for h in habitaciones):
        print("Ya existe una habitacion con ese numero.")
        return
    piso = validar_entero("Piso: ")
    tipo = validar_tipo_habitacion("Tipo (Simple, Doble, Familiar): ")
    if tipo == "simple":
        habitacion = Simple(numero, piso)
    elif tipo == "doble":
        habitacion = Doble(numero, piso)
    else:
        habitacion = Familiar(numero, piso)
    habitaciones.append(habitacion)
    print("Habitacion creada correctamente.")

# ===========================================================
# definir_disponibilidad_habitacion
# ===========================================================

def definir_disponibilidad_habitacion(habitacion, reservas, fecha_entrada, fecha_salida):
    if not habitacion.get_disponible():
        return False
    for reserva in reservas:
        if reserva.get_habitacion() == habitacion:
            if fecha_entrada < reserva.get_fecha_salida() and fecha_salida > reserva.get_fecha_entrada():
                return False
    return True

# ===========================================================
# verificar_disponibilidad_habitacion
# ===========================================================

def verificar_disponibilidad_habitacion(habitaciones, reservas, fecha_entrada, fecha_salida, numero_habitacion):
    for habitacion in habitaciones:
        if habitacion.get_numero() == numero_habitacion:
            return definir_disponibilidad_habitacion(habitacion, reservas, fecha_entrada, fecha_salida)


def mostrar_habitaciones_disponibles(habitaciones, reservas, fecha_entrada, fecha_salida, tipo=None, piso=None):
    disponibles = []
    for habitacion in habitaciones:
        if tipo and habitacion.get_tipo() != tipo:
            continue
        if piso != None and habitacion.get_piso() != piso:
            continue
        if definir_disponibilidad_habitacion(habitacion, reservas, fecha_entrada, fecha_salida):
            disponibles.append(habitacion)

    if not disponibles:
        print("No hay habitaciones disponibles en ese rango de fechas.")
        return
    for habitacion in disponibles:
        mostrar_habitacion(habitacion)

# ===========================================================
# menu_habitaciones
# ===========================================================

def menu_habitaciones(habitaciones, reservas, usuarios):
    while True:
        print("\n--- Gestion de habitaciones ---")
        print("1. Ver todas las habitaciones")
        print("2. Ver habitaciones disponibles")
        print("3. Crear habitacion")
        print("4. Volver")
        opcion = validar_entero("Seleccione una opcion: ")
        if opcion == 1:
            mostrar_habitaciones(habitaciones)
        elif opcion == 2:
            fecha_entrada = validar_fecha("Ingrese la fecha de entrada (YYYY-MM-DD): ")
            fecha_salida = validar_fecha("Ingrese la fecha de salida (YYYY-MM-DD): ")
            if fecha_salida <= fecha_entrada:
                print("La fecha de salida debe ser posterior a la fecha de entrada.")
                continue
            tipo = input("Ingrese tipo de habitacion para filtrar (Simple, Doble, Familiar) o Enter para todas: ").strip()
            if tipo:
                tipo = normalizar_respuesta(tipo)
                if tipo not in ["simple", "doble", "familiar"]:
                    print("Tipo no valido.")
                    continue
            else:
                tipo = None

            piso = None
            while True:
                piso_input = input("Ingrese piso para filtrar o presione enter para todos: ").strip()
                if piso_input == "":
                    break
                if piso_input.isdigit():
                    piso = int(piso_input)
                    break
                print("Entrada no valida. Por favor, ingrese un numero entero o presione enter para omitir.")

            mostrar_habitaciones_disponibles(habitaciones, reservas, fecha_entrada, fecha_salida, tipo, piso)
        elif opcion == 3:
            crear_habitacion(habitaciones, reservas, usuarios)
        elif opcion == 4:
            break
        else:
            print("Opcion no valida.")

# ======================================================================================================================
# Gestion de reservas
# ======================================================================================================================

# ===========================================================
# seleccionar_usuario
# ===========================================================

def seleccionar_usuario(usuarios, habitaciones, reservas):
    while True:
        documento = validar_texto("Ingrese su numero de documento: ")
        usuario = buscar_usuario(usuarios, documento)
        if usuario:
            print(f"Bienvenido de nuevo, {usuario.get_nombre()}!")
            return usuario

        print("Usuario no encontrado.")
        while True:
            respuesta = normalizar_respuesta(input("Desea registrarse? (si/no): "))
            if respuesta in ["si", "no"]:
                break
            print("Respuesta no valida. Por favor, responda si o no.")
        if respuesta == "si":
            return registrar_huesped(usuarios, habitaciones, reservas)
        print("Debe registrarse para continuar con la reserva.")

# ===========================================================
# usuario_reservar_habitacion
# ===========================================================

def usuario_reservar_habitacion(habitaciones, reservas, usuarios):
    print("\n=== Reservar una habitacion ===")
    usuario = seleccionar_usuario(usuarios, habitaciones, reservas)
    if not usuario:
        return

    print("Tenemos las siguientes habitaciones:")
    print("Simple: Precio 50$, Capacidad 1 persona")
    print("Doble: Precio 100$, Capacidad 2 personas")
    print("Familiar: Precio 150$, Capacidad 4 personas")

    tipo_habitacion = validar_tipo_habitacion("Ingrese el tipo de habitacion que desea reservar (Simple, Doble, Familiar): ")
    fecha_entrada = validar_fecha("Ingrese la fecha de entrada (YYYY-MM-DD): ")
    while True:
        fecha_salida = validar_fecha("Ingrese la fecha de salida (YYYY-MM-DD): ")
        if fecha_salida > fecha_entrada:
            break
        print("La fecha de salida debe ser posterior a la fecha de entrada.")

    mostrar_habitaciones_disponibles(habitaciones, reservas, fecha_entrada, fecha_salida, tipo=tipo_habitacion)

    while True:
        numero_habitacion = validar_entero("Ingrese el numero de la habitacion que desea reservar: ")
        habitacion_seleccionada = None
        for habitacion in habitaciones:
            if habitacion.get_numero() == numero_habitacion:
                habitacion_seleccionada = habitacion
                break
        if habitacion_seleccionada and habitacion_seleccionada.get_disponible():
            if verificar_disponibilidad_habitacion(habitaciones, reservas, fecha_entrada, fecha_salida, numero_habitacion):
                reservar_habitacion(habitaciones, reservas, habitacion_seleccionada, usuario.get_documento(), fecha_entrada, fecha_salida)
                break
            print("La habitacion no esta disponible en esas fechas.")
        else:
            print("NNumero de habitacion no valido o habitacion no disponible.")


def reservar_habitacion(habitaciones, reservas, habitacion, id_usuario, fecha_entrada, fecha_salida):
    reserva = Reserva(habitacion, id_usuario, fecha_entrada, fecha_salida)
    reserva.calcular_costo_total(habitacion.get_precio())
    reservas.append(reserva)
    print(f"Reserva realizada para {id_usuario} en la habitacion {habitacion.get_numero()}")
    reserva.mostrar_informacion()

# ===========================================================
# cancelar_reserva
# ===========================================================

def cancelar_reserva(reservas, habitaciones, usuarios):
    print("\n=== Cancelar reserva ===")
    id_usuario = validar_texto("Ingrese su numero de documento para cancelar la reserva: ")
    usuario = buscar_usuario(usuarios, id_usuario)
    if not usuario:
        print("Usuario no encontrado. No se puede cancelar la reserva.")
        return

    fecha_actual = validar_fecha("Ingrese la fecha actual (YYYY-MM-DD): ")
    for reserva in reservas[:]:
        reserva.Set_dias_transcurridos(fecha_actual)
        reserva.set_estado()
        if reserva.get_id_usuario() == id_usuario and reserva.get_estado() == "activa":
            reservas.remove(reserva)
            print(f"Reserva cancelada para {id_usuario} en la habitacion {reserva.get_habitacion().get_numero()}")
            return
        if reserva.get_id_usuario() == id_usuario and reserva.get_estado() == "en progreso":
            print(f"No se puede cancelar la reserva para {usuario.get_nombre()} en la habitacion {reserva.get_habitacion().get_numero()} porque ya esta en progreso.")
            return
        if reserva.get_id_usuario() == id_usuario and reserva.get_estado() == "finalizada":
            print(f"No se puede cancelar la reserva para {usuario.get_nombre()} en la habitacion {reserva.get_habitacion().get_numero()} porque ya ha finalizado.")
            return
    print("No se encontró una reserva activa para el usuario ingresado.")

# ===========================================================
# mostrar_reservas_estado
# ===========================================================

def mostrar_reservas_estado(reservas):
    while True:
        estado = normalizar_respuesta(input("Ingrese el estado de las reservas a mostrar (activa, en progreso, finalizada): "))
        if estado in ["activa", "en progreso", "finalizada"]:
            break
        print("Estado no válido. Por favor, ingrese activa, en progreso o finalizada.")
    fecha_actual = validar_fecha("Ingrese la fecha actual (YYYY-MM-DD): ")
    print(f"\n=== Reservas {estado} ===")
    for reserva in reservas:
        reserva.Set_dias_transcurridos(fecha_actual)
        reserva.set_estado()
        if reserva.get_estado() == estado:
            reserva.mostrar_informacion()


def menu_reservas(habitaciones, reservas, usuarios):
    while True:
        print("\n--- Gestión de reservas ---")
        print("1. Crear reserva")
        print("2. Cancelar reserva")
        print("3. Mostrar reservas por estado")
        print("4. Volver")
        opcion = validar_entero("Seleccione una opción: ")
        if opcion == 1:
            usuario_reservar_habitacion(habitaciones, reservas, usuarios)
        elif opcion == 2:
            cancelar_reserva(reservas, habitaciones, usuarios)
        elif opcion == 3:
            mostrar_reservas_estado(reservas)
        elif opcion == 4:
            break
        else:
            print("Opción no válida.")

# ======================================================================================================================
# mostrar_menu
# ======================================================================================================================
# mostrar_menu
# ===========================================================
# gestion de menus
# ===========================================================


# ===========================================================
# mostrar_menu
# ===========================================================
def mostrar_menu():
    print("\n=== Sistema de reservas del hotel ===")
    print("1. Gestión de huéspedes")
    print("2. Gestión de habitaciones")
    print("3. Gestión de reservas")
    print("4. Salir")

# ===========================================================
# inicializar_habitaciones
# ===========================================================
def inicializar_habitaciones(habitaciones):
    habitaciones.append(Simple(101, 1))
    habitaciones.append(Simple(102, 1))
    habitaciones.append(Doble(103, 1))
    habitaciones.append(Doble(104, 1))
    habitaciones.append(Familiar(105, 1))
    habitaciones.append(Simple(201, 2))
    habitaciones.append(Simple(202, 2))
    habitaciones.append(Doble(203, 2))
    habitaciones.append(Doble(204, 2))
    habitaciones.append(Familiar(205, 2))
    habitaciones.append(Simple(301, 3))
    habitaciones.append(Simple(302, 3))
    habitaciones.append(Doble(303, 3))
    habitaciones.append(Doble(304, 3))
    habitaciones.append(Familiar(305, 3))
    habitaciones.append(Simple(401, 4))
    habitaciones.append(Simple(402, 4))
    habitaciones.append(Doble(403, 4))
    habitaciones.append(Doble(404, 4))
    habitaciones.append(Familiar(405, 4))

# ===========================================================
# main
# ===========================================================

def main():
    habitaciones = []
    reservas = []
    usuarios = []

    ruta = r'C:\Users\HOME\Downloads\proyecto (1)\proyecto\habitaciones.pkl'
    if not os.path.exists(ruta):
        print("Archivo no existe, creando uno nuevo...")
        with open(ruta, 'wb') as f:
            pickle.dump([], f)  # lista vacía como ejemplo
    with open(ruta, 'rb') as f:
        habitaciones = pickle.load(f)
    
    ruta = r'C:\Users\HOME\Downloads\proyecto (1)\proyecto\reservas.pkl'
    if not os.path.exists(ruta):
        print("Archivo no existe, creando uno nuevo...")
        with open(ruta, 'wb') as f:
            pickle.dump([], f)  # lista vacía como ejemplo
    with open(ruta, 'rb') as f:
        reservas = pickle.load(f)
    
    ruta = r'C:\Users\HOME\Downloads\proyecto (1)\proyecto\usuarios.pkl'
    if not os.path.exists(ruta):
        print("Archivo no existe, creando uno nuevo...")
        with open(ruta, 'wb') as f:
            pickle.dump([], f)  # lista vacía como ejemplo
    with open(ruta, 'rb') as f:
        usuarios = pickle.load(f)
    
    if not habitaciones:
        inicializar_habitaciones(habitaciones)

    while True:
        mostrar_menu()
        opcion = validar_entero("Seleccione una opción: ")
        if opcion == 1:
            menu_huespedes(usuarios, habitaciones, reservas)
        elif opcion == 2:
            menu_habitaciones(habitaciones, reservas, usuarios)
        elif opcion == 3:
            menu_reservas(habitaciones, reservas, usuarios)
        elif opcion == 4:
            print("Gracias por usar el sistema de reservas del hotel. ¡Hasta luego!")
            with open(r'C:\Users\HOME\Downloads\proyecto (1)\proyecto\habitaciones.pkl', "wb") as f:
                pickle.dump(habitaciones, f)
            with open(r'C:\Users\HOME\Downloads\proyecto (1)\proyecto\reservas.pkl', "wb") as f:
                pickle.dump(reservas, f)
            with open(r'C:\Users\HOME\Downloads\proyecto (1)\proyecto\usuarios.pkl', "wb") as f:
                pickle.dump(usuarios, f)
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del 1 al 4.")


if __name__ == "__main__":
    main()
