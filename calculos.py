import json

flag = False
listaVariable = []

sumatoriaAnterior = 0
cantidadAnterior = 0

def leerDataSet(nombreArchivo, variable):
  with open(nombreArchivo) as file:
    datos = json.load(file)
    return datos[variable]

def calcularPromedioSimple(nombreArchivo, variable):
  global flag
  global listaVariable
  global sumatoriaAnterior
  global sumatoriaAnterior
  valAux = 0
  calculo = 0

  cargarDataSet = leerDataSet(nombreArchivo, variable)

  if flag:
    valAux = cargarDataSet[-1]
    listaVariable.append(valAux)
    calculo = (sumatoriaAnterior + listaVariable[-1])/(cantidadAnterior + 1)
  else:
    for accion in cargarDataSet:
      listaVariable.append(accion)

    sumatoriaActual = sum(listaVariable)
    sumatoriaAnterior = sumatoriaActual
    cantidadActual = len(listaVariable)
    cantidadAnterior = cantidadActual
    calculo = sumatoriaActual/cantidadActual
  return calculo

def calcularPromedioSimplePeriodos(nombreArchivo, variable, cantidadPeriodos):
  listaAux = []
  cargarDataSet = leerDataSet(nombreArchivo, variable)

  for accion in cargarDataSet[-cantidadPeriodos:]:
    listaAux.append(accion)

  calculo = sum(listaAux)/len(listaAux)
  return calculo

def tendencia(nombreArchivo, variable):
  cargarDataSet = leerDataSet(nombreArchivo, variable)
  if cargarDataSet[-1] >= cargarDataSet[-2]:
    return True
  else:
    return False

if __name__ == "__main__":
  print(calcularPromedioSimplePeriodos('BRENTCMDUSD_D1.json', 'volume', 13))