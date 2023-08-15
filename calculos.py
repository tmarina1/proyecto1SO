import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mplfinance as mpf

class CalculadoraFinanciera:
  def __init__(self):
      self.flag = False
      self.listaVariable = []
      self.sumatoriaAnterior = 0
      self.cantidadAnterior = 0

  def leerDataSet(self, nombreArchivo, variable):
      with open(nombreArchivo) as file:
          datos = json.load(file)
          return datos[variable]

  def calcularPromedioSimple(self, nombreArchivo, variable):
      valAux = 0
      calculo = 0

      cargarDataSet = self.leerDataSet(nombreArchivo, variable)

      if self.flag:
          valAux = cargarDataSet[-1]
          self.listaVariable.append(valAux)
          calculo = (self.sumatoriaAnterior + self.listaVariable[-1]) / (self.cantidadAnterior + 1)
      else:
          for accion in cargarDataSet:
              self.listaVariable.append(accion)

          sumatoriaActual = sum(self.listaVariable)
          self.sumatoriaAnterior = sumatoriaActual
          cantidadActual = len(self.listaVariable)
          self.cantidadAnterior = cantidadActual
          calculo = sumatoriaActual / cantidadActual
      return calculo

  def calcularPromedioSimplePeriodos(self, nombreArchivo, variable, cantidadPeriodos):
      cargarDataSet = self.leerDataSet(nombreArchivo, variable)
      listaAux = cargarDataSet[-cantidadPeriodos:]
      calculo = sum(listaAux) / len(listaAux)
      return calculo

  def grafica(self):
      fig = plt.figure()
      ax1 = fig.add_subplot()

      def graficar(i):
          with open('BRENTCMDUSD_D1.json', 'r') as archivo:
              datos = json.load(archivo)

          campos = {
              'time': datos['time'][-50:], 'Open': datos['open'][-50:], 'High': datos['high'][-50:],
              'Low': datos['low'][-50:], 'Close': datos['close'][-50:], 'Volume': datos['volume'][-50:]
          }
          data = pd.DataFrame(campos)
          data['time'] = pd.to_datetime(data['time'], unit='s')
          data.set_index('time', inplace=True)

          ax1.clear()
          mpf.plot(data, ax=ax1, type='candle', style='charles')

      ani = animation.FuncAnimation(fig, graficar, interval=1000)
      plt.show()

  def tendencia(self, nombreArchivo, variable):
      cargarDataSet = self.leerDataSet(nombreArchivo, variable)
      return cargarDataSet[-1] >= cargarDataSet[-2]

if __name__ == "__main__":
  print(calcularPromedioSimplePeriodos('BRENTCMDUSD_D1.json', 'volume', 13))
