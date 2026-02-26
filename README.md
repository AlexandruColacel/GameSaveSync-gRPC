# GameSaveSync-gRPC 🎮🔄

> **[Español]** Sistema distribuido para la sincronización de archivos de guardado (SaveGames) mediante gRPC.
>
> **[English]** Distributed system for synchronizing game save files using gRPC.

---

## 🇪🇸 Descripción del Proyecto

**GameSaveSync** es una solución de ingeniería diseñada para resolver el problema de la sincronización de estados de juego entre diferentes dispositivos con latencia mínima.

A diferencia de las arquitecturas REST tradicionales, este proyecto implementa **gRPC** sobre **HTTP/2**, aprovechando la serialización binaria (Protocol Buffers) para maximizar el rendimiento y minimizar el uso de ancho de banda. El sistema está diseñado para manejar archivos binarios grandes de manera eficiente mediante el uso de **Streaming**, evitando la sobrecarga de memoria en el servidor.

### 🏗️ Arquitectura y Stack Tecnológico

* **Core:** .NET 9 (C#) para un Backend de alto rendimiento.
* **Cliente:** Python (Scripting eficiente y multiplataforma).
* **Protocolo:** gRPC (Google Remote Procedure Calls) & Protocol Buffers.
* **Patrón:** Monorepo (Single Source of Truth para contratos `.proto`).

### 🚀 Estado del Desarrollo (Roadmap)

El proyecto sigue un desarrollo iterativo incremental. A continuación se detalla el progreso actual:

#### Fase 1: Infraestructura y Definición de Contratos
- [x] **Definición de Interfaz (IDL):** Creación del contrato `savesync.proto` para definir servicios y mensajes.
- [x] **Configuración del Servidor:** Implementación de Kestrel en .NET 9 escuchando en HTTP/2 (Puerto 5000).
- [x] **Generación de Código (Stubs):** Compilación de protobufs para C# y Python.

#### Fase 2: Implementación de Lógica (Core)
- [x] **Cliente (Upload - Streaming):** Implementación de generadores en Python para fragmentación (chunking) y subida de archivos binarios.
- [X] **Servidor (Persistencia):** Recepción de streams y escritura asíncrona en disco local.
- [ ] **Cliente (Download):** Lógica para solicitar y reconstruir archivos desde el servidor.

#### Fase 3: Futuras Mejoras y Expansión (Backlog)
- [ ] **Frontal de Usuario (GUI):** Interfaz gráfica "Drag & Drop" para facilitar la gestión de archivos sin terminal.
- [ ] **Cliente Nativo (Rust):** Implementación de un cliente en Rust para máxima eficiencia y seguridad de memoria.
- [ ] **Despliegue Cloud:** Contenedorización (Docker) y despliegue en Azure Container Apps.

---

## 🇺🇸 Project Description

**GameSaveSync** is an engineering solution designed to solve game state synchronization challenges across devices with minimal latency.

Unlike traditional REST architectures, this project leverages **gRPC** over **HTTP/2**, utilizing binary serialization (Protocol Buffers) to maximize throughput and minimize bandwidth usage. The system is architected to handle large binary files efficiently through **Streaming**, preventing memory overload on the server side.

### 🏗️ Architecture & Tech Stack

* **Core:** .NET 9 (C#) for a high-performance Backend.
* **Client:** Python (Cross-platform efficient scripting).
* **Protocol:** gRPC (Google Remote Procedure Calls) & Protocol Buffers.
* **Pattern:** Monorepo (Single Source of Truth for `.proto` contracts).

### 🚀 Development Status (Roadmap)

The project follows an iterative incremental development lifecycle. Current progress is detailed below:

#### Phase 1: Infrastructure & Contract Definition
- [x] **Interface Definition (IDL):** `savesync.proto` contract defined for services and messages.
- [x] **Server Configuration:** .NET 9 Kestrel implementation listening on HTTP/2 (Port 5000).
- [x] **Code Generation (Stubs):** Protobuf compilation for C# and Python.

#### Phase 2: Core Logic Implementation
- [x] **Client (Upload - Streaming):** Python generator implementation for file chunking and binary streaming.
- [ ] **Server (Persistence):** Stream reception and asynchronous disk writing logic.
- [ ] **Client (Download):** Logic to request and reconstruct files from the server.

#### Phase 3: Future Scope & Backlog
- [ ] **User Frontend (GUI):** "Drag & Drop" graphical interface for seamless file management.
- [ ] **Native Client (Rust):** Implementation of a Rust client for memory safety and peak performance.
- [ ] **Cloud Deployment:** Docker containerization and deployment to Azure Container Apps.
