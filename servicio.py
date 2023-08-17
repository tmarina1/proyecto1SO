from multiprocessing import Process
from multiprocessing.connection import Listener
from calculos import CalculadoraFinanciera
from colorama import init, Fore, Back, Style

def handle_client(client_conn, client_id, calc_handler, archivo_dataset):
    while True:
        try:
            data = client_conn.recv()
            if data is None:
                break 
            print(f"Cliente {client_id}: {data}")
            tendencia = calc_handler.tendencia(archivo_dataset, 'close')
            valAccion = calc_handler.ultimoValor(archivo_dataset, 'close')
            precioAlto = calc_handler.ultimoValor(archivo_dataset, 'high')
            precioBajo = calc_handler.ultimoValor(archivo_dataset, 'low')
            proGeneral = calc_handler.calcularPromedioSimple(archivo_dataset, 'close')
            promUltimosCinco = calc_handler.calcularPromedioSimplePeriodos(archivo_dataset, 'close', 5)
            proUltimosTrece = calc_handler.calcularPromedioSimplePeriodos(archivo_dataset, 'close', 13)

            if tendencia:
                print(Fore.GREEN + "Tendencia: Subir")
            else:
                print(Fore.RED + "Tendencia: Bajar")
            print(calc_handler.tabla(valAccion, precioAlto, precioBajo, proGeneral, promUltimosCinco, proUltimosTrece))
        except EOFError:
            #print(f"Cliente {client_id} salió.")
            break

    client_conn.close()

# Crea los procesos que se necesiten
def main(archivo_dataset):
    server_address = ('localhost', 6000)
    server = Listener(server_address)
    calc = CalculadoraFinanciera()

    tendencia = calc.tendencia(archivo_dataset, 'close')
    valAccion = calc.ultimoValor(archivo_dataset, 'close')
    precioAlto = calc.ultimoValor(archivo_dataset, 'high')
    precioBajo = calc.ultimoValor(archivo_dataset, 'low')
    proGeneral = calc.calcularPromedioSimple(archivo_dataset, 'close')
    promUltimosCinco = calc.calcularPromedioSimplePeriodos(archivo_dataset, 'close', 5)
    proUltimosTrece = calc.calcularPromedioSimplePeriodos(archivo_dataset, 'close', 13)

    if tendencia:
        print(Fore.GREEN + "Tendencia: Subir")
    else:
        print(Fore.RED + "Tendencia: Bajar")
    print(calc.tabla(valAccion, precioAlto, precioBajo, proGeneral, promUltimosCinco, proUltimosTrece))

    client_id = 0

    grafic_process = Process(target=calc.grafica)
    grafic_process.start()

    while True:
        client_conn = server.accept()
        #print("Conexion de:", server.last_accepted)

        client_process = Process(target=handle_client, args=(client_conn, client_id, calc, archivo_dataset))
        client_process.start()
        client_id += 1

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-ar", "--archivo", help = "Archivo dataset a utilizar (default=BRENTCMDUSD_D1.json)")
    args = parser.parse_args()
    
    if args.archivo:
        main(args.archivo)
    else:
        main('BRENTCMDUSD_D1.json')