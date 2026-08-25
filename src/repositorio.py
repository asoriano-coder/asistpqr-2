import json
import subprocess
from pathlib import Path


# ============================================================
# CONFIGURACIÓN GOOGLE DRIVE
# ============================================================

RCLONE_REMOTE = "gdrive_pqr"

CARPETA_REPORTES = (
    "BotPQR/Reportes Auraquantic"
)


# ============================================================
# SUBIR REPORTE A GOOGLE DRIVE
# ============================================================

def subir_reporte_a_gdrive(
    archivo_local
):

    archivo_local = Path(
        archivo_local
    )

    print("")
    print("=== SUBIENDO REPORTE A GOOGLE DRIVE ===")

    # --------------------------------------------------------
    # 1. VALIDAR ARCHIVO LOCAL
    # --------------------------------------------------------

    if not archivo_local.exists():

        raise FileNotFoundError(
            f"No existe el archivo: {archivo_local}"
        )

    if archivo_local.stat().st_size <= 0:

        raise RuntimeError(
            "El archivo local está vacío."
        )

    destino = (
        f"{RCLONE_REMOTE}:"
        f"{CARPETA_REPORTES}/"
    )

    print("Archivo local:")
    print(archivo_local)

    print("Destino:")
    print(destino)

    # --------------------------------------------------------
    # 2. SUBIR MEDIANTE RCLONE
    # --------------------------------------------------------

    comando = [
        "rclone",
        "copy",
        str(archivo_local),
        destino,
    ]

    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True
    )

    if resultado.returncode != 0:

        print("")
        print("❌ Error rclone:")
        print(resultado.stderr)

        raise RuntimeError(
            "No fue posible subir "
            "el reporte a Google Drive."
        )

    print("")
    print("✅ Archivo enviado a Google Drive.")

    # --------------------------------------------------------
    # 3. RUTA EXACTA DEL ARCHIVO REMOTO
    # --------------------------------------------------------

    archivo_remoto = (
        f"{RCLONE_REMOTE}:"
        f"{CARPETA_REPORTES}/"
        f"{archivo_local.name}"
    )

    # --------------------------------------------------------
    # 4. VALIDAR Y OBTENER METADATOS CON LSJSON
    # --------------------------------------------------------

    print("")
    print(
        "Obteniendo información del archivo "
        "en Google Drive..."
    )

    comando_json = [
        "rclone",
        "lsjson",
        archivo_remoto,
    ]

    resultado_json = subprocess.run(
        comando_json,
        capture_output=True,
        text=True
    )

    if resultado_json.returncode != 0:

        print(
            resultado_json.stderr
        )

        raise RuntimeError(
            "El archivo fue subido, pero no fue "
            "posible obtener sus metadatos "
            "desde Google Drive."
        )

    try:

        datos = json.loads(
            resultado_json.stdout
        )

    except json.JSONDecodeError as error:

        raise RuntimeError(
            "No fue posible interpretar "
            "la respuesta de rclone lsjson."
        ) from error

    if not datos:

        raise RuntimeError(
            "Google Drive no devolvió información "
            "del archivo recién cargado."
        )

    # Normalmente lsjson devuelve una lista
    info_archivo = datos[0]

    nombre_remoto = info_archivo.get(
        "Name"
    )

    id_drive = info_archivo.get(
        "ID"
    )

    print("")
    print("Archivo validado en Google Drive:")
    print(nombre_remoto)

    # --------------------------------------------------------
    # 5. CONSTRUIR ENLACE DIRECTO GOOGLE DRIVE
    # --------------------------------------------------------

    enlace_drive = None

    if id_drive:

        enlace_drive = (
            "https://drive.google.com/file/d/"
            f"{id_drive}/view"
        )

        print("")
        print("✅ Enlace Google Drive generado:")
        print(enlace_drive)

    else:

        print("")
        print(
            "⚠️ rclone no devolvió ID de Google Drive."
        )

    print("")
    print("✅ ARCHIVO VALIDADO EN GOOGLE DRIVE")

    # --------------------------------------------------------
    # 6. DEVOLVER INFORMACIÓN AL ROBOT
    # --------------------------------------------------------

    return {
        "archivo_remoto": archivo_remoto,
        "nombre": nombre_remoto,
        "id_drive": id_drive,
        "enlace_drive": enlace_drive,
    }