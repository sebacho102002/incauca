import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class ChromeUtils:
    def login_manglar(self, driver, correo, contrasena):
        driver.get("https://gis.manglar.com/login#")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "inputEmail")))

        email_input = driver.find_element(By.NAME, "inputEmail")
        email_input.send_keys(correo)

        password_input = driver.find_element(By.NAME, "inputPassword")
        password_input.send_keys(contrasena)

        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()

        try:
            time.sleep(20)
            maps_button = driver.find_element(By.LINK_TEXT, "Maps")
            maps_button.click()
        except Exception:
            print("No se pudo encontrar el elemento 'a.nav-link.active[href='/maps']' dentro del tiempo de espera.")

    def buscar_codigos(self, driver, codigos):
        buscar_campo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-control.font-md.border-0"))
        )

        for codigo in codigos:
            driver.execute_script("arguments[0].value = '';", buscar_campo)
            time.sleep(1)

            if buscar_campo.get_attribute('value') == '':
                for caracter in codigo:
                    buscar_campo.send_keys(caracter)
                    time.sleep(1)
                time.sleep(3)
                buscar_campo.send_keys(Keys.ENTER)
                time.sleep(10)

                try:
                    replant_checkbox = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, ".//span[contains(text(), 'Replant (Plan)')]//ancestor::div[@class='d-flex'][1]//div[@class='d-flex ml-auto mr-1']/button[@class='btn btn-sm text-secondary']//i[@class='fas fa-chevron-right']"))
                    )
                    if not replant_checkbox.is_selected():
                        replant_checkbox.click()
                    print("Seleccionado el campo 'Replant (Plan)' para el código: " + codigo)
                except Exception as e:
                    print(f"No se pudo seleccionar el campo 'Replant (Plan)' para el código {codigo}: {e}")

                try:
                    boton_abrir_ventana = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "i.text-info.fas.fa-chart-pie"))
                    )
                    if not boton_abrir_ventana.is_selected():
                        boton_abrir_ventana.click()
                    print("Botón para abrir otra ventana clickeado.")
                except Exception as e:
                    print(f"No se pudo hacer clic en el botón para abrir otra ventana: {e}")
                buscar_campo.send_keys(Keys.DELETE)
                time.sleep(5)
                print("Se buscó el código: " + codigo)
            else:
                print("El campo de búsqueda no se limpió correctamente.")
