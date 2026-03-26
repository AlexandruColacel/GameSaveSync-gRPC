#IMPORTANTE ES UNA GUI VIBECODEADA PARA PRUEBAS
import threading
import tkinter.filedialog as fd
import customtkinter as ctk
import pathlib as path
import shutil
import os
import grpc
import savesync_pb2_grpc
import savesync_pb2

# Reutilizamos la configuracion y helpers del cliente CLI
CHUNK_SIZE = 32 * 1024
CANAL = grpc.insecure_channel("localhost:5000")
stub = savesync_pb2_grpc.TrabajarGuardadoStub(CANAL)


def coger_save(ruta_archivo: path.Path, chunk_size: int):
    """Genera trozos del archivo o carpeta (zip) para subirlos via gRPC."""
    if ruta_archivo.exists() and ruta_archivo.is_file():
        with open(ruta_archivo, "rb") as archivo:
            while True:
                dato_enviar = archivo.read(chunk_size)
                if len(dato_enviar) == 0:
                    break
                yield savesync_pb2.saves(id=1, filename=ruta_archivo.name, save=dato_enviar)
    else:
        ruta_zip_temporal = shutil.make_archive(ruta_archivo, "zip", ruta_archivo)
        with open(ruta_zip_temporal, "rb") as archivo:
            while True:
                dato_enviar = archivo.read(chunk_size)
                if len(dato_enviar) == 0:
                    break
                yield savesync_pb2.saves(
                    id=1,
                    filename=path.Path(ruta_zip_temporal).name,
                    save=dato_enviar,
                )
        os.remove(ruta_zip_temporal)


class SaveSyncGUI(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("GameSaveSync GUI")
        self.geometry("720x420")
        self.minsize(640, 360)

        self.grid_columnconfigure(0, weight=1, uniform="col")
        self.grid_columnconfigure(1, weight=1, uniform="col")
        self.grid_rowconfigure(2, weight=1)

        # Subida
        self.upload_button = ctk.CTkButton(
            self,
            text="Subir Carpeta/Archivo",
            command=self.handle_upload_click,
            height=48,
        )
        self.upload_button.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        # Bajada
        self.download_entry = ctk.CTkEntry(
            self,
            placeholder_text="nombre_del_archivo.ext",
        )
        self.download_entry.grid(row=0, column=1, padx=20, pady=(20, 5), sticky="ew")

        self.download_button = ctk.CTkButton(
            self,
            text="Bajar Partida",
            command=self.handle_download_click,
            height=40,
        )
        self.download_button.grid(row=1, column=1, padx=20, pady=(0, 10), sticky="ew")

        # Consola embebida
        self.console = ctk.CTkTextbox(self, wrap="word")
        self.console.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.console.configure(state="disabled")

    # ---------- Helpers UI ----------
    def append_log(self, mensaje: str) -> None:
        def _append():
            self.console.configure(state="normal")
            self.console.insert("end", f"{mensaje}\n")
            self.console.see("end")
            self.console.configure(state="disabled")
        self.console.after(0, _append)

    def set_busy(self, busy: bool) -> None:
        estado = "disabled" if busy else "normal"
        self.upload_button.configure(state=estado)
        self.download_button.configure(state=estado)

    # ---------- Acciones ----------
    def handle_upload_click(self) -> None:
        selected = fd.askopenfilename(title="Selecciona archivo a subir", initialdir=str(path.Path.home()))
        ruta = path.Path(selected) if selected else None
        if ruta is None or not ruta.exists():
            carpeta = fd.askdirectory(title="Selecciona carpeta a subir", initialdir=str(path.Path.home()))
            ruta = path.Path(carpeta) if carpeta else None

        if ruta is None or not ruta.exists():
            self.append_log("No se selecciono archivo ni carpeta para subir.")
            return

        self.set_busy(True)
        threading.Thread(target=self.upload_path, args=(ruta,), daemon=True).start()

    def upload_path(self, ruta: path.Path) -> None:
        try:
            self.append_log(f"Subiendo: {ruta.name}")
            iterador = coger_save(ruta, CHUNK_SIZE)
            respuesta = stub.UploadSave(iterador)
            self.append_log(f"Servidor: {respuesta.message} (Confirmacion: {respuesta.confirmacion})")
        except grpc.RpcError as e:
            self.append_log(f"Error gRPC al subir: {e.details()}")
        except Exception as exc:
            self.append_log(f"Error inesperado al subir: {exc}")
        finally:
            self.set_busy(False)

    def handle_download_click(self) -> None:
        nombre = self.download_entry.get().strip()
        if not nombre:
            self.append_log("Introduce un nombre de archivo para bajar.")
            return

        self.set_busy(True)
        threading.Thread(target=self.download_save, args=(nombre,), daemon=True).start()

    def download_save(self, nombre_archivo: str) -> None:
        ruta_descargas = path.Path(r"C:\Users\Lex\TestServer\downloads")
        ruta_descargas.mkdir(parents=True, exist_ok=True)
        ruta_guardado = ruta_descargas / nombre_archivo

        self.append_log(f"Solicitando descarga de: {nombre_archivo}")
        try:
            peticion = savesync_pb2.PeticionBajarGuardado(filename=nombre_archivo)
            flujo_bajada = stub.DownloadSave(peticion)
            with open(ruta_guardado, "wb") as archivo_nuevo:
                for trozo in flujo_bajada:
                    archivo_nuevo.write(trozo.save)

            if ruta_guardado.suffix == ".zip":
                carpeta_destino = ruta_descargas / ruta_guardado.stem
                shutil.unpack_archive(ruta_guardado, carpeta_destino)
                os.remove(ruta_guardado)
                self.append_log(f"Descarga descomprimida en: {carpeta_destino}")
            else:
                self.append_log(f"Descarga guardada en: {ruta_guardado}")
        except grpc.RpcError as e:
            self.append_log(f"Error gRPC al bajar: {e.details()}")
        except Exception as exc:
            self.append_log(f"Error inesperado al bajar: {exc}")
        finally:
            self.set_busy(False)


def main() -> None:
    app = SaveSyncGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
