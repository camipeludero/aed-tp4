from clase import *
from funciones import *
import pickle
import os.path


def menu():
    print("Menu de opciones:")
    print("\t 1. Cargar envios")
    print("\t 2. Mostrar listado")
    print("\t 3. Buscar")
    print("\t 4. Mayores")
    print("\t 0. Salir")
    print()
    op = int(input("Ingrese opción: "))
    return op


def cargar_datos():
    global FD
    archivo = open(FD)
    linea = archivo.readline().strip()
    v = []

    while linea != "":

        linea_sp = linea.split(",")
        id_pago, id_dest, nom_dest, tasa, monto_nom, id_algcom, id_algimp = linea_sp[0], linea_sp[1], linea_sp[2], float(linea_sp[3]), int(linea_sp[4]), int(linea_sp[5]), int(linea_sp[6])

        envio = Envio(id_pago, id_dest, nom_dest, tasa, monto_nom, id_algcom, id_algimp)
        add_in_order(v, envio)

        linea = archivo.readline().strip()

    archivo.close()
    return v


def mostrar_id_pago(v):
    i = int(input("Ingrese un valor i: "))
    n = len(v)
    if i % 2 == 0:
        indice = i // 2
    else:
        indice = (i * 3) + 1

    if indice >= n or i >= n:
        indice = n - 1
        i = n - 1

    print(f"r1.1: {v[i].obtener_identificador_pago()}")
    print(f"r1.2: {v[indice].obtener_identificador_pago()}")


def generar_archivo(v):
    global FD_BIN
    n = len(v)
    v_prom = [0] * 5
    v_acum = [0] * 5
    v_cont = [0] * 5

    m = open(FD_BIN, "wb")
    for i in range(n):
        mon_orig = int(v[i].obtener_codigo_moneda_origen()) - 1
        v_cont[mon_orig] += 1
        v_acum[mon_orig] += calcular_comision(v[i].monto_nominal, v[i].algoritmo_comision)
    for i in range(5):
        if v_cont[i] > 0:
            v_prom[i] = v_acum[i] / v_cont[i]
        else:
            v_prom[i] = 0

    for i in range(n):
        ind = int(v[i].obtener_codigo_moneda_origen()) - 1
        if calcular_comision(v[i].monto_nominal, v[i].algoritmo_comision) > v_prom[ind]:
            pickle.dump(v[i], m)
    m.close()


def mostrar_archivo():
    global FD_BIN

    if not os.path.exists(FD_BIN):
       print("Archivo inexistente")
       return

    m = open(FD_BIN, "rb")
    tam = os.path.getsize(FD_BIN)
    while m.tell() < tam:
        envio = pickle.load(m)
        print(envio)
    m.close()


def mostrar_mayor_moneda_origen(v):
    v_mayor = [None] * 5
    for i in range(len(v)):
        moneda_orig = v[i].obtener_codigo_moneda_origen() - 1
        if v_mayor[moneda_orig] is None or calcular_comision(v[i].monto_nominal, v[i].algoritmo_comision) > calcular_comision(v_mayor[moneda_orig].monto_nominal, v_mayor[moneda_orig].algoritmo_comision):
            v_mayor[moneda_orig] = v[i]

    for e in v_mayor:
        print(e)


def buscar(v):
    monto_nominal = monto_nominal_actualizado = 0

    id = input('Ingrese ID: ')
    envio = find_by_id(id, v)
    if envio != -1:
        monto_nominal = envio.monto_nominal
        monto_nominal_actualizado = round(monto_nominal * 1.17, -2)
        envio.monto_nominal = monto_nominal_actualizado

    print(f"r3.1: {monto_nominal}")
    print(f"r3.2: {monto_nominal_actualizado}")


def mayor(v):
    cf = 5
    cc = 5
    cant = [cc * [None] for f in range(cf)]

    for r in v:
        f = r.obtener_codigo_moneda_origen() - 1
        c = r.obtener_codigo_moneda_destino() - 1

        if cant[f][c] is None:
            cant[f][c] = r
        else:
            monto_final = calcular_monto_final(r)
            monto_final_almacenado = calcular_monto_final(cant[f][c])
            if monto_final_almacenado < monto_final:
                cant[f][c] = r
    moneda = ("ARS", "USD", "EUR", "GBP", "JPY")
    for f in range(cf):
        for c in range(cc):
            if cant[f][c] is not None:
                print(f"Origen {moneda[f]} Destino {moneda[c]}: {cant[f][c].obtener_identificador_pago()}")


def main():
    global FD
    global FD_BIN
    FD = "envios.csv"
    FD_BIN = "envios_binario.dat"
    v = []
    op = -1

    while op != 0:
        op = menu()

        if op == 1:
            v = cargar_datos()
            mostrar_id_pago(v)

        elif op == 2:
            if v:
                generar_archivo(v)
                mostrar_archivo()
                mostrar_mayor_moneda_origen(v)
            else:
                print("No hay datos cargados.")

        elif op == 3:
            if v:
                buscar(v)
            else:
                print("No hay datos cargados.")

        elif op == 4:
            if v:
                mayor(v)
            else:
                print("No hay datos cargados.")

        elif op == 0:
            print("Programa finalizado.")

        else:
            print("Opción invalida.")


if __name__ == "__main__":
    main()
