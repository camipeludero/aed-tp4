def calcular_comision_1(monto_nominal):
    return (monto_nominal * 9) // 100


def calcular_comision_2(monto_nominal):
    if monto_nominal < 50000:
        return 0
    elif 50000 <= monto_nominal < 80000:
        return (monto_nominal * 5) // 100
    else:
        return (monto_nominal * 7.8) // 100


def calcular_comision_3(monto_nominal):
    MONTO_FIJO = 100
    comision = 0
    if monto_nominal > 25000:
        comision = (monto_nominal * 6) // 100
    return MONTO_FIJO + comision


def calcular_comision_4(monto_nominal):
    if monto_nominal <= 100000:
        return 500
    else:
        return 1000


def calcular_comision_5(monto_nominal):
    comision = 0
    if monto_nominal >= 500000:
        comision = (monto_nominal * 7) // 100
    if comision > 50000:
        comision = 50000
    return comision


def calcular_comision_7(monto_nominal):
    comision = 0
    if monto_nominal <= 75000:
        comision = 3000
    else:
        comision = ((monto_nominal - 75000) * 5) // 100
    if comision > 10000:
        comision = 10000
    return comision


def calcular_comision(monto_nominal, n_algoritmo):
    if n_algoritmo == 1:
        return calcular_comision_1(monto_nominal)
    elif n_algoritmo == 2:
        return calcular_comision_2(monto_nominal)
    elif n_algoritmo == 3:
        return calcular_comision_3(monto_nominal)
    elif n_algoritmo == 4:
        return calcular_comision_4(monto_nominal)
    elif n_algoritmo == 5:
        return calcular_comision_5(monto_nominal)
    elif n_algoritmo == 7:
        return calcular_comision_7(monto_nominal)
    else:
        return monto_nominal


def calcular_monto_final_1(monto_base):
    impuesto = 0
    if monto_base > 300000:
        excedente = monto_base - 300000
        impuesto = (excedente * 25) // 100
    return monto_base - impuesto


def calcular_monto_final_2(monto_base):
    if monto_base < 50000:
        impuesto = 50
    else:
        impuesto = 100
    return monto_base - impuesto


def calcular_monto_final_3(monto_base):
    impuesto = (monto_base * 3) // 100
    return monto_base - impuesto


def calcular_monto_final(r):
    comision = calcular_comision(r.monto_nominal, r.algoritmo_comision)
    monto_base = r.monto_nominal - comision

    if r.algoritmo_impositivo == 1:
        return calcular_monto_final_1(monto_base)
    elif r.algoritmo_impositivo == 2:
        return calcular_monto_final_2(monto_base)
    elif r.algoritmo_impositivo == 3:
        return calcular_monto_final_3(monto_base)
    else:
        return monto_base


def calcular_monto_final_convertido(r):
    monto_final = calcular_monto_final(r)
    monto_final_convertido = int(monto_final * r.tasa)

    return monto_final_convertido


def calcular_porcentaje_descuento(r):
    monto_final = calcular_monto_final(r)
    descuento = r.monto_nominal - monto_final

    return descuento * 100 / r.monto_nominal


def add_in_order(v, r):
    n = len(v)
    pos = n
    izq, der = 0, n-1

    while izq <= der:
        c = (izq+der)//2
        if v[c].identificacion_destinatario == r.identificacion_destinatario:
            pos = c
            break
        elif v[c].identificacion_destinatario < r.identificacion_destinatario:
            der = c-1
        else:
            izq = c+1
    else:
        pos = izq
    v[pos:pos] = [r]


def find_by_id(id, v):
    n = len(v)
    izq = 0
    der = n-1

    while izq <= der:
        c = (izq+der)//2
        if v[c].identificacion_destinatario == id:
            return v[c]
        if id < v[c].identificacion_destinatario:
            izq = c+1
        else:
            der = c-1
    return -1