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
        #
        # IMPORTANTE:
        # ID 3.11 ES EL REPORTE PRINCIPAL.
        # CUALQUIER ERROR EN ESTE BLOQUE SIGUE SIENDO CRÍTICO.
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
        #
        # MODO DE CONTINGENCIA:
        # ID 3.1 ES TEMPORALMENTE NO CRÍTICO.
        #
        # Si AuraQuantic abre un reporte incorrecto,
        # no encuentra campos, genera timeout o falla
        # cualquier etapa del procesamiento, ASISTPQR
        # continuará utilizando únicamente ID 3.11.
        # ====================================================

        archivo_id31 = None
        json_id31 = None
        info_drive_id31 = None
        info_json_id31 = None
        error_id31 = None

        print("")
        print("########################################")
        print("# INICIANDO REPORTE ID 3.1")
        print("# MODO NO CRÍTICO / CONTINGENCIA")
        print("########################################")

        try:

            # ================================================
            # 7.1 GENERAR EXCEL ID 3.1
            # ================================================

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

            # ================================================
            # 7.2 GENERAR JSON ID 3.1
            # ================================================

            json_id31 = (
                generar_json_desde_excel(
                    archivo_excel=archivo_id31,
                    reporte_id="3.1",
                    reporte_nombre=(
                        "Reporte de novedades"
                    ),
                )
            )

            # ================================================
            # 7.3 SUBIR XLSX ID 3.1
            # ================================================

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

            # ================================================
            # 7.4 SUBIR JSON ID 3.1
            # ================================================

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

        except Exception as error:

            error_id31 = str(error)

            # Evitamos que variables parcialmente generadas
            # sean consideradas válidas más adelante.
            archivo_id31 = None
            json_id31 = None
            info_drive_id31 = None
            info_json_id31 = None

            print("")
            print("==========================================")
            print("⚠️ ADVERTENCIA - ID 3.1 NO DISPONIBLE")
            print("==========================================")

            print("")
            print(
                "El reporte ID 3.1 no pudo "
                "procesarse correctamente."
            )

            print("")
            print(
                "Motivo:"
            )

            print(
                error_id31
            )

            print("")
            print(
                "⚠️ ID 3.1 será omitido "
                "en esta ejecución."
            )

            print(
                "✅ ID 3.11 ya fue generado "
                "y almacenado correctamente."
            )

            print(
                "➡️ ASISTPQR continuará "
                "sin provocar CRASH."
            )

        # ====================================================
        # 8. VALIDACIÓN GENERAL
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

        if archivo_id31 is not None:

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

        else:

            print("")
            print(
                "⚠️ ID 3.1:"
            )

            print(
                "No actualizado en esta ejecución."
            )

        # ====================================================
        # 9. PREPARAR NOTIFICACIÓN
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

        reporte_notificacion_id31 = None

        if (
            archivo_id31 is not None
            and info_drive_id31 is not None
            and info_drive_id31.get(
                "enlace_drive"
            )
        ):

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
        # 10. CORREO FINAL
        #
        # Si ID 3.1 está disponible se conserva el
        # comportamiento normal.
        #
        # Si ID 3.1 falló, intentamos enviar la notificación
        # únicamente con ID 3.11.
        # ====================================================

        print("")
        print("########################################")
        print("# ENVIANDO NOTIFICACIÓN FINAL")
        print("########################################")

        if reporte_notificacion_id31 is not None:

            enviar_notificacion_reportes(
                reporte_notificacion_id311,
                reporte_notificacion_id31
            )

        else:

            try:

                enviar_notificacion_reportes(
                    reporte_notificacion_id311,
                    None
                )

            except Exception as error_notificacion:

                print("")
                print(
                    "⚠️ La función actual de notificación "
                    "no admite ID 3.1 vacío."
                )

                print(
                    "La actualización del ID 3.11 "
                    "permanece válida."
                )

                print("")
                print(
                    "Detalle de notificación:"
                )

                print(
                    str(error_notificacion)
                )

                print("")
                print(
                    "⚠️ El error de notificación "
                    "no provocará CRASH."
                )

        # ====================================================
        # 11. FIN
        # ====================================================

        print("")
        print("==========================================")
        print("✅ ASISTPQR v2 COMPLETADO")
        print("==========================================")

        if archivo_id31 is not None:

            print("")
            print(
                "✅ ID 3.11 actualizado correctamente"
            )

            print(
                "✅ ID 3.1 actualizado correctamente"
            )

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

        else:

            print("")
            print(
                "✅ ID 3.11 actualizado correctamente"
            )

            print(
                "✅ Excel ID 3.11 generado"
            )

            print(
                "✅ JSON ID 3.11 generado"
            )

            print(
                "✅ ID 3.11 almacenado "
                "en Google Drive"
            )

            print("")
            print(
                "⚠️ ID 3.1 no fue actualizado"
            )

            print(
                "⚠️ Ejecución completada "
                "en MODO CONTINGENCIA"
            )

            if error_id31:

                print("")
                print(
                    "Motivo ID 3.1:"
                )

                print(
                    error_id31
                )

    except Exception as error:

        # ====================================================
        # ERROR GENERAL
        #
        # Este bloque continúa siendo crítico para errores
        # fuera del ID 3.1, especialmente:
        # login, ID 3.11, JSON 3.11 y Google Drive 3.11.
        # ====================================================

        print("")
        print("==========================================")
        print("❌ ERROR CRÍTICO EN ASISTPQR v2")
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