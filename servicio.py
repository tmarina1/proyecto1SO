from multiprocessing import Process
from multiprocessing.connection import Listener
from calculos import CalculadoraFinanciera
from colorama import init, Fore, Back, Style

def handle_client(client_conn, client_id, calc_handler):
    while True:
        try:
            data = client_conn.recv()
            if data is None:
                break 
            print(f"Cliente {client_id}: {data}")
            #print('PROM_SIMP: ',calc_handler.calcularPromedioSimple('BRENTCMDUSD_D1.json', 'close'))
            tendencia = calc_handler.tendencia('BRENTCMDUSD_D1.json', 'close')
            valAccion = calc_handler.ultimoValor('BRENTCMDUSD_D1.json', 'close')
            precioAlto = calc_handler.ultimoValor('BRENTCMDUSD_D1.json', 'high')
            precioBajo = calc_handler.ultimoValor('BRENTCMDUSD_D1.json', 'low')
            proGeneral = calc_handler.calcularPromedioSimple('BRENTCMDUSD_D1.json', 'close')
            promUltimosCinco = calc_handler.calcularPromedioSimplePeriodos('BRENTCMDUSD_D1.json', 'close', 5)
            proUltimosTrece = calc_handler.calcularPromedioSimplePeriodos('BRENTCMDUSD_D1.json', 'close', 13)

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
def main():
    server_address = ('localhost', 6000)
    server = Listener(server_address)
    calc = CalculadoraFinanciera()

    tendencia = calc.tendencia('BRENTCMDUSD_D1.json', 'close')
    valAccion = calc.ultimoValor('BRENTCMDUSD_D1.json', 'close')
    precioAlto = calc.ultimoValor('BRENTCMDUSD_D1.json', 'high')
    precioBajo = calc.ultimoValor('BRENTCMDUSD_D1.json', 'low')
    proGeneral = calc.calcularPromedioSimple('BRENTCMDUSD_D1.json', 'close')
    promUltimosCinco = calc.calcularPromedioSimplePeriodos('BRENTCMDUSD_D1.json', 'close', 5)
    proUltimosTrece = calc.calcularPromedioSimplePeriodos('BRENTCMDUSD_D1.json', 'close', 13)

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

        client_process = Process(target=handle_client, args=(client_conn, client_id, calc))
        client_process.start()
        client_id += 1

if __name__ == "__main__":
    main()