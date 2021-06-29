import subprocess
import threading
import socket
import sys
import os

FIN_COMANDO = b'#00#'


def leer_respuesta(socket):
    """
    Lee el canal de comunicación del servidor y reconstruye
    la salida asociada
    """
    salida = socket.recv(2048)
    while not salida.endswith(FIN_COMANDO):
        salida += socket.recv(2048)
    a_quitar_caracteres = len(FIN_COMANDO)
    return salida[:-a_quitar_caracteres]


def mandar_comando(comando, socket):
    """
    Envía el comando a través del socket, haciendo conversiones necesarias
    Espera la respuesta del servidor y la regresa
    comando viene como str
    """
    comando = comando.encode('utf-8') # convertir a binario
    comando += FIN_COMANDO
    socket.send(comando)
    salida = leer_respuesta(socket)
    return salida

def desplegar_salida_comando(salida):
    """
    Despliega la salida regresada por el servidor
    salida es una cadena binaria
    """
    salida = salida.decode('utf-8')
    print(salida)


def leer_comandos(socket):
    """
    Función con la interfaz de usuario
    """
    comando = ''
    while comando != 'exit': 
        comando = input('$> ') # lee un str no binario
        respuesta = mandar_comando(comando, socket)
        desplegar_salida_comando(respuesta)
    socket.close()



def inicializar_servidor(puerto):
    """
    Crea el servidor bind y se queda esperando
    """
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('', int(puerto)))  # hace el bind en cualquier interfaz disponible
    servidor.listen(5) # peticiones de conexion simultaneas
    print('Escuchando peticiones en el puerto %s' % puerto)
    


    cliente, addr = servidor.accept()
    print('Iniciando atención a cliente')
    print(addr)
    leer_comandos(cliente)
    cliente.close()
        

        
if __name__ == '__main__':
    puerto = sys.argv[1]
    inicializar_servidor(puerto)