import os
import time

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright


load_dotenv()

AURA_URL = os.getenv("AURA_URL")
AURA_USUARIO = os.getenv("AURA_USUARIO")
AURA_PASSWORD = os.getenv("AURA_PASSWORD")


def login_aura():
    if not AURA_URL:
        raise ValueError("Falta AURA_URL en el archivo .env")

    if not AURA_USUARIO:
        raise ValueError("Falta AURA_USUARIO en el archivo .env")

    if not AURA_PASSWORD:
        raise ValueError("Falta AURA_PASSWORD en el archivo .env")

    # Importante:
    # mantenemos Playwright activo para poder seguir usando
    # browser, context y page después del login.
    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=True
    )

    context = browser.new_context()

    page = context.new_page()

    print("Abriendo AuraQuantic...")

    page.goto(
        AURA_URL,
        wait_until="domcontentloaded",
        timeout=120000
    )

    print("Esperando formulario de login...")

    page.wait_for_selector(
        "#ctrlDynamicLogin_Log_2558",
        timeout=60000
    )

    print("✅ Formulario de login detectado.")

    # Usuario
    page.locator(
        "#ctrlDynamicLogin_Log_2558"
    ).fill(AURA_USUARIO)

    print("Usuario ingresado.")

    # Contraseña
    page.locator(
        "#ctrlDynamicLogin_Pass_2558"
    ).fill(AURA_PASSWORD)

    print("Contraseña ingresada.")

    print("Ejecutando login...")

    page.get_by_role(
        "button",
        name="Iniciar sesión"
    ).click()

    print("Esperando validación de AuraQuantic...")

    # AuraQuantic es lento después del login
    time.sleep(10)

    try:
        page.wait_for_load_state(
            "networkidle",
            timeout=60000
        )
    except Exception:
        print(
            "AuraQuantic mantiene actividad de red; "
            "continuamos."
        )

    time.sleep(10)

    print("URL después del login:")
    print(page.url)

    print("Título:")
    print(page.title())

    # Captura posterior al login
    page.screenshot(
        path="downloads/aura_despues_login.png",
        full_page=True
    )

    # Validar que salimos del Login.aspx
    if "Login.aspx" in page.url:
        browser.close()
        playwright.stop()

        raise RuntimeError(
            "No fue posible iniciar sesión en AuraQuantic."
        )

    print("")
    print("✅ LOGIN AURAQUANTIC EXITOSO")
    print("✅ Navegador permanece abierto para continuar.")

    # NO cerramos browser aquí
    return playwright, browser, context, page


if __name__ == "__main__":
    playwright, browser, context, page = login_aura()

    print("")
    print("Prueba terminada.")
    print("El navegador sigue activo dentro del proceso.")

    input("Presiona ENTER para cerrar...")

    browser.close()
    playwright.stop()