import time

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


# ============================================================
# ID 3.11
# REPORTE DE SEGUIMIENTO DE NOVEDADES PQR
# ============================================================


def abrir_reporte_seguimiento(page, context):

    print("")
    print("=== ID 3.11 - REPORTE SEGUIMIENTO DE NOVEDADES ===")

    print("Buscando menú Informes...")

    menu_informes = page.get_by_text(
        "Informes",
        exact=True
    )

    menu_informes.wait_for(
        state="visible",
        timeout=60000
    )

    menu_informes.scroll_into_view_if_needed()
    menu_informes.click()

    print("✅ Menú Informes desplegado.")

    time.sleep(3)

    print("Buscando Rep. Seguimiento de novedades...")

    reporte = page.get_by_text(
        "Rep. Seguimiento de novedades",
        exact=True
    )

    reporte.wait_for(
        state="visible",
        timeout=60000
    )

    reporte.scroll_into_view_if_needed()

    print("✅ Rep. Seguimiento de novedades encontrado.")

    print("Abriendo Rep. Seguimiento de novedades...")

    with context.expect_page(
        timeout=60000
    ) as nueva_pagina_info:

        reporte.click()

    reporte_page = nueva_pagina_info.value

    print("✅ Nueva pestaña detectada.")

    reporte_page.wait_for_load_state(
        "domcontentloaded",
        timeout=120000
    )

    print("Esperando carga dinámica del reporte...")

    time.sleep(10)

    print("URL del reporte:")
    print(reporte_page.url)

    print("Título:")
    print(reporte_page.title())

    print(
        "Cantidad de frames detectados:",
        len(reporte_page.frames)
    )

    reporte_page.screenshot(
        path="downloads/reporte_id311_abierto.png",
        full_page=True
    )

    return reporte_page


def llenar_fechas_reporte(reporte_page):

    print("")
    print("=== ID 3.11 - LLENANDO FECHAS ===")

    fecha_desde = "2026-01-01"

    fecha_hasta = datetime.now(
        ZoneInfo("America/Guayaquil")
    ).strftime("%Y-%m-%d")

    print("Fecha Ingreso Desde:", fecha_desde)
    print("Fecha Ingreso Hasta:", fecha_hasta)

    campo_desde = reporte_page.locator(
        '[id="1163_Ini_date"]'
    )

    campo_desde.wait_for(
        state="visible",
        timeout=60000
    )

    campo_desde.fill(fecha_desde)

    print("✅ Fecha Ingreso Desde cargada.")

    campo_hasta = reporte_page.locator(
        '[id="1163_End_date"]'
    )

    campo_hasta.wait_for(
        state="visible",
        timeout=60000
    )

    campo_hasta.fill(fecha_hasta)

    print("✅ Fecha Ingreso Hasta cargada.")

    time.sleep(2)

    valor_desde = campo_desde.input_value()
    valor_hasta = campo_hasta.input_value()

    print("")
    print("Valores verificados:")
    print("Desde:", valor_desde)
    print("Hasta:", valor_hasta)

    if valor_desde != fecha_desde:
        raise RuntimeError(
            "Fecha Ingreso Desde incorrecta."
        )

    if valor_hasta != fecha_hasta:
        raise RuntimeError(
            "Fecha Ingreso Hasta incorrecta."
        )

    reporte_page.screenshot(
        path="downloads/reporte_id311_fechas.png",
        full_page=True
    )


def proceder_reporte(reporte_page):

    print("")
    print("=== ID 3.11 - EJECUTANDO REPORTE ===")

    print("Buscando botón Proceder...")

    boton_proceder = None

    reporte_page.wait_for_timeout(3000)

    print(
        "Frames disponibles:",
        len(reporte_page.frames)
    )

    for numero, frame in enumerate(
        reporte_page.frames
    ):

        try:

            print(
                f"Revisando frame {numero}:",
                frame.url
            )

            candidato = frame.get_by_text(
                "Proceder",
                exact=True
            )

            cantidad = candidato.count()

            if cantidad > 0:

                print(
                    f"Encontrado texto Proceder "
                    f"en frame {numero}."
                )

                for indice in range(cantidad):

                    elemento = candidato.nth(indice)

                    try:

                        if elemento.is_visible():

                            boton_proceder = elemento

                            print(
                                "✅ Botón Proceder visible "
                                f"en frame {numero}."
                            )

                            break

                    except Exception:
                        continue

            if boton_proceder is not None:
                break

        except Exception:
            continue

    if boton_proceder is None:

        print("Intentando búsqueda alternativa...")

        for numero, frame in enumerate(
            reporte_page.frames
        ):

            try:

                candidato = frame.get_by_role(
                    "link",
                    name="Proceder"
                )

                if (
                    candidato.count() > 0
                    and candidato.first.is_visible()
                ):

                    boton_proceder = candidato.first

                    print(
                        "✅ Proceder encontrado como "
                        f"enlace en frame {numero}."
                    )

                    break

            except Exception:
                pass

    if boton_proceder is None:

        raise RuntimeError(
            "No fue posible encontrar Proceder."
        )

    boton_proceder.scroll_into_view_if_needed()

    reporte_page.wait_for_timeout(1500)

    print("Presionando Proceder...")

    boton_proceder.click(
        timeout=60000
    )

    print("✅ Click en Proceder ejecutado.")

    print("Esperando procesamiento...")

    reporte_page.wait_for_timeout(10000)

    try:

        reporte_page.wait_for_load_state(
            "networkidle",
            timeout=60000
        )

        print("✅ Red estabilizada.")

    except Exception:

        print(
            "AuraQuantic mantiene actividad de red."
        )

    reporte_page.wait_for_timeout(5000)

    print("✅ Reporte ID 3.11 procesado.")

    reporte_page.screenshot(
        path="downloads/reporte_id311_despues_proceder.png",
        full_page=True
    )


