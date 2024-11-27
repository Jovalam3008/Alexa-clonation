import pyttsx3 # Sirve para convertir texto a habla
import datetime  # Sirve para manipular fechas
import wikipedia  
import webbrowser # Navegar en internet
import speech_recognition as sr  # Conversion de habla a texto
import pywhatkit # Automatizar tareas
import tkinter as tk  # Interfaz grafica
from tkinter import scrolledtext
from tkinter import ttk

# Iniciar
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour<12:
        speak("Buenos días")
    elif 12 <= hour <18:
        speak("Buenas tardes")
    else:
        speak("Buenas noches")
    speak("En qué puedo ayudarte?")

def take_comand():
    recognizer = sr.Recognizer
    with sr.Microphone() as source:
        print("Escuchando...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Reconociendo")
        query = recognizer.recognize_google(audio, language='es-ES')
        print(f"Tú dijiste: {query}")
        return query
    except sr.UnknownValueError:
        print("No entendí lo que dijiste. Por favor,intenta de nuevo")
        return "None"
    except sr.RequestError as e:
        print(f"Error al conectarse al servicio de reconocimiento de voz {e}")
        return "None"

def search_wikipedia(query):
    speak("Buscando en wikipedia...")
    query = query.replace("wikipedia","")
    results = wikipedia.summary(query,sentences=2)
    speak("Según Wikipedia")
    speak(results)
    return results

def open_web(query):
    search_query = query.replace("Buscar","").strip()
    url= f"https://www.google.com/search?q={search_query}"
    webbrowser.open(url)
    speak(f"buscando{search_query} en Google")
    return f"Buscando {search_query} en Google"   

def search_youtube(query):
    search_query = query.replace("youtube","").strip()
    pywhatkit.playonyt(search_query)
    speak(f"Reproducioendo{search_query} en Youtube")
    return f"Reproduciendo{search_query} en Youtube"

def perform_calculation(query):
    try:
        #Eliminar cualquier palabra innecesaria
        query = query.replace("mas","+").replace("menos","-").replace("por","*").replace("dividido por","/")
        #Evaluar la expresión matematica
        result = eval(query)
        speak(f"El resultado es {result}")
        return result
    except Exception as e:
        speak("Lo siento, no pude realizar la operación")
        return "Error en la operación"

def handle_command(command):
    if "wikipedia" in command:
        return search_wikipedia(command)
    elif "hora" in command:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"La hora es{str_time}")
        return str_time
    elif "buscar" in command:
        return open_web(command)
    elif "youtube" in command:
        return search_youtube(command)
    elif "salir" in command:
        speak("Adios!")
        root.quit()
    elif any(op in command for op in ["mas","menos","por","dividido por","+","-","*","/"]):
        return perform_calculation(command)
    else:
        speak("No entendi el comando. Por favo,intentalo de nuevo")
        return "commando no reconocido"

# Interfaz
def on_button_click():
    command = take_comand().lower()
    if command and command != "none":
        result = handle_command(command)
        result_text.insert(tk.END,f"Tú: {command}/n: {result}/n")
        result_text.yview(tk.END) # desplazar hacia abajo el area de texto

# Crear la ventana principal
root = tk.Tk()
root.title("Assistant")
root.geometry("500*600")

# Estilo futurista
style = ttk.Style()
style.configure("TButton", font=('Helvetica',12), padding=10)
style.configure("Tlabel", font=("Helvatica",12), padding=10)
style.configure("TFrame", background='#1f1f1f') 
style.configure("TText", background='#1f1f1f',foreground='#00ff00')
style.configure("TScrolledText",background='#1f1f1f',foregrounf='#00ff00',font=('Helvetica',12))

# Configuar colores
root.configure(bg='#1f1f1f')

# Crear un marco para los componentes
frame = ttk.Frame(root, padding=20,style='TFrame')
frame.pack(expand=True, fill='both')

# Crear un boton para enviar el comando
send_button = ttk.Button(frame, text="hablar",command=on_button_click,style='TButton')
send_button.pack(pady=20)

# Creaer un area de texto para mostrar la conversacion
result_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=('Helvetica',12),bg='#1f1f1f',fg='#00ff00',heigh=20 ,width=60)
result_text.pack(pady=10)

# Saludo inicial
greet_user()

# Ejecutar la aplicacion
root.mainloop()