import os


def limpiar_pantalla():
    """Limpio la pantalla."""
    # Detecto si el so es linux
    if os.name == "posix":
        print()
        input("Presione enter para limpiar...")
        os.system("clear")
    # Detecto si el so es Windows
    if os.name == "nt":
        print()

        input("Presione enter para limpiar..")
        os.system("cls")


def cartel():
    """Procedimiento que muestra un cartel con opciones"""
    print("1- Realizar consulta de saldo de cualquier cuenta")
    print("2- Hacer ABM(Alta-Baja-Modificacion)")
    print("3- Info cuenta/cajero")
    print("0- Para salir")


def cartel_abm():
    """Mostramos las opciones del submenu ABM"""
    print("1- Dar de alta una cuenta")
    print("2- Dar de baja una cuenta")
    print("3- Modificar una cuenta")
    print("0- Salir")


"""2) Procesar el archivo de movimientos, utilizando la técnica de corte de control, para:

C) Actualizar el saldo de las cuentas en CUENTAS.
D) Actualizar la cantidad de movimientos de cada cajero en CAJEROS"""


def cartel_info_cuentas():
    """Mostramos las opciones del submenu de info_cuentas"""
    print("1- total anual en pesos ($) de los movimientos de cada una de las cuentas.")
    print(
        "2- Informar que cajero registró mayor cantidad de movimientos durante el año."
    )


def validacion(entrada):
    """Se valida que el valor ingresado no sea menor que 1000"""
    while entrada < 1000:
        print("Solo se admiten valores de cuatro digitos, reintente.")
        limpiar_pantalla()
        entrada = int(input("Ingrese Nro Cuenta: "))
        limpiar_pantalla()
    return entrada


def opciones(op) -> int:
    """Realiza una validación del input del usuario, reintentando las veces necesarias y retornando el valor correcto."""

    usuario = int(input("Escoge una opción: "))
    limpiar_pantalla()
    while usuario < 0 or usuario > op:
        print("Opción incorrecta, intente nuevamente")
        cartel()
        usuario = int(input("Escoge una opción: "))
        limpiar_pantalla()

    return usuario


def cant_real(vec_cuentas, capacidad_nuevas_cuentas) -> int:
    """Se toma como parámetro un vector, se calcula la cantidad real y se retorna."""
    # Establecemos la cantidad real.
    cantidad_real = len(vec_cuentas) - capacidad_nuevas_cuentas

    return cantidad_real


def validacion_tipo_cuenta(entrada) -> int:
    """Se retorna el valor del nro de cuenta validado."""
    while entrada < 1 or entrada > 15:
        print("Opcion incorrecta, rango de valores admitidos: [1-15]")
        limpiar_pantalla()
        entrada = int(input("Ingrese un nro de cuenta: "))
        limpiar_pantalla()
    return entrada