def generar_nombre_archivo_id311():

    momento_ecuador = datetime.now(
        ZoneInfo("America/Guayaquil")
    )

    fecha_corte = momento_ecuador.strftime(
        "%d%m%Y"
    )

    hora_corte = momento_ecuador.strftime(
        "%H%M"
    )

    return (
        "3.11- Reporte de seguimiento de novedades PQR "
        f"01012026-{fecha_corte}-{hora_corte}.xlsx"
    )


def exportar_excel_con_formato(reporte_page):

    print("")
    print("=== ID 3.11 - EXPORTANDO EXCEL ===")

    reporte_page.wait_for_timeout(5000)

    opcion_exportar = None

    print(
        "Buscando control Exportar con formato..."
    )

    for numero, frame in enumerate(
        reporte_page.frames
    ):

        try:

            candidato = frame.locator(
                '[id="bExcelFormatCtrlGrid_869"]'
            )

            if candidato.count() > 0:

                opcion_exportar = candidato.first

                print(
                    "✅ Exportar con formato encontrado "
                    f"en frame {numero}."
                )

                break

        except Exception:
            continue

    if opcion_exportar is None:

        for numero, frame in enumerate(
            reporte_page.frames
        ):

            try:

                candidato = frame.get_by_text(
                    "Exportar con formato",
                    exact=True
                )

                if candidato.count() > 0:

                    opcion_exportar = candidato.first

                    print(
                        "✅ Exportar con formato encontrado "
                        f"por texto en frame {numero}."
                    )

                    break

            except Exception:
                continue

    if opcion_exportar is None:

        raise RuntimeError(
            "No fue posible localizar "
            "Exportar con formato."
        )

    carpeta_downloads = Path("downloads")

    carpeta_downloads.mkdir(
        parents=True,
        exist_ok=True
    )

    nombre_archivo = generar_nombre_archivo_id311()

    archivo_destino = (
        carpeta_downloads
        / nombre_archivo
    )

    descargas_detectadas = []
    respuestas_excel = []

    def registrar_descarga(download):

        print("📥 Evento DOWNLOAD detectado.")

        descargas_detectadas.append(
            download
        )

    def registrar_respuesta(response):

        try:

            headers = response.headers

            content_type = headers.get(
                "content-type",
                ""
            ).lower()

            content_disposition = headers.get(
                "content-disposition",
                ""
            ).lower()

            es_excel = (
                "spreadsheet" in content_type
                or "ms-excel" in content_type
                or "application/vnd.ms" in content_type
                or ".xlsx" in content_disposition
                or ".xls" in content_disposition
            )

            if es_excel:

                print(
                    "📡 Respuesta Excel detectada."
                )

                respuestas_excel.append(
                    response
                )

        except Exception:
            pass

    reporte_page.on(
        "download",
        registrar_descarga
    )

    reporte_page.on(
        "response",
        registrar_respuesta
    )

    print("Presionando Exportar con formato...")

    opcion_exportar.evaluate(
        "elemento => elemento.click()"
    )

    print("✅ Click ejecutado.")

    tiempo_maximo = 120
    intervalo = 2
    tiempo_transcurrido = 0

    while tiempo_transcurrido < tiempo_maximo:

        if descargas_detectadas:
            break

        if respuestas_excel:
            break

        reporte_page.wait_for_timeout(
            intervalo * 1000
        )

        tiempo_transcurrido += intervalo

        if tiempo_transcurrido % 10 == 0:

            print(
                f"Esperando exportación... "
                f"{tiempo_transcurrido}s"
            )

    if descargas_detectadas:

        descarga = descargas_detectadas[0]

        descarga.save_as(
            str(archivo_destino)
        )

        print(
            "✅ Excel descargado mediante evento "
            "DOWNLOAD."
        )

    elif respuestas_excel:

        response = respuestas_excel[0]

        contenido = response.body()

        with open(
            archivo_destino,
            "wb"
        ) as archivo:

            archivo.write(
                contenido
            )

        print(
            "✅ Excel guardado desde "
            "respuesta HTTP."
        )

    else:

        raise RuntimeError(
            "AuraQuantic no generó "
            "una exportación Excel detectable."
        )

    if not archivo_destino.exists():

        raise RuntimeError(
            "El archivo Excel no fue generado."
        )

    tamano = archivo_destino.stat().st_size

    if tamano <= 0:

        raise RuntimeError(
            "El Excel generado está vacío."
        )

    print("")
    print("✅ EXCEL ID 3.11 VALIDADO")
    print("Nombre:", archivo_destino.name)
    print("Tamaño:", tamano, "bytes")

    return archivo_destino


def ejecutar_reporte_id311(page, context):

    print("")
    print("########################################")
    print("# ID 3.11 - SEGUIMIENTO DE NOVEDADES")
    print("########################################")

    reporte_page = abrir_reporte_seguimiento(
        page,
        context
    )

    llenar_fechas_reporte(
        reporte_page
    )

    proceder_reporte(
        reporte_page
    )

    archivo_excel = exportar_excel_con_formato(
        reporte_page
    )

    print("")
    print("✅ ID 3.11 COMPLETADO")

    return archivo_excel