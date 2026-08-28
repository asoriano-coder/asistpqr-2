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

CARPETA_HISTORICOS = (
    f"{CARPETA_REPORTES}/históricos"
)


# ============================================================
# CONTROL DE EJECUCIÓN
#
# Permite archivar los archivos actuales una sola vez
# durante cada ejecución de RobotPQR.
# ============================================================

HISTORICO_PREPARADO = False


# ============================================================
# EJECUTAR COMANDO RCLONE
# ============================================================

def ejecutar_rclone(
    comando,
    descripcion_error
):

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
            descripcion_error
        )

    return resultado


# ============================================================
# ARCHIVAR REPORTES ANTERIORES
# ============================================================

def archivar_reportes_actuales():

    global HISTORICO_PREPARADO

    # --------------------------------------------------------
    # EVITAR ARCHIVAR MÁS DE UNA VEZ EN LA MISMA EJECUCIÓN
    # --------------------------------------------------------

    if HISTORICO_PREPARADO:

        return

    print("")
    print("========================================")
    print(" ARCHIVANDO REPORTES ANTERIORES")
    print("========================================")

    ruta_raiz = (
        f"{RCLONE_REMOTE}:"
        f"{CARPETA_REPORTES}"
    )

    ruta_historicos = (
        f"{RCLONE_REMOTE}:"
        f"{CARPETA_HISTORICOS}"
    )

    # --------------------------------------------------------
    # 1. CREAR CARPETA HISTÓRICOS SI NO EXISTE
    # --------------------------------------------------------

    print("")
    print(
        "Validando carpeta históricos..."
    )

    ejecutar_rclone(
        [
            "rclone",
            "mkdir",
            ruta_historicos,
        ],
        (
            "No fue posible crear o validar "
            "la carpeta históricos."
        )
    )

    # --------------------------------------------------------
    # 2. LISTAR ARCHIVOS EN LA RAÍZ
    # --------------------------------------------------------

    print("")
    print(
        "Buscando reportes actuales "
        "en Google Drive..."
    )

    resultado = ejecutar_rclone(
        [
            "rclone",
            "lsjson",
            ruta_raiz,
            "--files-only",
            "--max-depth",
            "1",
        ],
        (
            "No fue posible consultar "
            "los reportes actuales "
            "en Google Drive."
        )
    )

    try:

        archivos = json.loads(
            resultado.stdout
        )

    except json.JSONDecodeError as error:

        raise RuntimeError(
            "No fue posible interpretar "
            "la lista de archivos "
            "de Google Drive."
        ) from error

    # --------------------------------------------------------
    # 3. FILTRAR SOLO EXCEL Y JSON
    # --------------------------------------------------------

    archivos_reportes = []

    for archivo in archivos:

        nombre = archivo.get(
            "Name",
            ""
        )

        extension = Path(
            nombre
        ).suffix.lower()

        if extension in [
            ".xlsx",
            ".json",
        ]:

            archivos_reportes.append(
                nombre
            )

    # --------------------------------------------------------
    # 4. SI NO HAY ARCHIVOS, CONTINUAR
    # --------------------------------------------------------

    if not archivos_reportes:

        print("")
        print(
            "No existen reportes anteriores "
            "para archivar."
        )

        HISTORICO_PREPARADO = True

        return

    print("")
    print(
        f"Reportes encontrados: "
        f"{len(archivos_reportes)}"
    )

    # --------------------------------------------------------
    # 5. MOVER CADA ARCHIVO A HISTÓRICOS
    # --------------------------------------------------------

    for nombre_archivo in archivos_reportes:

        origen = (
            f"{RCLONE_REMOTE}:"
            f"{CARPETA_REPORTES}/"
            f"{nombre_archivo}"
        )

        destino = (
            f"{RCLONE_REMOTE}:"
            f"{CARPETA_HISTORICOS}/"
            f"{nombre_archivo}"
        )

        print("")
        print(
            "Archivando:"
        )

        print(
            nombre_archivo
        )

        ejecutar_rclone(
            [
                "rclone",
                "moveto",
                origen,
                destino,
            ],
            (
                "No fue posible mover "
                f"{nombre_archivo} "
                "a históricos."
            )
        )

        print(
            "✅ Archivado correctamente."
        )

    print("")
    print(
        "✅ REPORTES ANTERIORES ARCHIVADOS"
    )

    # --------------------------------------------------------
    # 6. MARCAR ARCHIVADO COMO COMPLETADO
    # --------------------------------------------------------

    HISTORICO_PREPARADO = True


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

    # --------------------------------------------------------
    # 2. ARCHIVAR REPORTES ANTERIORES
    #
    # Esta función realmente ejecutará el archivado
    # solamente en la primera carga de cada ejecución.
    # --------------------------------------------------------

    archivar_reportes_actuales()

    destino = (
        f"{RCLONE_REMOTE}:"
        f"{CARPETA_REPORTES}/"
    )

    print("Archivo local:")
    print(archivo_local)

    print("Destino:")
    print(destino)

    # --------------------------------------------------------
    # 3. SUBIR MEDIANTE RCLONE
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
    print(
        "✅ Archivo enviado a Google Drive."
    )

    # --------------------------------------------------------
    # 4. RUTA EXACTA DEL ARCHIVO REMOTO
    # --------------------------------------------------------

    archivo_remoto = (
        f"{RCLONE_REMOTE}:"
        f"{CARPETA_REPORTES}/"
        f"{archivo_local.name}"
    )

    # --------------------------------------------------------
    # 5. VALIDAR Y OBTENER METADATOS CON LSJSON
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
    print(
        "Archivo validado en Google Drive:"
    )

    print(
        nombre_remoto
    )

    # --------------------------------------------------------
    # 6. CONSTRUIR ENLACE DIRECTO GOOGLE DRIVE
    # --------------------------------------------------------

    enlace_drive = None

    if id_drive:

        enlace_drive = (
            "https://drive.google.com/file/d/"
            f"{id_drive}/view"
        )

        print("")
        print(
            "✅ Enlace Google Drive generado:"
        )

        print(
            enlace_drive
        )

    else:

        print("")
        print(
            "⚠️ rclone no devolvió ID "
            "de Google Drive."
        )

    print("")
    print(
        "✅ ARCHIVO VALIDADO EN GOOGLE DRIVE"
    )

    # --------------------------------------------------------
    # 7. DEVOLVER INFORMACIÓN AL ROBOT
    # --------------------------------------------------------

    return {
        "archivo_local": str(
            archivo_local
        ),
        "archivo_remoto": archivo_remoto,
        "nombre": nombre_remoto,
        "id_drive": id_drive,
        "enlace_drive": enlace_drive,
    }