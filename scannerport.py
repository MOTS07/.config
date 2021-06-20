import socket
import sys
import time
import threading


def esta_abierto_puerto(host: str, puerto: int):
    """
    Determina si el puerto dado en el host dado está abierto o no
    """
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((host, puerto))
        return True
    except ConnectionRefusedError:
        return False
    except Exception as err:
        print(err)
        return False
    finally:
        cliente.close()


def almacenar_resultado_hilo(host, puerto, lista_puertos: list, mutex):
    """
    Wrapper de esta_abierto_puerto para hilos
    """
    if esta_abierto_puerto(host, puerto):
        mutex.acquire() # cierra el candado
        lista_puertos.append(puerto)
        mutex.release() # libera el candado
        
        
def regresar_puertos_abiertos_lineal(host: str, inicio_puerto=0, final_puerto=65536, trottling=0):
    """
    Regresa una lista de los puertos abiertos en el host
    """
    resultado = []
    for puerto in range(inicio_puerto, final_puerto):
        if esta_abierto_puerto(host, puerto):
            resultado.append(puerto)
        time.sleep(trottling)
    return resultado


def regresar_puertos_abiertos_hilos(host: str, inicio_puerto=0, final_puerto=65536):
    """
    Regresa una lista de los puertos abiertos en el host
    trabaja mediante hilos para mayor velocidad
    """
    # Falta considerar rangos de puertos mayores a mil (se terminan los descriptores de archivo)
    resultado = []
    pool_hilos = []
    mutex = threading.Lock() # evitar problemas de condiciones de carrera
    for puerto in range(inicio_puerto, final_puerto):
        hilo = threading.Thread(target=almacenar_resultado_hilo, args=(host, puerto, resultado, mutex))
        hilo.start()
        pool_hilos.append(hilo)
    for hilo in pool_hilos: # esperar a que todos los hilos terminen
        hilo.join()
    return resultado

        
if __name__ == '__main__':
    host = sys.argv[1]
    puertos_abiertos = regresar_puertos_abiertos_hilos(host)
    print(puertos_abiertos)