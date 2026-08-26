from aura_login import login_aura

from reporte_id311_seguimiento_novedades import (
    ejecutar_reporte_id311,
)

from reporte_id31_novedades_calidad import (
    ejecutar_reporte_id31,
)

from generador_json import (
    generar_json_desde_excel,
)

from repositorio import (
    subir_reporte_a_gdrive,
)

from notificaciones import (
    enviar_notificacion_reportes,
)


# ============================================================
# VOLVER A HOME
# ============================================================


def volver_a_home(page):

    print("")
    print("==========================================")
    print(" VOLVIENDO AL MENÚ PRINCIPAL AURAQUANTIC")
    print("==========================================")

    if page.is_closed():

        raise RuntimeError(
            "La pestaña principal de AuraQuantic "
            "se encuentra cerrada."
        )

    page.bring_to_front()

    print(
        "✅ Pestaña principal activada."
    )

    print(
        "URL actual:"
    )

    print(
        page.url
    )

    if "Home.aspx" not in page.url:

        print("")
        print(
            "Regresando a Home.aspx..."
        )

        partes_url = page.url.split(
            "/"
        )

        if len(partes_url) < 3:

            raise RuntimeError(
                "No fue posible determinar "
                "la URL de AuraQuantic."
            )

        url_home = (
            partes_url[0]
            + "//"
            + partes_url[2]
            + "/Home.aspx"
        )

        page.goto(
            url_home,
            wait_until="domcontentloaded",
            timeout=120000
        )

        page.wait_for_timeout(
            5000
        )

    if "Home.aspx" not in page.url:

        raise RuntimeError(
            "No fue posible regresar "
            "a Home.aspx."
        )

    print("")
    print(
        "✅ MENÚ PRINCIPAL DISPONIBLE"
    )

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
    # 1. LOGIN
    # ========================================================

    playwright, browser, context, page = (
        login_aura()
    )

    try:

        volver_a_home(
            page
        )

        # ====================================================
        # 2. REPORTE ID 3.11
        # ====================================================

        print("")
        print("########################################")
        print("# INICIANDO REPORTE ID 3.11")
        print("########################################")

        archivo_id311 = (
            ejecutar_reporte_id311(
                page,
                context
            )
        )

        print("")
        print(
            "✅ Excel ID 3.11 generado."
        )

        # ====================================================
        # 3. GENERAR JSON ID 3.11
        # ====================================================

        json_id311 = (
            generar_json_desde_excel(
                archivo_excel=archivo_id311,
                reporte_id="3.11",
                reporte_nombre=(
                    "Reporte de seguimiento "
                    "de novedades PQR"
                ),
            )
        )

        # ====================================================
        # 4. SUBIR XLSX ID 3.11
        # ====================================================

        print("")
        print("########################################")
        print("# SUBIENDO XLSX ID 3.11")
        print("########################################")

        info_drive_id311 = (
            subir_reporte_a_gdrive(
                archivo_id311
            )
        )

        if not info_drive_id311.get(
            "enlace_drive"
        ):

            raise RuntimeError(
                "No se obtuvo enlace Drive "
                "para XLSX ID 3.11."
            )

        # ====================================================
        # 5. SUBIR JSON ID 3.11
        # ====================================================

        print("")
        print("########################################")
        print("# SUBIENDO JSON ID 3.11")
        print("########################################")

        info_json_id311 = (
            subir_reporte_a_gdrive(
                json_id311
            )
        )

        if not info_json_id311.get(
            "enlace_drive"
        ):

            raise RuntimeError(
                "No se obtuvo enlace Drive "
                "para JSON ID 3.11."
            )

        print("")
        print(
            "✅ ID 3.11 XLSX + JSON "
            "confirmados en Google Drive."
        )

        # ====================================================
        # 6. VOLVER HOME
        # ====================================================

        volver_a_home(
            page
        )

        # ====================================================
        # 7. REPORTE ID 3.1
        # ====================================================

        print("")
        print("########################################")
        print("# INICIANDO REPORTE ID 3.1")
        print("########################################")

        archivo_id31 = (
            ejecutar_reporte_id31(
                page,
                context
            )
        )

        print("")
        print(
            "✅ Excel ID 3.1 generado."
        )

        # ====================================================
        # 8. GENERAR JSON ID 3.1
        # ====================================================

        json_id31 = (
            generar_json_desde_excel(
                archivo_excel=archivo_id31,
                reporte_id="3.1",
                reporte_nombre=(
                    "Reporte de novedades"
                ),
            )
        )

        # ====================================================
        # 9. SUBIR XLSX ID 3.1
        # ====================================================

        print("")
        print("########################################")
        print("# SUBIENDO XLSX ID 3.1")
        print("########################################")

        info_drive_id31 = (
            subir_reporte_a_gdrive(
                archivo_id31
            )
        )

        if not info_drive_id31.get(
            "enlace_drive"
        ):

            raise RuntimeError(
                "No se obtuvo enlace Drive "
                "para XLSX ID 3.1."
            )

        # ====================================================
        # 10. SUBIR JSON ID 3.1
        # ====================================================

        print("")
        print("########################################")
        print("# SUBIENDO JSON ID 3.1")
        print("########################################")

        info_json_id31 = (
            subir_reporte_a_gdrive(
                json_id31
            )
        )

        if not info_json_id31.get(
            "enlace_drive"
        ):

            raise RuntimeError(
                "No se obtuvo enlace Drive "
                "para JSON ID 3.1."
            )

        print("")
        print(
            "✅ ID 3.1 XLSX + JSON "
            "confirmados en Google Drive."
        )

        # ====================================================
        # 11. VALIDACIÓN GENERAL
        # ====================================================

        print("")
        print("==========================================")
        print("✅ CAPA DE DATOS ACTUALIZADA")
        print("==========================================")

        print("")
        print(
            "Archivos generados:"
        )

        print("")
        print(
            "ID 3.11 XLSX:"
        )
        print(
            archivo_id311.name
        )

        print(
            "ID 3.11 JSON:"
        )
        print(
            json_id311.name
        )

        print("")
        print(
            "ID 3.1 XLSX:"
        )
        print(
            archivo_id31.name
        )

        print(
            "ID 3.1 JSON:"
        )
        print(
            json_id31.name
        )

        # ====================================================
        # 12. PREPARAR NOTIFICACIÓN
        #
        # Los enlaces visibles para el usuario continúan
        # siendo los Excel.
        # ====================================================

        reporte_notificacion_id311 = {

            "archivo_local": (
                archivo_id311
            ),

            "enlace_drive": (
                info_drive_id311[
                    "enlace_drive"
                ]
            ),
        }

        reporte_notificacion_id31 = {

            "archivo_local": (
                archivo_id31
            ),

            "enlace_drive": (
                info_drive_id31[
                    "enlace_drive"
                ]
            ),
        }

        # ====================================================
        # 13. CORREO ÚNICO
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
        # 14. FIN
        # ====================================================

        print("")
        print("==========================================")
        print("✅ ASISTPQR v2 COMPLETADO")
        print("==========================================")

        print("")
        print(
            "✅ 2 reportes Excel generados"
        )

        print(
            "✅ 2 archivos JSON generados"
        )

        print(
            "✅ 4 archivos almacenados "
            "en Google Drive"
        )

        print(
            "✅ Correo único enviado"
        )

    except Exception as error:

        print("")
        print("==========================================")
        print("❌ ERROR EN ASISTPQR v2")
        print("==========================================")

        print("")
        print(
            str(error)
        )

        raise

    finally:

        print("")
        print(
            "Cerrando navegador..."
        )

        try:

            browser.close()

            print(
                "✅ Navegador cerrado."
            )

        except Exception as error_cierre:

            print(
                "⚠️ Error cerrando navegador:"
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
                "⚠️ Error finalizando Playwright:"
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