from aura_login import login_aura

from reporte_id311_seguimiento_novedades import (
    ejecutar_reporte_id311,
)

from reporte_id31_novedades_calidad import (
    ejecutar_reporte_id31,
)

from repositorio import (
    subir_reporte_a_gdrive,
)

from notificaciones import (
    enviar_notificacion_reportes,
)


# ============================================================
# VOLVER A LA PÁGINA PRINCIPAL DE AURAQUANTIC
# ============================================================


def volver_a_home(page):

    print("")
    print("==========================================")
    print(" VOLVIENDO AL MENÚ PRINCIPAL AURAQUANTIC")
    print("==========================================")

    # --------------------------------------------------------
    # 1. VALIDAR QUE LA PESTAÑA SIGA ABIERTA
    # --------------------------------------------------------

    if page.is_closed():

        raise RuntimeError(
            "La pestaña principal de AuraQuantic "
            "se encuentra cerrada."
        )

    # --------------------------------------------------------
    # 2. TRAER PESTAÑA PRINCIPAL AL FRENTE
    # --------------------------------------------------------

    page.bring_to_front()

    print("✅ Pestaña principal activada.")

    print("URL actual de la pestaña principal:")
    print(page.url)

    # --------------------------------------------------------
    # 3. ASEGURAR QUE ESTAMOS EN HOME
    # --------------------------------------------------------

    if "Home.aspx" not in page.url:

        print("")
        print(
            "La pestaña principal no está en Home.aspx."
        )

        print(
            "Regresando a la página principal..."
        )

        partes_url = page.url.split("/")

        if len(partes_url) >= 3:

            url_home = (
                partes_url[0]
                + "//"
                + partes_url[2]
                + "/Home.aspx"
            )

        else:

            raise RuntimeError(
                "No fue posible determinar "
                "la URL principal de AuraQuantic."
            )

        page.goto(
            url_home,
            wait_until="domcontentloaded",
            timeout=120000
        )

        page.wait_for_timeout(
            5000
        )

    # --------------------------------------------------------
    # 4. VALIDACIÓN FINAL
    # --------------------------------------------------------

    if "Home.aspx" not in page.url:

        raise RuntimeError(
            "No fue posible regresar "
            "a Home.aspx de AuraQuantic."
        )

    print("")
    print("✅ MENÚ PRINCIPAL DISPONIBLE")

    print("URL:")
    print(page.url)

    return page


# ============================================================
# ROBOTPQR
# ============================================================


