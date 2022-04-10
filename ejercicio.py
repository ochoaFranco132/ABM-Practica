"""
Una entidad bancaria tiene organizada su información en los siguientes vectores de registros:
CUENTAS datos de los clientes
CAJEROS datos de los cajeros automáticos

“CUENTAS”
Numero_cuenta: Integer;
Apellido: String [50];
Nombre: String [50];
DNI: String [8]
Tipo_Cuenta:(1 al 15): Integer
Saldo: Real;
Activa: Booleano (True=Activa, False=Inactiva dada de baja)

Numero_cajero: Integer;(1 al 120)
Ubicacion: String [50];
Cant_mov: Integer;(Cantidad histórica de movimientos)

1) Realizar consulta de saldo de cualquier cuenta, ingresando por teclado el número de cuenta.

2) Procesar el archivo de movimientos, utilizando la técnica de corte de control, para:
A) Informar el total anual (en $) de los movimientos de cada una de las cuentas.
B) Informar que cajero registró mayor cantidad de movimientos durante el año.
C) Actualizar el saldo de las cuentas en CUENTAS.
D) Actualizar la cantidad de movimientos de cada cajero en CAJEROS

3) Realizar ABM sobre CUENTAS
A Altas de nuevas cuentas
B Borrado de cuentas, solo se pone Activa en False
M Modificaciones como Apellido, Nombre, DNI y Tipo de cuenta
- Considerar que cada cliente puede tener solamente 1 cuenta en el banco. Al realizar un alta
debe verificarse que no exista una cuenta activa para el mismo DNI.
- La numeración de las nuevas cuentas debe ser consecutiva"""

import numpy as np
from pyrecord import Record
from utilidades import *


# Creacion de registro.
Rcuentas = Record.create_type(
    "Rcuentas",
    "nro_cuenta",
    "apellido",
    "nombre",
    "dni",
    "tipo_cuenta",
    "saldo",
    "activa",
    nro_cuenta=0,
    apellido="",
    nombre="",
    dni="",
    tipo_cuenta=0,
    saldo=0.0,
    activa=True,
)

Rcajero = Record.create_type(
    "Rcajero",
    "num_cajero",
    "ubicacion",
    "cant_mov",
    num_cajero=0,
    ubicacion="",
    cant_mov=0,
)


def carga(vec_cuentas, vec_cajeros):
    """Cargo dos Vectores a partir de un archivo de cuentas y un archivo cajeros."""
    # Abrimos los archivos a leer.
    archivo_cuentas = open("cuentas.txt", "r")
    archivo_cajeros = open("cajeros.txt", "r")
    # Leer las lineas de los archivos.
    linea_cuentas = archivo_cuentas.readline().strip()
    linea_cajeros = archivo_cajeros.readline().strip()
    # Indices de los vectores.
    c_cuentas = 0
    c_cajeros = 0
    # Comprobamos que termine de leer cuando en ambos casos haya una linea vacia.
    while linea_cuentas != "" or linea_cajeros != "":
        separador_cuentas = linea_cuentas.split(",")
        separador_cajeros = linea_cajeros.split(",")
        # Primeramente trabajamos con cuentas.txt y su respectivo vector.
        if linea_cuentas != "":
            nro_cuenta = int(separador_cuentas[0])
            apellido = separador_cuentas[1]
            nombre = separador_cuentas[2]
            dni = separador_cuentas[3]
            tipo_cuenta = int(separador_cuentas[4])
            saldo = float(separador_cuentas[5])
            activa = bool(separador_cuentas[6])
            # Cargamos el vector.
            vec_cuentas[c_cuentas] = Rcuentas()
            vec_cuentas[c_cuentas].nro_cuenta = nro_cuenta
            vec_cuentas[c_cuentas].apellido = apellido
            vec_cuentas[c_cuentas].nombre = nombre
            vec_cuentas[c_cuentas].dni = dni
            vec_cuentas[c_cuentas].tipo_cuenta = tipo_cuenta
            vec_cuentas[c_cuentas].saldo = saldo
            vec_cuentas[c_cuentas].activa = activa

            # Incrementamos el indice cuentas.
            c_cuentas += 1
            # Volvemos a leer.
            linea_cuentas = archivo_cuentas.readline().strip()

        # Hacemos lo mismo con cajeros.txt verificando que no sea una linea vacia.
        if linea_cajeros != "":
            num_cajero = int(separador_cajeros[0])
            ubicacion = separador_cajeros[1]
            cant_mov = int(separador_cajeros[2])
            # Cargamos el vector.
            vec_cajeros[c_cajeros] = Rcajero()
            vec_cajeros[c_cajeros].num_cajero = num_cajero
            vec_cajeros[c_cajeros].ubicacion = ubicacion
            vec_cajeros[c_cajeros].cant_mov = cant_mov
            # Incrementamos el indice
            c_cajeros += 1
            # Volvemos a leer.
            linea_cajeros = archivo_cajeros.readline().strip()

    archivo_cuentas.close()
    archivo_cajeros.close()


