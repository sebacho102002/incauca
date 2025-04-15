import pyautogui
import time

# Espera para que abras WhatsApp y pongas el foco en el chat
time.sleep(5)

# Escribe el mensaje
pyautogui.write('Hola, esto es un mensaje automatizado 📩')
pyautogui.press('enter')
