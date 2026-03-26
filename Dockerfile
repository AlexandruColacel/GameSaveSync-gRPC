FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /workspace

COPY protos/ ./protos/
COPY src/Server/ ./src/Server/
WORKDIR /workspace/src/Server
RUN dotnet restore
RUN dotnet publish -c Release -o /app/out

FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS runtime
WORKDIR /app
COPY --from=build /app/out ./
ENv ASPNETCORE_URLS=http://+:5000
EXPOSE 5000
ENTRYPOINT [ "dotnet","GameSaveSync.Server.dll" ]