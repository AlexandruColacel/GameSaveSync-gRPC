import sys #libreria para pillar por terminal los parametros en este caso pillare el path de donde este al archivo de guardado
import pathlib as path #libreria para comprobar que la ruta existe realmente
import grpc
import savesync_pb2_grpc
import savesync_pb2
import shutil
import os

# Definimos el límite de seguridad (Límite - 64KB para metadatos de gRPC)
# 4,194,304 - 65,536 = 4,128,768 bytes
#aunque finalmente uso 32KB para una conexion mas rapida que si no me tiro 5 años subiendo archivos
CHUNK_SIZE = 32 * 1024

#definir el canal
canal = grpc.insecure_channel('localhost:5000') #para pruebas en local lo voy a dejar como insecure chanael.
stub = savesync_pb2_grpc.TrabajarGuardadoStub(canal) # es my stub del lado del cliente


def coger_save(ruta_archivo, CHUNK_SIZE):
    if ruta_archivo.exists() and ruta_archivo.is_file():
        with open(ruta_archivo,'rb') as archivo: #el rb es de read bynary ya que asumo que la mayoria de saves son binarios
            while True: #voy mientras datos enviar no este vacio voy leyendo leo mi CHUNCK_SIZE que es el minimo que permite gRPC
                dato_enviar = archivo.read(CHUNK_SIZE)
                if len(dato_enviar) == 0:
                    break
                
                yield savesync_pb2.saves(id = 1,filename = ruta_archivo.name,save = dato_enviar) #Aqui el texto deberia de sacarlo 
               
                ##print(dato_enviar)

    else:
        #print("narys") 
        #si estoy aqui es que es una carpeta y haz que zippearla
        ruta_zip_temporal = shutil.make_archive(ruta_archivo,'zip',ruta_archivo) #el shutil me hace el zip y me devuelve la ruta donde lo a creado aunque de momento uso la misma que la del archivo 
        with open(ruta_zip_temporal,'rb') as archivo: #el rb es de read bynary ya que asumo que la mayoria de saves son binarios
            while True: #voy mientras datos enviar no este vacio voy leyendo leo mi CHUNCK_SIZE que es el minimo que permite gRPC
                dato_enviar = archivo.read(CHUNK_SIZE)
                if len(dato_enviar) == 0:
                    break
                
                yield savesync_pb2.saves(id = 1,filename = path.Path(ruta_zip_temporal).name,save = dato_enviar) #Aqui el texto deberia de sacarlo 
               
                ##print(dato_enviar)
        
        #despues borro el archivo ya que el usuario no quiere guarreria
        os.remove(ruta_zip_temporal); 

# --- INICIO DE LA LÓGICA DEL MENÚ ---
# Comprobamos que me pasen bien los argumentos por consola
if len(sys.argv) < 3:
    print("Uso incorrecto bro. Hazlo así:")
    print("  Para subir: py client.py subir \"C:\\Ruta\\Al\\archivo.dat\"")
    print("  Para bajar: py client.py bajar \"nombre_del_archivo.dat\"")
    sys.exit()

accion = sys.argv[1].lower() # pillo si quiero subir o bajar
parametro = sys.argv[2]      # pillo la ruta o el nombre dependiendo de la accion

if accion == "subir":
    # guardo el path que recibo por argumetos en rutaarchivo
    # importante la ruta siempre entrecomillada
    ruta_archivo = path.Path(parametro).resolve() 
    
    iterador = coger_save(ruta_archivo, CHUNK_SIZE)

    print(f"--- Subiendo {ruta_archivo.name} ---")
    respuesta = stub.UploadSave(iterador)
    print(f"Servidor dice: {respuesta.message} (Confirmación: {respuesta.confirmacion})")

elif accion == "bajar":
    ruta_descargas = path.Path(r"C:\Users\Lex\TestServer\downloads")  # la r es de raw string para que no molesten las \ 
   

    
    # IMPORTANTE: Creo la carpeta de descargas por si no existe en mi PC, así no da error
    ruta_descargas.mkdir(parents=True, exist_ok=True)
    
    nombre_descarga = parametro # pillo el nombre del archivo directamente del parametro que me han pasado
    ruta_guardado = ruta_descargas / nombre_descarga # junto la carpeta con el nombre para saber donde guardarlo

    print(f"\n--- Solicitando descarga de {nombre_descarga} ---")

    try:
        # preparo la peticion con el nombre del archivo que quiero pedirle al server
        peticion = savesync_pb2.PeticionBajarGuardado(filename=nombre_descarga)
        
        # llamo al servidor y me guardo el iterador de red que me devuelve
        flujo_bajada = stub.DownloadSave(peticion)
        
        # abro mi archivo local en modo escritura binaria para ir metiendo los datos
        with open(ruta_guardado, 'wb') as archivo_nuevo:
            # por cada trozo que el servidor me escupe, lo escribo en mi disco duro
            for trozo in flujo_bajada:
                archivo_nuevo.write(trozo.save) 
                
        print(f"¡Descarga completada con éxito en {ruta_guardado}!")
        if(ruta_guardado.suffix == '.zip'):
            nombre_carpeta = ruta_guardado.stem 
            carpeta_destino = ruta_descargas / nombre_carpeta
            shutil.unpack_archive(ruta_guardado, carpeta_destino)
            os.remove(ruta_guardado)

    except grpc.RpcError as e:
        # si el servidor me tira un error (ej: el archivo no existe), lo cazo por aquí
        print(f"Error gRPC: {e.details()}")

else:
    print(f"No reconozco la acción '{accion}'. Usa 'subir' o 'bajar'.")