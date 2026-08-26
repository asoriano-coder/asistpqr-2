import os

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import resend

from dotenv import load_dotenv


# ============================================================
# CONFIGURACIÓN
# ============================================================

load_dotenv()

RESEND_API_KEY = os.getenv(
    "RESEND_API_KEY"
)

EMAIL_DESTINO = os.getenv(
    "EMAIL_DESTINO"
)

EMAIL_REPLY_TO = os.getenv(
    "EMAIL_REPLY_TO"
)

EMAIL_FROM_NAME = os.getenv(
    "EMAIL_FROM_NAME",
    "Asistente PQR"
)

# ------------------------------------------------------------
# REMITENTE TEMPORAL DE RESEND
#
# Mientras no tengamos un dominio propio verificado
# utilizaremos onboarding@resend.dev.
# ------------------------------------------------------------

RESEND_FROM_EMAIL = os.getenv(
    "RESEND_FROM_EMAIL",
    "onboarding@resend.dev"
)

# ------------------------------------------------------------
# COPIA
#
# Seguimos utilizando asoriano@ansonet.biz como CC.
# Si existe GMAIL_USER en Railway reutilizamos esa variable.
# ------------------------------------------------------------

EMAIL_CC = os.getenv(
    "GMAIL_USER"
)


# ============================================================
# VALIDAR CONFIGURACIÓN
# ============================================================


def validar_configuracion_email():

    if not RESEND_API_KEY:

        raise ValueError(
            "Falta RESEND_API_KEY "
            "en las variables de entorno."
        )

    if not EMAIL_DESTINO:

        raise ValueError(
            "Falta EMAIL_DESTINO "
            "en las variables de entorno."
        )

    if not EMAIL_REPLY_TO:

        raise ValueError(
            "Falta EMAIL_REPLY_TO "
            "en las variables de entorno."
        )

    if not RESEND_FROM_EMAIL:

        raise ValueError(
            "Falta RESEND_FROM_EMAIL."
        )


# ============================================================
# ENVIAR NOTIFICACIÓN DE LOS DOS REPORTES
# ============================================================


