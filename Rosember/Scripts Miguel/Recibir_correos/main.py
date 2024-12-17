import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from tkinter import messagebox
from email_utils import EmailsUtil
from chrome_utils import ChromeUtils
import config

class Main:
    def __init__(self):
        self.driver = None

    def setup_driver(self):
        service = Service(config.Config.webdriver_path)
        self.driver = webdriver.Chrome(service=service)

    def run(self):
        self.setup_driver()

        emails_util = EmailsUtil()
        codigos = emails_util.codsia_outlook()

        if codigos:
            messagebox.showinfo("Códigos Encontrados", f'Codigos extraídos: {codigos}')
        else:
            messagebox.showinfo("Sin Códigos", 'No se encontraron códigos en los correos no leídos de Manglar.')
            self.driver.quit()

        chrome_utils = ChromeUtils()
        chrome_utils.login_manglar(self.driver, config.Config.Correo_m, config.Config.Contra_m)
        chrome_utils.buscar_codigos(self.driver, codigos)
        
        messagebox.showinfo("Códigos Encontrados", "LLL")

        
if __name__ == "__main__":
    app = Main()
    app.run()
