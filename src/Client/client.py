import sys #libreria para pillar por terminal los parametros en este caso pillare el path de donde este al archivo de guardado
import pathlib as path #libreria para comprobar que la ruta existe realmente
import grpc
import savesync_pb2_grpc
import savesync_pb2
ruta_archivo= path.Path(sys.argv[1]).resolve() #guardo el path que recibo por argumetos en rutaarchivo
#importante la ruta siempre entrecomillada
# Definimos el límite de seguridad (Límite - 64KB para metadatos de gRPC)
# 4,194,304 - 65,536 = 4,128,768 bytes
#aunque finalmente uso 32KB para una conexion mas rapida que si no me tiro 5 años subiendo archivos
CHUNK_SIZE = 32 * 1024

#definir el canal
canal = grpc.insecure_channel('localhost:5000') #para pruebas en local lo voy a dejar como insecure chanael.
stub = savesync_pb2_grpc.TrabajarGuardadoStub(canal) # es my stub del lado del 


def coger_save(ruta_archivo,CHUNK_SIZE):
    if ruta_archivo.exists():
        with open(ruta_archivo,'rb') as archivo: #el rb es de read bynary ya que asumo que la mayoria de saves son binarios
            while True: #voy mientras datos enviar no este vacio voy leyendo leo mi CHUNCK_SIZE que es el minimo que permite gRPC
                dato_enviar = archivo.read(CHUNK_SIZE)
                if len(dato_enviar) == 0:
                    break
                
                yield savesync_pb2.saves(id = 1,filename = ruta_archivo.name,save = dato_enviar) #Aqui el texto deberia de sacarlo 
               
                ##print(dato_enviar)

    else:
        print("narys")

iterador = coger_save(ruta_archivo,CHUNK_SIZE)

print(f"--- Subiendo {ruta_archivo.name} ---")
respuesta = stub.SubirGuardado(iterador)
print(f"Servidor dice: {respuesta.message} (Confirmación: {respuesta.confirmacion})")
    