def consulta(vec_cuenta):
    """Pedimos por teclado un valor para acceder"""
    entrada = int(input("Ingrese Nro Cuenta: "))
    limpiar_pantalla()
    # Validamos la entrada
    entrada = validacion(entrada)
    # Restamos 1000 para emparentar el número de cuenta con el valor real del dvector.
    entrada -= 1000
    print(f"Nro cuenta: {vec_cuenta[entrada].nro_cuenta}")
    print(f"Apellido: {vec_cuenta[entrada].apellido}")
    print(f"Nombre: {vec_cuenta[entrada].nombre}")
    print(f"DNI: {vec_cuenta[entrada].dni}")
    print(f"Tipo de Cuenta: {vec_cuenta[entrada].tipo_cuenta}")
    print(f"Saldo: {vec_cuenta[entrada].saldo}")
    print(f"Activa: {vec_cuenta[entrada].activa}")


def bajas(vec_cuenta):
    """Se da de baja una cuenta."""
    cuenta_a_suspender = int(input("Ingrese el Nro de Cuenta a Suspender: "))
    # Validamos la entrada
    validacion(cuenta_a_suspender)
    cuenta_a_suspender -= 1000
    if vec_cuenta[cuenta_a_suspender].activa == True:
        vec_cuenta[cuenta_a_suspender].activa = False
        # Mostramos los datos del usuario.
        print(f"Nro cuenta: {vec_cuenta[cuenta_a_suspender].nro_cuenta}")
        print(f"Apellido: {vec_cuenta[cuenta_a_suspender].apellido}")
        print(f"Nombre: {vec_cuenta[cuenta_a_suspender].nombre}")
        print(f"DNI: {vec_cuenta[cuenta_a_suspender].dni}")
        print(f"Saldo: {vec_cuenta[cuenta_a_suspender].saldo}")
        print(f"Estado de Cuenta: {vec_cuenta[cuenta_a_suspender].activa}")
        print("Cuenta Suspendida")
    else:
        print("la Cuenta ya se encuentra suspendida")


