using Grpc.Core;
using GameSaveSync.Server;
using Google.Protobuf;


namespace GameSaveSync.Server.Services
{
    // Heredamos de la clase Base generada automáticamente por el .proto
    public class SaveSyncService : TrabajarGuardado.TrabajarGuardadoBase
    {
        private readonly ILogger<SaveSyncService> _logger;
        
        String UploadDirectory = "C:/Users/Lex/TestServer/Updates";
        public SaveSyncService(ILogger<SaveSyncService> logger)
        {
            _logger = logger;
        }

        // Implementación del método SUBIR (Client Streaming)
        public override async Task<EstadoSubida> UploadSave(IAsyncStreamReader<saves> requestStream, ServerCallContext context)
        {
            FileStream stream = null ;
            // Aquí irá la lógica de leer el archivo, por ahora solo leemos el stream
            while (await requestStream.MoveNext())
            {   

                var currentChunk = requestStream.Current;
                int id = currentChunk.Id; //pillo el id  del objeto
                string nombre_juego = currentChunk.Filename;
                ByteString guardado = currentChunk.Save;
                
                if (stream == null)
                {
                    string safeFileName = Path.GetFileName(currentChunk.Filename);
                    string finalPath = Path.Combine(UploadDirectory, safeFileName);
                    
                    // Creamos el archivo
                    stream = new FileStream(finalPath, FileMode.Create);
                }
                guardado.WriteTo(stream);
                _logger.LogInformation($"Recibido chunk de: {currentChunk.Filename}");

            }
            if(stream != null)
            {
                await stream.DisposeAsync();
            }
            // Respondemos una sola vez al final
            return new EstadoSubida
            {
                Confirmacion = true,
                Message = "Archivo recibido correctamente en el servidor."
            };
        }

        // Implementación del método BAJAR (Server Streaming)
        public override async Task DownloadSave(PeticionBajarGuardado request, IServerStreamWriter<EstadoBajada> responseStream, ServerCallContext context)
        {
            // Simulación: Enviamos un dato dummy
            _logger.LogInformation($"Cliente pide bajar juego ID: {request.Id}");

            // Aquí leeríamos del disco y enviaríamos chunks
            await responseStream.WriteAsync(new EstadoBajada 
            { 
                Save = Google.Protobuf.ByteString.CopyFromUtf8("DUMMY_DATA") 
            });
        }
    }
}