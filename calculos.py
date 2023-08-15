import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mplfinance as mpf

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

def grafica():
  fig = plt.figure()
  ax1 = fig.add_subplot()

  def graficar(i):
    with open('BRENTCMDUSD_D1.json', 'r') as archivo:
        datos = json.load(archivo)
    
    campos = {'time': datos['time'][-50:],'Open': datos['open'][-50:],'High': datos['high'][-50:],'Low': datos['low'][-50:],'Close': datos['close'][-50:],'Volume': datos['volume'][-50:]}
    data = pd.DataFrame(campos)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    data.set_index('time', inplace = True)
    
    ax1.clear()
    mpf.plot(data, ax = ax1, type = 'candle', style = 'charles')

  ani = animation.FuncAnimation(fig, graficar, interval = 1000)
  plt.show()

def tendencia(nombreArchivo, variable):
  cargarDataSet = leerDataSet(nombreArchivo, variable)
  if cargarDataSet[-1] >= cargarDataSet[-2]:
    return True
  else:
    return False

if __name__ == "__main__":
  print(calcularPromedioSimplePeriodos('BRENTCMDUSD_D1.json', 'volume', 13))
