import speech_recognition as sr
import pyttsx3
import pvporcupine
import pyaudio
import struct
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

#configurar TTS

engine = pyttsx3.init()
engine.setProperty('rate', 150) #Velocidad del TTS
engine.setProperty('voice', 'es') #Voz español

def hablar(texto):
    engine.say(texto)
    engine.runAndWait() 

#configurar el reconocimiento de voz

def escuchar_comando(): 
    recognizer = sr.Recognizer()
    with sr.Microphone() as source: 
        print("Escuchando...")
        hablar ("Estoy escuchando...")
        try: 
            audio = recognizer.listen(source, timeout=5)
            comando = recognizer.recognize_google(audio, language="es-ES")
            print(f"comando Reconocido: {comando}")
            return comando.lower()
        except sr.UnknownValueError:
            hablar("Lo siento, no entiendo.")
            return ""
        except sr.RequestError: 
            hablar("Hubo un problema con la grabación.")
            return ""

#configurar el navegador

def iniciar_whatsapp():
    """Abre WhatsApp Web con Selenium."""
    ruta_chromedriver = r"C:\Users\Juank\OneDrive\Desktop\chromedriver-win64"  # Asegúrate de cambiar esta ruta
    service = Service(ChromeDriverManager().install())

    # Inicializa el WebDriver con el servicio
    driver = webdriver.Chrome(service=service)
    driver.get("https://web.whatsapp.com")
    print("Por favor, escanea el código QR en WhatsApp Web.")
    return driver

#buscar los mensajes

def buscar_contacto(driver, nombre_contacto):
    """Busca el nombre de un contacto en WhatsApp"""
    #buscar = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@title="Buscar"]')
    #buscar.click()
    #buscar.send_keys(nombre_contacto)
    #time.sleep(2)
    #buscar.send_keys(Keys.ENTER)
    #time.sleep(2)
    try:
        # Localiza la barra de búsqueda
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        search_box.clear()

        # Escribe el nombre del contacto
        search_box.send_keys(nombre_contacto)
        time.sleep(2)  # Espera para que cargue el resultado
        search_box.send_keys(Keys.ENTER)  # Abre el chat
        print(f"Abriendo chat con {nombre_contacto}...")
    except Exception as e:
        print(f"Error al buscar el contacto: {e}")

def leer_mensaje(driver):
    """Lee el mensaje del usuario"""
    mensajes = driver.find_elements(By.XPATH, '//div[contains(@class="_akbu")]//span[@dir="ltr"]')
    if mensajes:
        ultimo_mensaje= mensajes[-1].text
        hablar("El ultimo mensaje que recibió es: " + ultimo_mensaje)
    else: 
        hablar("No hay mensajes")

def reproducir_audio(driver):
    """Reproduce el audio del usuario"""
    try:
        audio = driver.find_elements(By.XPATH, '//button[@aria-label="Reproducir mensaje de voz"]') [-1]
        audio.click()
    except IndexError:
        hablar("No hay audios recientes en este chat")

# enviar mensaje

def enviar_mensaje(driver, mensaje):
    """Envía un mensaje al contacto abierto en WhatsApp Web."""
    try:
        # Espera a que la caja de mensaje esté disponible
        caja_mensaje = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true" and @data-tab="10"]'))
        )
        caja_mensaje.click()
        caja_mensaje.send_keys(mensaje)  # Escribe el mensaje
        time.sleep(1)
        caja_mensaje.send_keys(Keys.ENTER)  # Envía el mensaje
        print("Mensaje enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")
#Ejecución del programa 

if __name__ == "__main__":
    driver = iniciar_whatsapp()
    while True: 
        comando = escuchar_comando()
        if "leer mensaje de" in comando:
            nombre_contacto = comando.replace("leer mensaje de", "").strip()
            buscar_contacto(driver, nombre_contacto)
            leer_mensaje(driver)
        elif "reproducir audio de" in comando:
            nombre_contacto = comando.replace("reproducir audio de", "").strip()
            buscar_contacto(driver, nombre_contacto)
            reproducir_audio(driver)
        elif "enviar mensaje" in comando:
            nombre_contacto = comando.replace("enviar mensaje a", "").strip()
            buscar_contacto(driver, nombre_contacto)
            hablar("que mensaje quieres enviar?")
            mensaje = escuchar_comando()
            enviar_mensaje(driver, mensaje)
        elif "buscar contacto" in comando:
            nombre_contacto = comando.replace("buscar contacto", "").strip()
            if nombre_contacto: 
                buscar_contacto(driver, nombre_contacto)
            else: 
                hablar("no has escrito el nombre del contacto")
        elif "Hola cómo estás" in comando: 
            hablar("Soy un robot que te puedes ayudar con tus necesidades")
        elif "cállate marcelo" in comando: 
            hablar("apagando el robot, hasta luego")
            driver.quit()
            break
