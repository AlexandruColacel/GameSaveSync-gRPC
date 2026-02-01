using GameSaveSync.Server.Services;
using Microsoft.AspNetCore.Server.Kestrel.Core;

var builder = WebApplication.CreateBuilder(args);
builder.WebHost.ConfigureKestrel(options => 
{ 
    // Configurar el servidor para escuchar en HTTP/2 sin TLS en el puerto 5000 
    options.ListenLocalhost(5000, o => o.Protocols = HttpProtocols.Http2); 
}); 

builder.Services.AddGrpc();

var app = builder.Build();
//builder.Services.AddSingleton<SaveSyncService>();  usaria esta linea extraida de mis apuntes ya que en mi ejemplo de practica era deseable
//mantener el estado entre peticiones aqui no la usare y saltare directamente al map

app.MapGrpcService<SaveSyncService>();

app.MapGet("/", () => "Servidor GameSaveSync activo. Usa un cliente gRPC.");

app.Run();