def enviar_notificacion_reportes(
    reporte_id311,
    reporte_id31
):

    validar_configuracion_email()

    # --------------------------------------------------------
    # CONFIGURAR RESEND
    # --------------------------------------------------------

    resend.api_key = RESEND_API_KEY

    # --------------------------------------------------------
    # REPORTE ID 3.11
    # --------------------------------------------------------

    archivo_id311 = Path(
        reporte_id311[
            "archivo_local"
        ]
    )

    enlace_id311 = reporte_id311[
        "enlace_drive"
    ]

    nombre_id311 = archivo_id311.name

    # --------------------------------------------------------
    # REPORTE ID 3.1
    # --------------------------------------------------------

    archivo_id31 = Path(
        reporte_id31[
            "archivo_local"
        ]
    )

    enlace_id31 = reporte_id31[
        "enlace_drive"
    ]

    nombre_id31 = archivo_id31.name

    # --------------------------------------------------------
    # VALIDAR ENLACES
    # --------------------------------------------------------

    if not enlace_id311:

        raise ValueError(
            "No se recibió el enlace "
            "de Google Drive del reporte ID 3.11."
        )

    if not enlace_id31:

        raise ValueError(
            "No se recibió el enlace "
            "de Google Drive del reporte ID 3.1."
        )

    # --------------------------------------------------------
    # FECHA / HORA ECUADOR
    # --------------------------------------------------------

    momento_ecuador = datetime.now(
        ZoneInfo(
            "America/Guayaquil"
        )
    )

    fecha_hora = momento_ecuador.strftime(
        "%d/%m/%Y %H:%M"
    )

    # --------------------------------------------------------
    # ASUNTO
    # --------------------------------------------------------

    asunto = (
        "AsistPQR - Reportes actualizados - "
        f"{fecha_hora}"
    )

    print("")
    print(
        "=== ENVIANDO NOTIFICACIÓN CON RESEND ==="
    )

    print(
        "Remitente:"
    )

    print(
        f"{EMAIL_FROM_NAME} "
        f"<{RESEND_FROM_EMAIL}>"
    )

    print(
        "Destinatario:"
    )

    print(
        EMAIL_DESTINO
    )

    print(
        "Copia:"
    )

    print(
        EMAIL_CC
    )

    print(
        "Responder a:"
    )

    print(
        EMAIL_REPLY_TO
    )

    # --------------------------------------------------------
    # TEXTO PLANO
    # --------------------------------------------------------

    cuerpo_texto = (
        "AsistPQR completó correctamente "
        "la actualización de los reportes "
        "de AuraQuantic.\n\n"

        f"Fecha y hora de actualización:\n"
        f"{fecha_hora}\n\n"

        "REPORTE ID 3.11\n"
        "Seguimiento de novedades PQR\n"
        f"{nombre_id311}\n\n"
        f"{enlace_id311}\n\n"

        "REPORTE ID 3.1\n"
        "Reporte de novedades\n"
        f"{nombre_id31}\n\n"
        f"{enlace_id31}\n\n"

        "Ubicación:\n"
        "Google Drive > BotPQR > "
        "Reportes Auraquantic\n\n"

        "Proceso completado automáticamente "
        "por AsistPQR v2."
    )

    # --------------------------------------------------------
    # HTML
    # --------------------------------------------------------

    cuerpo_html = f"""
    <html>

        <body style="
            font-family: Arial, sans-serif;
            font-size: 14px;
            color: #333333;
        ">

            <h2>
                AsistPQR - Actualización completada
            </h2>

            <p>
                AsistPQR completó correctamente
                la actualización de los reportes
                de AuraQuantic.
            </p>

            <p>
                <strong>
                    Fecha y hora de actualización:
                </strong>
                <br>
                {fecha_hora}
            </p>

            <hr>

            <h3>
                ID 3.11 - Seguimiento de novedades PQR
            </h3>

            <p>
                <strong>Archivo:</strong>
                <br>
                {nombre_id311}
            </p>

            <p>
                <a
                    href="{enlace_id311}"
                    style="
                        display: inline-block;
                        padding: 12px 20px;
                        background-color: #1a73e8;
                        color: white;
                        text-decoration: none;
                        border-radius: 4px;
                        font-weight: bold;
                    "
                >
                    VER REPORTE ID 3.11
                </a>
            </p>

            <hr>

            <h3>
                ID 3.1 - Reporte de novedades
            </h3>

            <p>
                <strong>Archivo:</strong>
                <br>
                {nombre_id31}
            </p>

            <p>
                <a
                    href="{enlace_id31}"
                    style="
                        display: inline-block;
                        padding: 12px 20px;
                        background-color: #1a73e8;
                        color: white;
                        text-decoration: none;
                        border-radius: 4px;
                        font-weight: bold;
                    "
                >
                    VER REPORTE ID 3.1
                </a>
            </p>

            <hr>

            <p>
                <strong>Ubicación:</strong>
                <br>
                Google Drive &gt; BotPQR &gt;
                Reportes Auraquantic
            </p>

            <p style="
                margin-top: 30px;
                color: #666666;
                font-size: 12px;
            ">
                Proceso completado automáticamente
                por AsistPQR v2.
            </p>

        </body>

    </html>
    """

    # --------------------------------------------------------
    # PREPARAR PARÁMETROS RESEND
    # --------------------------------------------------------

    parametros = {

        "from": (
            f"{EMAIL_FROM_NAME} "
            f"<{RESEND_FROM_EMAIL}>"
        ),

        "to": [
            EMAIL_DESTINO
        ],

        "subject": asunto,

        "html": cuerpo_html,

        "text": cuerpo_texto,

        "reply_to": (
            EMAIL_REPLY_TO
        ),
    }

    # --------------------------------------------------------
    # CC SOLO SI EXISTE
    # --------------------------------------------------------

    if EMAIL_CC:

        parametros[
            "cc"
        ] = [
            EMAIL_CC
        ]

    # --------------------------------------------------------
    # ENVIAR
    # --------------------------------------------------------

    try:

        respuesta = resend.Emails.send(
            parametros
        )

        print("")
        print(
            "✅ CORREO ENVIADO CON RESEND"
        )

        print(
            "Respuesta:"
        )

        print(
            respuesta
        )

        print("")
        print(
            "Para:",
            EMAIL_DESTINO
        )

        print(
            "CC:",
            EMAIL_CC
        )

        print(
            "Reply-To:",
            EMAIL_REPLY_TO
        )

        print(
            "Asunto:",
            asunto
        )

        return True

    except Exception as error:

        print("")
        print(
            "❌ Error enviando correo "
            "mediante Resend:"
        )

        print(
            str(error)
        )

        raise RuntimeError(
            "No fue posible enviar "
            "la notificación mediante Resend."
        ) from error


# ============================================================
# PRUEBA INDEPENDIENTE
# ============================================================


if __name__ == "__main__":

    print("")
    print("==============================")
    print("   NOTIFICACIONES ASISTPQR")
    print("==============================")

    print("")
    print(
        "Este módulo debe ser invocado "
        "por robot_pqr.py después de subir "
        "los dos reportes a Google Drive."
    )