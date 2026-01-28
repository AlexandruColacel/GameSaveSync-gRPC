using Grpc.Core;
using GameSaveSync.Server; // Namespace generado por el proto

namespace GameSaveSync.Server.Services
{
    // Heredamos de la clase Base generada automáticamente por el .proto
    public class SaveSyncService : TrabajarGuardado.TrabajarGuardadoBase
    {
        private readonly ILogger<SaveSyncService> _logger;

        public SaveSyncService(ILogger<SaveSyncService> logger)
        {
            _logger = logger;
        }

        // Implementación del método SUBIR (Client Streaming)
        public override async Task<EstadoSubida> UploadSave(IAsyncStreamReader<saves> requestStream, ServerCallContext context)
        {
            // Aquí irá la lógica de leer el archivo, por ahora solo leemos el stream
            while (await requestStream.MoveNext())
            {
                var currentChunk = requestStream.Current;
                _logger.LogInformation($"Recibido chunk de: {currentChunk.Filename}");
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