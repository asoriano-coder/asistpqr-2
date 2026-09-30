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
# COPIA OPCIONAL
#
# EMAIL_CC es independiente de GMAIL_USER.
# Si EMAIL_CC no existe o está vacío, el correo se enviará
# únicamente al destinatario principal.
# ------------------------------------------------------------

EMAIL_CC = os.getenv(
    "EMAIL_CC"
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
# ENVIAR NOTIFICACIÓN DE REPORTES
#
# ID 3.11 = OBLIGATORIO
# ID 3.1  = OPCIONAL / MODO CONTINGENCIA
# ============================================================


def enviar_notificacion_reportes(
    reporte_id311,
    reporte_id31=None
):

    validar_configuracion_email()

    # --------------------------------------------------------
    # CONFIGURAR RESEND
    # --------------------------------------------------------

    resend.api_key = RESEND_API_KEY

    # --------------------------------------------------------
    # REPORTE ID 3.11 - OBLIGATORIO
    # --------------------------------------------------------

    if not reporte_id311:

        raise ValueError(
            "No se recibió información "
            "del reporte ID 3.11."
        )

    archivo_id311 = Path(
        reporte_id311[
            "archivo_local"
        ]
    )

    enlace_id311 = reporte_id311[
        "enlace_drive"
    ]

    nombre_id311 = archivo_id311.name

    if not enlace_id311:

        raise ValueError(
            "No se recibió el enlace "
            "de Google Drive del reporte ID 3.11."
        )

    # --------------------------------------------------------
    # REPORTE ID 3.1 - OPCIONAL
    # --------------------------------------------------------

    archivo_id31 = None
    enlace_id31 = None
    nombre_id31 = None

    id31_disponible = False

    if reporte_id31:

        archivo_local_id31 = reporte_id31.get(
            "archivo_local"
        )

        enlace_id31 = reporte_id31.get(
            "enlace_drive"
        )

        if (
            archivo_local_id31
            and enlace_id31
        ):

            archivo_id31 = Path(
                archivo_local_id31
            )

            nombre_id31 = archivo_id31.name

            id31_disponible = True

    # --------------------------------------------------------
    # ESTADO DE LA NOTIFICACIÓN
    # --------------------------------------------------------

    print("")
    print("==========================================")

    if id31_disponible:

        print(
            "✅ NOTIFICACIÓN CON ID 3.11 + ID 3.1"
        )

    else:

        print(
            "⚠️ NOTIFICACIÓN EN MODO CONTINGENCIA"
        )

        print(
            "✅ ID 3.11 disponible."
        )

        print(
            "⚠️ ID 3.1 no disponible."
        )

        print(
            "➡️ Se enviará correo únicamente "
            "con ID 3.11."
        )

    print("==========================================")

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

    if id31_disponible:

        asunto = (
            "AsistPQR - Reportes actualizados - "
            f"{fecha_hora}"
        )

    else:

        asunto = (
            "AsistPQR - Reporte 3.11 actualizado - "
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

    if EMAIL_CC:
        print(EMAIL_CC)
    else:
        print("Sin copia")

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
        "la actualización del reporte "
        "ID 3.11 de AuraQuantic.\n\n"

        f"Fecha y hora de actualización:\n"
        f"{fecha_hora}\n\n"

        "REPORTE ID 3.11\n"
        "Seguimiento de novedades PQR\n"
        f"{nombre_id311}\n\n"
        f"{enlace_id311}\n\n"
    )

    if id31_disponible:

        cuerpo_texto += (
            "REPORTE ID 3.1\n"
            "Reporte de novedades\n"
            f"{nombre_id31}\n\n"
            f"{enlace_id31}\n\n"
        )

    else:

        cuerpo_texto += (
            "NOTA DE CONTINGENCIA\n"
            "El reporte ID 3.1 no fue actualizado "
            "en esta ejecución.\n"
            "AsistPQR continuará operando "
            "temporalmente con el reporte ID 3.11.\n\n"
        )

    cuerpo_texto += (
        "Ubicación:\n"
        "Google Drive > BotPQR > "
        "Reportes Auraquantic\n\n"

        "Proceso completado automáticamente "
        "por AsistPQR v2."
    )

    # --------------------------------------------------------
    # BLOQUE HTML ID 3.1
    # --------------------------------------------------------

    if id31_disponible:

        bloque_html_id31 = f"""
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
        """

    else:

        bloque_html_id31 = """
            <hr>

            <h3>
                Estado del reporte ID 3.1
            </h3>

            <p>
                El reporte ID 3.1 no fue actualizado
                en esta ejecución.
            </p>

            <p>
                AsistPQR continuará operando
                temporalmente con el reporte ID 3.11.
            </p>
        """

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
                la actualización del reporte
                ID 3.11 de AuraQuantic.
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

            {bloque_html_id31}

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
            EMAIL_CC if EMAIL_CC else "Sin copia"
        )

        print(
            "Reply-To:",
            EMAIL_REPLY_TO
        )

        print(
            "Asunto:",
            asunto
        )

        if id31_disponible:

            print(
                "✅ Correo enviado con "
                "ID 3.11 + ID 3.1."
            )

        else:

            print(
                "✅ Correo enviado únicamente "
                "con ID 3.11."
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
        "los reportes disponibles a Google Drive."
    )