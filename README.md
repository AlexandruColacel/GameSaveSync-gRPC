# GameSaveSync-gRPC
Personal project for synchronizing game saves across devices. Created to reinforce knowledge of Distributed Systems using .NET 9 and gRPC.
## 🧠 Architecture Decisions

### Why gRPC?
Unlike REST, which is text-based (JSON) and stateless, gRPC uses **Protocol Buffers** (binary).
- **Efficiency:** Binary serialization is smaller and faster for transmitting game save files.
- **Streaming:** Essential for uploading large save files (100MB+) without loading the entire file into server RAM.
- **Contract-First:** The `.proto` file acts as the single source of truth, preventing API drift between the C# Server and Python Client.

### Project Structure: Monorepo
I chose a Monorepo structure to keep the `.proto` definitions in a shared location (`/protos`). This ensures that both the Server and Client generated code are always in sync with the latest contract version.
