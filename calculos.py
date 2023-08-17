import json
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mplfinance as mpf
from tabulate import tabulate
from colorama import init, Fore, Back, Style

class CalculadoraFinanciera:
    def __init__(self):
        self.flag = False
        self.listaVariable = []
        self.sumatoriaAnterior = 0
        self.cantidadAnterior = 0

    # Permite leer el archivo .json especificando el archivo que se desea leer y la variable que se desea tener
    def leerDataSet(self, nombreArchivo, variable):
        with open(nombreArchivo) as file:
            datos = json.load(file)
            return datos[variable]

    # Retorna el calculo del promedio simple de todos los datos del archivo
    def calcularPromedioSimple(self, nombreArchivo, variable):
        valAux = 0
        calculo = 0

        cargarDataSet = self.leerDataSet(nombreArchivo, variable)

        if self.flag:
            valAux = cargarDataSet[-1]
            self.listaVariable.append(valAux)
            calculo = (self.sumatoriaAnterior + self.listaVariable[-1]) / (self.cantidadAnterior + 1)
        else:
            self.flag = True
            for accion in cargarDataSet:
                self.listaVariable.append(accion)

            sumatoriaActual = sum(self.listaVariable)
            self.sumatoriaAnterior = sumatoriaActual
            cantidadActual = len(self.listaVariable)
            self.cantidadAnterior = cantidadActual
            calculo = sumatoriaActual / cantidadActual
        return calculo

    # Retorna el calculo del promedio simple de los ultimos n periodos que se le indiquen
    def calcularPromedioSimplePeriodos(self, nombreArchivo, variable, cantidadPeriodos):
        cargarDataSet = self.leerDataSet(nombreArchivo, variable)
        listaAux = cargarDataSet[-cantidadPeriodos:]
        calculo = sum(listaAux) / len(listaAux)
        return calculo

    # Grafica los ultimos 50 datos del dataset 
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

        ani = animation.FuncAnimation(fig, graficar, interval=1000, cache_frame_data = False)
        plt.show()
        tiempo_espera = random.uniform(1, 3) 
        time.sleep(tiempo_espera)

    # Retorna el ultimo valor de la variable ingresada
    def ultimoValor(self, nombreArchivo, variable):
        cargarDataSet = self.leerDataSet(nombreArchivo, variable)
        return cargarDataSet[-1]

    # Retorna si las acciones estan tendiendo a subir o a bajar
    def tendencia(self, nombreArchivo, variable):
        cargarDataSet = self.leerDataSet(nombreArchivo, variable)
        ultimoDato = self.ultimoValor(nombreArchivo, variable)
        contadorSube = 0
        contadorBaja = 0
        for i in range(-7,-1):
            if cargarDataSet[i] < ultimoDato:
                contadorSube += 1
            elif cargarDataSet[i] > ultimoDato:
                contadorBaja += 1
        
        return contadorSube >= contadorBaja
    
    # Retorna la tabla que se va a mostrar por la terminal
    def tabla(self, valAccion, precioAlto, precioBajo, proGeneral, promUltimosCinco, proUltimosTrece):
        tabla = [['Valor accion', valAccion],
                ['Precio más alto', precioAlto],
                ['Precio más bajo', precioBajo],
                ['Promedio general', proGeneral],
                ['Promedio ultimos 5', promUltimosCinco],
                ['Promedio ultimos 13', proUltimosTrece]]
        
        table = tabulate(tabla)
        return table