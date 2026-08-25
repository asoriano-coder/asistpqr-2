import os
import ssl
import smtplib

from datetime import datetime
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv


# ============================================================
# CONFIGURACIÓN
# ============================================================

load_dotenv()

GMAIL_USER = os.getenv(
    "GMAIL_USER"
)

GMAIL_APP_PASSWORD = os.getenv(
    "GMAIL_APP_PASSWORD"
)

EMAIL_DESTINO = os.getenv(
    "EMAIL_DESTINO"
)

EMAIL_FROM_NAME = os.getenv(
    "EMAIL_FROM_NAME",
    "Asistente PQR"
)

EMAIL_REPLY_TO = os.getenv(
    "EMAIL_REPLY_TO"
)

SMTP_SERVIDOR = "smtp.gmail.com"
SMTP_PUERTO = 465


# ============================================================
# VALIDAR CONFIGURACIÓN
# ============================================================


def validar_configuracion_email():

    if not GMAIL_USER:
        raise ValueError(
            "Falta GMAIL_USER en el archivo .env"
        )

    if not GMAIL_APP_PASSWORD:
        raise ValueError(
            "Falta GMAIL_APP_PASSWORD "
            "en el archivo .env"
        )

    if not EMAIL_DESTINO:
        raise ValueError(
            "Falta EMAIL_DESTINO "
            "en el archivo .env"
        )

    if not EMAIL_REPLY_TO:
        raise ValueError(
            "Falta EMAIL_REPLY_TO "
            "en el archivo .env"
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
    # INFORMACIÓN REPORTE ID 3.11
    # --------------------------------------------------------

    archivo_id311 = Path(
        reporte_id311["archivo_local"]
    )

    enlace_id311 = reporte_id311[
        "enlace_drive"
    ]

    nombre_id311 = archivo_id311.name

    # --------------------------------------------------------
    # INFORMACIÓN REPORTE ID 3.1
    # --------------------------------------------------------

    archivo_id31 = Path(
        reporte_id31["archivo_local"]
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
            "No se recibió el enlace de Google Drive "
            "del reporte ID 3.11."
        )

    if not enlace_id31:
        raise ValueError(
            "No se recibió el enlace de Google Drive "
            "del reporte ID 3.1."
        )

    # --------------------------------------------------------
    # FECHA Y HORA ECUADOR
    # --------------------------------------------------------

    momento_ecuador = datetime.now(
        ZoneInfo("America/Guayaquil")
    )

    fecha_hora = momento_ecuador.strftime(
        "%d/%m/%Y %H:%M"
    )

    print("")
    print(
        "=== ENVIANDO NOTIFICACIÓN POR CORREO ==="
    )

    print("Nombre remitente:")
    print(EMAIL_FROM_NAME)

    print("Cuenta SMTP:")
    print(GMAIL_USER)

    print("Destinatario:")
    print(EMAIL_DESTINO)

    print("Copia:")
    print(GMAIL_USER)

    print("Responder a:")
    print(EMAIL_REPLY_TO)

    print("")
    print("Reporte ID 3.11:")
    print(nombre_id311)

    print("")
    print("Reporte ID 3.1:")
    print(nombre_id31)

    # --------------------------------------------------------
    # ASUNTO
    # --------------------------------------------------------

    asunto = (
        "AsistPQR - Reportes actualizados - "
        f"{fecha_hora}"
    )

    # --------------------------------------------------------
    # CREAR MENSAJE
    # --------------------------------------------------------

    mensaje = EmailMessage()

    mensaje["From"] = formataddr(
        (
            EMAIL_FROM_NAME,
            GMAIL_USER
        )
    )

    mensaje["To"] = EMAIL_DESTINO

    mensaje["Cc"] = GMAIL_USER

    mensaje["Reply-To"] = EMAIL_REPLY_TO

    mensaje["Subject"] = asunto

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
        "Enlace:\n"
        f"{enlace_id311}\n\n"

        "REPORTE ID 3.1\n"
        "Reporte de novedades\n"
        f"{nombre_id31}\n\n"
        "Enlace:\n"
        f"{enlace_id31}\n\n"

        "Ubicación:\n"
        "Google Drive > BotPQR > "
        "Reportes Auraquantic\n\n"

        "Proceso completado automáticamente "
        "por AsistPQR v2."
    )

    mensaje.set_content(
        cuerpo_texto
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
                AsistPQR completó correctamente la
                actualización de los reportes de AuraQuantic.
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

    mensaje.add_alternative(
        cuerpo_html,
        subtype="html"
    )

    # --------------------------------------------------------
    # ENVÍO SMTP
    # --------------------------------------------------------

    contexto_ssl = ssl.create_default_context()

    try:

        with smtplib.SMTP_SSL(
            SMTP_SERVIDOR,
            SMTP_PUERTO,
            context=contexto_ssl
        ) as servidor:

            print("")
            print(
                "Conectando con Gmail SMTP..."
            )

            servidor.login(
                GMAIL_USER,
                GMAIL_APP_PASSWORD
            )

            print(
                "✅ Autenticación Gmail correcta."
            )

            servidor.send_message(
                mensaje
            )

        print("")
        print(
            "✅ CORREO ÚNICO ENVIADO CORRECTAMENTE"
        )

        print(
            "Para:",
            EMAIL_DESTINO
        )

        print(
            "CC:",
            GMAIL_USER
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

    except smtplib.SMTPAuthenticationError as error:

        print("")
        print(
            "❌ Error de autenticación Gmail."
        )

        raise RuntimeError(
            "No fue posible autenticarse "
            "contra Gmail SMTP."
        ) from error

    except Exception as error:

        print("")
        print(
            "❌ Error enviando correo:"
        )

        print(
            str(error)
        )

        raise RuntimeError(
            "No fue posible enviar "
            "la notificación por correo."
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