def altas(vec_cuentas, cap_nuevas_cuentas) -> bool:
    """Damos de alta una nueva cuenta, si es que esta no existe. y retorna True si la cuenta existe y False en caso contrario."""
    ingreso_dni = input("Ingrese su DNI: ")
    while len(ingreso_dni) != 8:
        ingreso_dni = input("DNI no válido, ingréselo nuevamente: ")
    contador = 0
    encontrado = False
    cant_util = cant_real(vec_cuentas, cap_nuevas_cuentas)
    # Buscar el dni
    while contador < cant_util and not encontrado:
        if ingreso_dni == vec_cuentas[contador].dni:
            # Comprobar si la cuenta está activada.
            if vec_cuentas[contador].activa:
                print("Tu cuenta está habilitada")
                encontrado = True
            # Si no lo está, preguntas si quiere activarla.
            else:
                opcion = int(input("¿Desea activar su cuenta?: 1- si, 2 no : "))
                if opcion == 1:
                    vec_cuentas[contador].activa = True
                    encontrado = True
                    print("Cuenta activada satisfactoriamente!")
        # Incremento el índice en cada vuelta.
        contador += 1
    # Sino encontramos el DNI, lo creamos.
    if not encontrado:
        print("Siga los pasos para crear su cuenta")
        cant_util = cant_real(vec_cuentas, cap_nuevas_cuentas)

        vec_cuentas[cant_util] = Rcuentas()
        vec_cuentas[cant_util].nro_cuenta = 1000 + cant_util
        vec_cuentas[cant_util].apellido = input("Ingrese su apellido: ")
        vec_cuentas[cant_util].nombre = input("Ingrese su nombre: ")
        vec_cuentas[cant_util].dni = ingreso_dni
        vec_cuentas[cant_util].tipo_cuenta = int(input("Ingrese su tipo de cuenta: "))
        vec_cuentas[cant_util].saldo = 0.0
        vec_cuentas[cant_util].activa = True

        print(
            f"Su cuenta se ha creado satisfactoriamente. numero {vec_cuentas[cant_util].nro_cuenta}"
        )

    return encontrado


# Modificaciones como Apellido, Nombre, DNI y Tipo de cuenta
def modificaciones(vec_cuentas):
    """Se le pide al usuario que realice una modificación de sus datos."""
    # Pedimos y valimos el input del usuario.
    cuenta_a_modificar = int(input("Ingrese el nro de cuenta a modificar: "))
    cuenta_a_modificar = validacion(cuenta_a_modificar)
    cuenta_a_modificar -= 1000

    ejecutar = True
    while ejecutar:
        print("1- Modificar Apellido")
        print("2- Modificar Nombre")
        print("3- Modificar DNI")
        print("4- Modificar Tipo de cuenta")
        print("0- Salir.")

        opcion = opciones(4)
        if opcion == 1:
            vec_cuentas[cuenta_a_modificar].apellido = input("Ingrese su apelldo: ")
            print("Apellido modificado correctamente.")
            limpiar_pantalla()
        elif opcion == 2:
            vec_cuentas[cuenta_a_modificar].nombre = input("Ingrese el nombre: ")
            print("Nombre modificado correctamente")
            limpiar_pantalla()
        elif opcion == 3:
            vec_cuentas[cuenta_a_modificar].dni = input("Ingrese el DNI: ")
            while len(vec_cuentas[cuenta_a_modificar].dni) != 8:
                vec_cuentas[cuenta_a_modificar].dni = input(
                    "Dato inválido, ingrese nuevamente: "
                )
            print("DNI modificado correctamente.")
            limpiar_pantalla()
        elif opcion == 4:
            vec_cuentas[cuenta_a_modificar].tipo_cuenta = int(
                input("Ingrese el tipo de cuenta: ")
            )
            # Proceso de validación de los datos.
            vec_cuentas[cuenta_a_modificar].tipo_cuenta = validacion_tipo_cuenta(
                vec_cuentas[cuenta_a_modificar].tipo_cuenta
            )
            print("Apellido modificado correctamente.")
        else:
            ejecutar = False


