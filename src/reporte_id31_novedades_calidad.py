import time

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


# ============================================================
# ID 3.1
# REPORTE DE NOVEDADES DE CALIDAD
# ============================================================


def abrir_reporte_novedades_calidad(page, context):

    print("")
    print("==========================================")
    print(" ID 3.1 - REPORTE NOVEDADES DE CALIDAD")
    print("==========================================")

    # --------------------------------------------------------
    # 1. LOCALIZAR REP. NOVEDADES DE CALIDAD
    #
    # Antes de tocar el menú verificamos si el reporte
    # ya está visible. Esto puede ocurrir cuando ID 3.11
    # se ejecutó antes dentro de la misma sesión.
    # --------------------------------------------------------

    print("")
    print("Buscando Rep. Novedades de Calidad...")

    reporte = page.locator(
        '[id="Item_950"]'
    )

    reporte_visible = False

    try:
        if reporte.count() > 0:
            reporte_visible = reporte.first.is_visible()
    except Exception:
        reporte_visible = False

    # --------------------------------------------------------
    # 2. ABRIR MENÚ INFORMES SOLO SI ES NECESARIO
    #
    # Importante:
    # Ya no usamos get_by_text("Informes") porque AuraQuantic
    # también genera un tooltip con el mismo texto.
    #
    # Usamos específicamente el link real del menú.
    # --------------------------------------------------------

    if not reporte_visible:

        print(
            "Rep. Novedades de Calidad todavía no está visible."
        )

        print("Buscando menú Informes...")

        menu_informes = page.get_by_role(
            "link",
            name="Informes",
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

    else:

        print(
            "✅ Menú Informes ya estaba desplegado."
        )

    # --------------------------------------------------------
    # 3. BUSCAR REP. NOVEDADES DE CALIDAD
    #
    # HTML observado:
    #
    # <a id="Item_950"
    #    target="_blank"
    #    coptitle="Rep. Novedades de Calidad">
    # --------------------------------------------------------

    reporte = page.locator(
        '[id="Item_950"]'
    )

    # Respaldo por texto si el ID dejara de existir
    if reporte.count() == 0:

        print(
            "No encontrado por ID. "
            "Intentando búsqueda por texto..."
        )

        reporte = page.get_by_text(
            "Rep. Novedades de Calidad",
            exact=True
        ).first

    reporte.wait_for(
        state="visible",
        timeout=60000
    )

    reporte.scroll_into_view_if_needed()

    print(
        "✅ Rep. Novedades de Calidad encontrado."
    )

    # --------------------------------------------------------
    # 4. ABRIR EN NUEVA PESTAÑA
    # --------------------------------------------------------

    print("")
    print(
        "Abriendo Rep. Novedades de Calidad..."
    )

    with context.expect_page(
        timeout=60000
    ) as nueva_pagina_info:

        reporte.click()

    reporte_page = nueva_pagina_info.value

    print("✅ Nueva pestaña detectada.")

    # --------------------------------------------------------
    # 5. ESPERAR CARGA
    # --------------------------------------------------------

    print("")
    print(
        "Esperando carga inicial del reporte..."
    )

    reporte_page.wait_for_load_state(
        "domcontentloaded",
        timeout=120000
    )

    time.sleep(10)

    print("")
    print("URL del reporte:")
    print(reporte_page.url)

    print("")
    print("Título:")
    print(reporte_page.title())

    print("")
    print(
        "Cantidad de frames detectados:",
        len(reporte_page.frames)
    )

    reporte_page.screenshot(
        path="downloads/reporte_id31_abierto.png",
        full_page=True
    )

    print("")
    print(
        "✅ Captura guardada en "
        "downloads/reporte_id31_abierto.png"
    )

    return reporte_page


# ============================================================
# LLENAR FECHAS
# ============================================================


def llenar_fechas_reporte(reporte_page):

    print("")
    print("=== ID 3.1 - LLENANDO FECHAS ===")

    # Fecha inicial fija
    fecha_desde = "2026-01-01"

    # Fecha final dinámica en Ecuador
    fecha_hasta = datetime.now(
        ZoneInfo("America/Guayaquil")
    ).strftime("%Y-%m-%d")

    print(
        "Fecha Ingreso Desde:",
        fecha_desde
    )

    print(
        "Fecha Ingreso Hasta:",
        fecha_hasta
    )

    # --------------------------------------------------------
    # FECHA INGRESO DESDE
    # ID: 871_Ini_date
    # --------------------------------------------------------

    campo_desde = reporte_page.locator(
        '[id="871_Ini_date"]'
    )

    campo_desde.wait_for(
        state="visible",
        timeout=60000
    )

    campo_desde.fill(
        fecha_desde
    )

    print(
        "✅ Fecha Ingreso Desde cargada."
    )

    # --------------------------------------------------------
    # FECHA INGRESO HASTA
    # ID: 871_End_date
    # --------------------------------------------------------

    campo_hasta = reporte_page.locator(
        '[id="871_End_date"]'
    )

    campo_hasta.wait_for(
        state="visible",
        timeout=60000
    )

    campo_hasta.fill(
        fecha_hasta
    )

    print(
        "✅ Fecha Ingreso Hasta cargada."
    )

    time.sleep(2)

    # --------------------------------------------------------
    # VALIDAR
    # --------------------------------------------------------

    valor_desde = (
        campo_desde.input_value()
    )

    valor_hasta = (
        campo_hasta.input_value()
    )

    print("")
    print("Valores verificados:")

    print(
        "Desde:",
        valor_desde
    )

    print(
        "Hasta:",
        valor_hasta
    )

    if valor_desde != fecha_desde:

        raise RuntimeError(
            "Fecha Ingreso Desde incorrecta "
            "en ID 3.1."
        )

    if valor_hasta != fecha_hasta:

        raise RuntimeError(
            "Fecha Ingreso Hasta incorrecta "
            "en ID 3.1."
        )

    reporte_page.screenshot(
        path="downloads/reporte_id31_fechas.png",
        full_page=True
    )

    print("")
    print(
        "✅ Fechas ID 3.1 validadas."
    )


# ============================================================
# PROCEDER
# ============================================================


def proceder_reporte(reporte_page):

    print("")
    print("=== ID 3.1 - EJECUTANDO REPORTE ===")

    print(
        "Buscando botón Proceder..."
    )

    boton_proceder = None

    reporte_page.wait_for_timeout(
        3000
    )

    print(
        "Frames disponibles:",
        len(reporte_page.frames)
    )

    # --------------------------------------------------------
    # BUSCAR PROCEDER EN TODOS LOS FRAMES
    # --------------------------------------------------------

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

                for indice in range(
                    cantidad
                ):

                    elemento = (
                        candidato.nth(indice)
                    )

                    try:

                        if elemento.is_visible():

                            boton_proceder = (
                                elemento
                            )

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

    # --------------------------------------------------------
    # RESPALDO POR ID
    # --------------------------------------------------------

    if boton_proceder is None:

        print(
            "No encontrado por texto. "
            "Intentando por ID..."
        )

        for numero, frame in enumerate(
            reporte_page.frames
        ):

            try:

                candidato = frame.locator(
                    '[id="lbtnProceed"]'
                )

                if candidato.count() > 0:

                    boton_proceder = (
                        candidato.first
                    )

                    print(
                        "✅ Proceder encontrado "
                        f"por ID en frame {numero}."
                    )

                    break

            except Exception:
                continue

    if boton_proceder is None:

        reporte_page.screenshot(
            path=(
                "downloads/"
                "error_id31_proceder.png"
            ),
            full_page=True
        )

        raise RuntimeError(
            "No fue posible encontrar "
            "el botón Proceder del ID 3.1."
        )

    # --------------------------------------------------------
    # CLICK PROCEDER
    # --------------------------------------------------------

    boton_proceder.scroll_into_view_if_needed()

    reporte_page.wait_for_timeout(
        1500
    )

    print("")
    print(
        "Presionando Proceder..."
    )

    boton_proceder.click(
        timeout=60000
    )

    print(
        "✅ Click en Proceder ejecutado."
    )

    # --------------------------------------------------------
    # ESPERAR PROCESAMIENTO
    # --------------------------------------------------------

    print("")
    print(
        "Esperando procesamiento "
        "de AuraQuantic..."
    )

    reporte_page.wait_for_timeout(
        10000
    )

    try:

        reporte_page.wait_for_load_state(
            "networkidle",
            timeout=60000
        )

        print(
            "✅ Red estabilizada."
        )

    except Exception:

        print(
            "AuraQuantic mantiene actividad "
            "de red; continuamos."
        )

    reporte_page.wait_for_timeout(
        5000
    )

    print(
        "✅ Reporte ID 3.1 procesado."
    )

    reporte_page.screenshot(
        path=(
            "downloads/"
            "reporte_id31_despues_proceder.png"
        ),
        full_page=True
    )


# ============================================================
# NOMBRE DINÁMICO
# ============================================================


def generar_nombre_archivo_id31():

    momento_ecuador = datetime.now(
        ZoneInfo("America/Guayaquil")
    )

    fecha_corte = (
        momento_ecuador.strftime(
            "%d%m%Y"
        )
    )

    hora_corte = (
        momento_ecuador.strftime(
            "%H%M"
        )
    )

    return (
        "3.1- Reporte de novedades "
        f"01012026-{fecha_corte}-"
        f"{hora_corte}.xlsx"
    )


# ============================================================
# EXPORTAR EXCEL
# ============================================================


def exportar_excel_con_formato(
    reporte_page
):

    print("")
    print(
        "=== ID 3.1 - EXPORTANDO EXCEL ==="
    )

    print(
        "Esperando que la tabla termine "
        "de actualizarse..."
    )

    reporte_page.wait_for_timeout(
        5000
    )

    opcion_exportar = None

    # --------------------------------------------------------
    # ID OBSERVADO:
    # bExcelFormatCtrlGrid_229
    # --------------------------------------------------------

    print("")
    print(
        "Buscando control "
        "bExcelFormatCtrlGrid_229..."
    )

    for numero, frame in enumerate(
        reporte_page.frames
    ):

        try:

            candidato = frame.locator(
                '[id="bExcelFormatCtrlGrid_229"]'
            )

            if candidato.count() > 0:

                opcion_exportar = (
                    candidato.first
                )

                print(
                    "✅ Exportar con formato "
                    f"encontrado en frame {numero}."
                )

                break

        except Exception:
            continue

    # --------------------------------------------------------
    # RESPALDO POR TEXTO
    # --------------------------------------------------------

    if opcion_exportar is None:

        print(
            "No encontrado por ID. "
            "Buscando por texto..."
        )

        for numero, frame in enumerate(
            reporte_page.frames
        ):

            try:

                candidato = frame.get_by_text(
                    "Exportar con formato",
                    exact=True
                )

                if candidato.count() > 0:

                    opcion_exportar = (
                        candidato.first
                    )

                    print(
                        "✅ Exportar con formato "
                        f"encontrado por texto "
                        f"en frame {numero}."
                    )

                    break

            except Exception:
                continue

    if opcion_exportar is None:

        reporte_page.screenshot(
            path=(
                "downloads/"
                "error_id31_exportar.png"
            ),
            full_page=True
        )

        raise RuntimeError(
            "No fue posible localizar "
            "Exportar con formato "
            "del ID 3.1."
        )

    # --------------------------------------------------------
    # ARCHIVO DESTINO
    # --------------------------------------------------------

    carpeta_downloads = Path(
        "downloads"
    )

    carpeta_downloads.mkdir(
        parents=True,
        exist_ok=True
    )

    nombre_archivo = (
        generar_nombre_archivo_id31()
    )

    archivo_destino = (
        carpeta_downloads
        / nombre_archivo
    )

    print("")
    print(
        "Nombre de archivo destino:"
    )

    print(
        nombre_archivo
    )

    # --------------------------------------------------------
    # CAPTURA DE EXPORTACIÓN
    # --------------------------------------------------------

    descargas_detectadas = []
    respuestas_excel = []

    def registrar_descarga(download):

        print("")
        print(
            "📥 Evento DOWNLOAD detectado."
        )

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
                or "application/vnd.ms"
                in content_type
                or ".xlsx"
                in content_disposition
                or ".xls"
                in content_disposition
            )

            if es_excel:

                print("")
                print(
                    "📡 Respuesta Excel detectada."
                )

                print(
                    "URL:",
                    response.url
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

    # --------------------------------------------------------
    # CLICK EXPORTAR
    # --------------------------------------------------------

    print("")
    print(
        "Presionando Exportar con formato..."
    )

    opcion_exportar.evaluate(
        "elemento => elemento.click()"
    )

    print(
        "✅ Click ejecutado."
    )

    # --------------------------------------------------------
    # ESPERAR EXPORTACIÓN
    # --------------------------------------------------------

    tiempo_maximo = 120
    intervalo = 2
    tiempo_transcurrido = 0

    while (
        tiempo_transcurrido
        < tiempo_maximo
    ):

        if descargas_detectadas:
            break

        if respuestas_excel:
            break

        reporte_page.wait_for_timeout(
            intervalo * 1000
        )

        tiempo_transcurrido += (
            intervalo
        )

        if (
            tiempo_transcurrido
            % 10
            == 0
        ):

            print(
                "Esperando exportación... "
                f"{tiempo_transcurrido}s"
            )

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    if descargas_detectadas:

        descarga = (
            descargas_detectadas[0]
        )

        print("")
        print(
            "✅ Descarga estándar detectada."
        )

        print(
            "Nombre original:",
            descarga.suggested_filename
        )

        descarga.save_as(
            str(archivo_destino)
        )

        print(
            "✅ Excel guardado mediante "
            "evento DOWNLOAD."
        )

    # --------------------------------------------------------
    # RESPUESTA HTTP
    # --------------------------------------------------------

    elif respuestas_excel:

        response = (
            respuestas_excel[0]
        )

        print("")
        print(
            "Guardando Excel desde "
            "respuesta HTTP..."
        )

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

        reporte_page.screenshot(
            path=(
                "downloads/"
                "error_id31_descarga.png"
            ),
            full_page=True
        )

        raise RuntimeError(
            "AuraQuantic no generó "
            "una exportación Excel detectable "
            "para ID 3.1."
        )

    # --------------------------------------------------------
    # VALIDACIÓN
    # --------------------------------------------------------

    if not archivo_destino.exists():

        raise RuntimeError(
            "El archivo Excel ID 3.1 "
            "no fue generado."
        )

    tamano = (
        archivo_destino.stat().st_size
    )

    print("")
    print(
        "Tamaño del archivo:",
        tamano,
        "bytes"
    )

    if tamano <= 0:

        raise RuntimeError(
            "El Excel ID 3.1 generado "
            "está vacío."
        )

    print("")
    print(
        "✅ EXCEL ID 3.1 VALIDADO"
    )

    print(
        "Archivo:"
    )

    print(
        archivo_destino
    )

    return archivo_destino


# ============================================================
# ORQUESTADOR ID 3.1
# ============================================================


def ejecutar_reporte_id31(
    page,
    context
):

    print("")
    print("########################################")
    print("# ID 3.1 - REPORTE NOVEDADES CALIDAD")
    print("########################################")

    # 1. Abrir
    reporte_page = (
        abrir_reporte_novedades_calidad(
            page,
            context
        )
    )

    # 2. Fechas
    llenar_fechas_reporte(
        reporte_page
    )

    # 3. Proceder
    proceder_reporte(
        reporte_page
    )

    # 4. Exportar
    archivo_excel = (
        exportar_excel_con_formato(
            reporte_page
        )
    )

    print("")
    print("========================================")
    print("✅ ID 3.1 COMPLETADO")
    print("========================================")

    print("")
    print(
        "Excel generado:"
    )

    print(
        archivo_excel
    )

    return archivo_excel