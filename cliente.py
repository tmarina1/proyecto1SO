from multiprocessing.connection import Client
import json
import random

def main(archivo_dataset):
  with open(archivo_dataset, 'r') as archivo:
    data = json.load(archivo)

  nuevaFecha = data['time'][-1] + random.randrange(3, 15, 4)
  Time = nuevaFecha
  Open = float(input('Ingrese el valor de apertura: '))
  High = float(input('Ingrese el valor más alto: '))
  Low = float(input('Ingrese el valor más bajo: '))
  Close = float(input('Ingrese el valor de cierre: '))
  Volume = float(input('Ingrese el volumen: '))

  data['time'].append(Time)
  data['open'].append(Open)
  data['high'].append(High)
  data['low'].append(Low)
  data['close'].append(Close)
  data['volume'].append(Volume)

  with open(archivo_dataset, 'w') as archivo:
    json.dump(data, archivo, indent=4)

  address = ('localhost', 6000)
  conn = Client(address)
  conn.send('signal')
  conn.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-ar", "--archivo", help = "Archivo dataset a utilizar (default=BRENTCMDUSD_D1.json)")
    args = parser.parse_args()
    
    if args.archivo:
        main(args.archivo)
    else:
        main('BRENTCMDUSD_D1.json')