def info_cuentas(vec_cuentas, vec_cajeros, vec_caj_may, eleccion):
    """Informa el total anual de los movimientos de cada cuenta.
    Informa que cajero registró mayor cantidad de movimientos durante el año.
    Actualiza el saldo de las cuentas en CUENTAS.
    Actualiza la cantidad de movimientos de cada cajero en CAJEROS
    """
    # Abrimos el archivo para leerlo.
    archivo_cuentas = open("operaciones.txt", "r")
    # Leemos una linea.
    linea = archivo_cuentas.readline().strip()
    # Dividimos la línea en un vector, para trabajar con sus elementos.
    separador = linea.split(",")
    # # Traemos el nro de cuenta a una variable.
    num_cuenta = int(separador[0])
    # Variables para detectar el cajero con más movimientos en el año.
    mayor = 0
    num_mayor = 0
    # Comprobamos que no lea una linea vacia.
    while linea != "":
        # Seteamos el valor inicial del total de la cuenta.
        total = 0
        # Creamos un backup del nro de cuenta para aplicar el corte.
        cuenta_ant = num_cuenta
        # Corte de control
        while linea != "" and cuenta_ant == num_cuenta:
            tipo_extraccion = int(separador[5])
            num_cajero = int(separador[4])
            # Incrementamos en 1 cada movimiento del cajero.
            vec_caj_may[num_cajero - 1] += 1
            # Comprobamos el tipo de extracción para poder operar.
            if tipo_extraccion == 1:
                total += float(separador[6])
            elif tipo_extraccion == 2:
                total -= float(separador[6])
            # Volvemos a leer.
            linea = archivo_cuentas.readline().strip()
            if linea != "":
                separador = linea.split(",")
                num_cuenta = int(separador[0])

        # Actualizamos la cuenta del usuario con el saldo total.
        # Falta implementar un menu que ejecute las opciones de abajo.
        vec_cuentas[cuenta_ant - 1000].saldo += total
        if eleccion == 1:
            print(vec_cuentas[cuenta_ant - 1000].saldo)
            print(f"Saldo de la cuenta: {cuenta_ant - 1000} \n")

    if eleccion == 2:
        for i in range(len(vec_cajeros) - 1):
            vec_cajeros[i].cant_mov += vec_caj_may[i]
            if vec_caj_may[i] > mayor:
                mayor = vec_caj_may[i]
                num_mayor = i + 1
        print(f"El mayor: Cajero {num_mayor} con {mayor} movimientos en el año")


def menu(vec_cuentas, vec_cajeros, vec_caj_may):
    """Muestra un menu."""
    ejecutar = True
    while ejecutar:
        cartel()
        eleccion = opciones(3)
        if eleccion == 1:
            consulta(vec_cuentas)
            limpiar_pantalla()
        elif eleccion == 2:
            menu_abm(vec_cuentas)
            limpiar_pantalla()

        elif eleccion == 3:
            cartel_info_cuentas()
            op = opciones(2)
            info_cuentas(vec_cuentas, vec_cajeros, vec_caj_may, op)
            limpiar_pantalla()
        else:
            ejecutar = False
            print("Adios.")


def menu_abm(vec_cuentas):
    """Muestra el submenu de ABM (altas, bajas, modificaciones)"""
    ejecutar = True
    # Capacidad de nuevas cuentas.
    capacidad_nuevas_cuentas = 10
    while ejecutar:
        cartel_abm()
        eleccion = opciones(3)
        if eleccion == 1:
            dni_registrado = altas(vec_cuentas, capacidad_nuevas_cuentas)
            limpiar_pantalla()
            # Actualizamos la posición de la nueva cuenta.
            if not dni_registrado:
                capacidad_nuevas_cuentas -= 1

        elif eleccion == 2:
            bajas(vec_cuentas)
            limpiar_pantalla()

        elif eleccion == 3:
            modificaciones(vec_cuentas)
            limpiar_pantalla()

        else:
            ejecutar = False
            print("Adios.")


def main():
    """Funcion principal"""
    vec_cuentas = np.array([Rcuentas] * 610)
    vec_cajeros = np.array([Rcuentas] * 120)
    vec_caj_may = np.array([0] * 120)
    carga(vec_cuentas, vec_cajeros)
    menu(vec_cuentas, vec_cajeros, vec_caj_may)


if __name__ == "__main__":
    main()