def main():

    print("")
    print("==========================================")
    print("              ASISTPQR v2")
    print("==========================================")

    # ========================================================
    # 1. LOGIN GENERAL
    #
    # Se realiza una sola vez.
    # ========================================================

    playwright, browser, context, page = login_aura()

    try:

        # ====================================================
        # 2. VALIDAR HOME
        # ====================================================

        volver_a_home(
            page
        )

        # ====================================================
        # 3. REPORTE ID 3.11
        # ====================================================

        print("")
        print("########################################")
        print("# INICIANDO REPORTE ID 3.11")
        print("########################################")

        archivo_id311 = ejecutar_reporte_id311(
            page,
            context
        )

        print("")
        print(
            "✅ Reporte ID 3.11 generado localmente."
        )

        print("Archivo:")
        print(archivo_id311)

        # ====================================================
        # 4. SUBIR ID 3.11 A GOOGLE DRIVE
        # ====================================================

        print("")
        print("########################################")
        print("# SUBIENDO REPORTE ID 3.11")
        print("########################################")

        info_drive_id311 = subir_reporte_a_gdrive(
            archivo_id311
        )

        if not info_drive_id311.get(
            "enlace_drive"
        ):

            raise RuntimeError(
                "El reporte ID 3.11 fue procesado, "
                "pero no se obtuvo su enlace "
                "de Google Drive."
            )

        print("")
        print(
            "✅ Reporte ID 3.11 confirmado "
            "en Google Drive."
        )

        print("Enlace:")

        print(
            info_drive_id311[
                "enlace_drive"
            ]
        )

        # ====================================================
        # 5. REGRESAR AL HOME
        # ====================================================

        print("")
        print("########################################")
        print("# PREPARANDO SEGUNDO REPORTE")
        print("########################################")

        volver_a_home(
            page
        )

        # ====================================================
        # 6. REPORTE ID 3.1
        # ====================================================

        print("")
        print("########################################")
        print("# INICIANDO REPORTE ID 3.1")
        print("########################################")

        archivo_id31 = ejecutar_reporte_id31(
            page,
            context
        )

        print("")
        print(
            "✅ Reporte ID 3.1 generado localmente."
        )

        print("Archivo:")
        print(archivo_id31)

        # ====================================================
        # 7. SUBIR ID 3.1 A GOOGLE DRIVE
        # ====================================================

        print("")
        print("########################################")
        print("# SUBIENDO REPORTE ID 3.1")
        print("########################################")

        info_drive_id31 = subir_reporte_a_gdrive(
            archivo_id31
        )

        if not info_drive_id31.get(
            "enlace_drive"
        ):

            raise RuntimeError(
                "El reporte ID 3.1 fue procesado, "
                "pero no se obtuvo su enlace "
                "de Google Drive."
            )

        print("")
        print(
            "✅ Reporte ID 3.1 confirmado "
            "en Google Drive."
        )

        print("Enlace:")

        print(
            info_drive_id31[
                "enlace_drive"
            ]
        )

        # ====================================================
        # 8. AMBOS REPORTES CONFIRMADOS
        # ====================================================

        print("")
        print("==========================================")
        print("✅ LOS DOS REPORTES ESTÁN EN GOOGLE DRIVE")
        print("==========================================")

        reporte_notificacion_id311 = {
            "archivo_local": archivo_id311,
            "enlace_drive": (
                info_drive_id311[
                    "enlace_drive"
                ]
            ),
        }

        reporte_notificacion_id31 = {
            "archivo_local": archivo_id31,
            "enlace_drive": (
                info_drive_id31[
                    "enlace_drive"
                ]
            ),
        }

        # ====================================================
        # 9. ENVIAR UN SOLO CORREO
        # ====================================================

        print("")
        print("########################################")
        print("# ENVIANDO NOTIFICACIÓN FINAL")
        print("########################################")

        enviar_notificacion_reportes(
            reporte_notificacion_id311,
            reporte_notificacion_id31
        )

        # ====================================================
        # 10. RESULTADO FINAL
        # ====================================================

        print("")
        print("==========================================")
        print("✅ ASISTPQR v2 COMPLETADO")
        print("==========================================")

        print("")
        print(
            "Flujo completado correctamente:"
        )

        print(
            "1. Login AuraQuantic"
        )

        print(
            "2. ID 3.11 generado"
        )

        print(
            "3. ID 3.11 subido a Google Drive"
        )

        print(
            "4. Regreso al menú principal"
        )

        print(
            "5. ID 3.1 generado"
        )

        print(
            "6. ID 3.1 subido a Google Drive"
        )

        print(
            "7. Un solo correo enviado "
            "con ambos enlaces"
        )

        print("")
        print("Reporte ID 3.11:")

        print(
            archivo_id311.name
            if hasattr(
                archivo_id311,
                "name"
            )
            else archivo_id311
        )

        print("")
        print("Reporte ID 3.1:")

        print(
            archivo_id31.name
            if hasattr(
                archivo_id31,
                "name"
            )
            else archivo_id31
        )

    # ========================================================
    # ERROR GENERAL
    # ========================================================

    except Exception as error:

        print("")
        print("==========================================")
        print("❌ ERROR EN ASISTPQR v2")
        print("==========================================")

        print("")
        print(str(error))

        # Mantiene código de salida de error.
        # Esto será importante para Railway.

        raise

    # ========================================================
    # CIERRE COMPLETAMENTE AUTOMÁTICO
    # ========================================================

    finally:

        print("")
        print("Cerrando navegador...")

        try:

            browser.close()

            print(
                "✅ Navegador cerrado."
            )

        except Exception as error_cierre:

            print(
                "⚠️ No fue posible cerrar "
                "el navegador normalmente:"
            )

            print(
                str(error_cierre)
            )

        try:

            playwright.stop()

            print(
                "✅ Playwright finalizado."
            )

        except Exception as error_playwright:

            print(
                "⚠️ No fue posible finalizar "
                "Playwright normalmente:"
            )

            print(
                str(error_playwright)
            )

        print("")
        print(
            "✅ Ejecución finalizada automáticamente."
        )


# ============================================================
# INICIO
# ============================================================


if __name__ == "__main__":
    main()