def cuadrados_medios_una_parada(semilla):
    cuadrado = semilla ** 2
    cuadrado_str = str(cuadrado).zfill(8)
    digitos_medios = int(cuadrado_str[2:6])
    pasajeros = digitos_medios % 41
    return pasajeros if pasajeros != 0 else 1234 % 41

print(cuadrados_medios_una_parada(1))