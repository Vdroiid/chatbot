import speech_recognition as sr
from gtts import gTTS
import pygame, os

# Para usar el reconocedor de voz sin internet (VOSK)
#import vosk
#import pyaudio
#import json
#import time

""" Variables globales """
sintomas_gripa = ['Fiebre', 'Dolor de cabeza', 'Dolor muscular', 'Cansancio', 'Secreción nasal', 'Dolor de garganta', 'Tos']
sintomas_resfriado = ['Secreción nasal', 'Dolor de garganta', 'Tos', 'Estornudo']
sintomas_alergia = ['Estornudo', 'Secreción nasal', 'Picazón en los ojos', 'Picazón en la piel', 'Congesión nasal']
numero_ordinal = ["primera", "segunda", "tercera", "cuarta", "quinta", "sexta", "septima"]

""" Leen en voz alta el texto que se le pase a la función. """
def leer_texto(texto):
    # Crear directorio para el archivo de audio si no existe
    audio_dir = "audio"
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    
    archivo_audio = os.path.join(audio_dir, "voz.mp3")
    
    # Generar archivo de audio
    tts = gTTS(text=texto, lang='es')
    tts.save(archivo_audio)
    
    # Inicializar pygame mixer
    pygame.mixer.init()
    
    # Limpiar pantalla (esto es específico para Windows, para otros sistemas usar 'clear')
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Cargar y reproducir el archivo de audio
    pygame.mixer.music.load(archivo_audio)
    pygame.mixer.music.play()
    
    # Mostrar texto
    print(texto)
    
    # Esperar hasta que el audio termine de reproducirse
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    # Finalizar pygame mixer
    pygame.mixer.quit()
    
    # Eliminar archivo de audio temporal
    if os.path.exists(archivo_audio):
        os.remove(archivo_audio)
    
    return texto

""" 
    Se diagnostica al paciente a base de las síntomas que se le pasa como primer parámetro:

    1. Lista de síntomas de Gripa
    2. Lista de síntomas de Resfriado
    3. Lista de síntomas de Alergia
"""
def validar_diagnostico(sintoma, s_g, s_r, s_a):
    os.system('cls')

    # Suma los valores de True y False de tal forma que da 1 a True y 0 a False
    cont_g = sum(i in sintoma for i in s_g)
    cont_r = sum(i in sintoma for i in s_r)
    cont_a = sum(i in sintoma for i in s_a)
    if cont_g >= 4:
        return "Usted presenta síntomas de Gripa."
    if cont_r >= 4:
        return "Usted presenta síntomas de Resfriado."
    if cont_a >= 4:
        return "Usted presenta síntomas de Alergia."
    else: 
        return "No hay sintomas suficientes para diagnosticar alguna enfermedad."

""" Recomendación """
def recomendar():
    return "Es importante consultar a un médico para obtener un diagnóstico preciso y un tratamiento adecuado."

"""
    Graba las síntomas que presenta el paciente. La función solo es para validar
    El primer parámetro es un contador que se usa en la petición (Necesita conexión a internet).
"""
def grabar_sintoma(contador):
    os.system('cls')
    peticion = f"Por favor, dime con voz alta la {numero_ordinal[contador]} síntoma que presenta. Puedes decir finalizar para realizar el diagnóstico."
    leer_texto(peticion)

    # Inicializa el reconocedor
    reconocedor = sr.Recognizer()

    # Usa el micrófono como fuente de entrada
    with sr.Microphone() as fuente:
        reconocedor.adjust_for_ambient_noise(fuente)  # Ajusta para el ruido ambiente
        audio = reconocedor.listen(fuente, timeout=5)  # Escucha el audio del micrófono

    # Reconoce el discurso en español
    try:
        texto = reconocedor.recognize_google(audio, language="es-ES")
        texto = texto.capitalize()
        print(texto)
    except sr.UnknownValueError:
        print("Google Speech Recognition no pudo entender el audio.")
        return False
    except sr.RequestError as e:
        print(f"No se pudieron solicitar resultados al servicio de Google Speech Recognition: {e}.")
        return False
    except:
        # Captura cualquier excepción no manejada
        print(f"Se ha producido un error inesperado de red")
        return False

    return texto
"""
    Graba las síntomas que presenta el paciente. La función solo es para validar
    El primer parámetro es un contador que se usa en la petición (No necesita conexión a internet).
"""

""" def escuchar_sintoma(contador):
    ruta_modelo = "chatbot/models/vosk-model-es-0.42"
    duracion_en_segundos = 6

    # Tamaño del fragmento de audio
    chunk_size = 4096 # Probar: 1024, 2048, 4000, 8192, etc.
    # Inicializar el modelo y el reconocedor
    model = vosk.Model(ruta_modelo)
    recognizer = vosk.KaldiRecognizer(model, 16000)

    # Configuración del micrófono
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,  # Formato de datos de audio (16 bits PCM)
        channels=1,              # Número de canales (1 para mono, 2 para estéreo)
        rate=16000,              # Frecuencia de muestreo (16000 Hz para audio de alta calidad)
        input=True,              # Configura el flujo para la entrada de audio
        frames_per_buffer=chunk_size  # Tamaño del fragmento de audio
    )

    # Variables para almacenar la transcripción, el tiempo de inicio y el último texto
    transcription = ""
    start_time = time.time()
    last_text = ""

    peticion = f"Por favor, dime con voz alta la {numero_ordinal[contador]} síntoma que presenta. Puedes decir finalizar para realizar el diagnóstico."
    #leer_texto(peticion)
    print("Escuchando...")

    try:
        while True:
            data = stream.read(chunk_size, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if 'text' in result:
                    new_text = result['text']

                    # Añadir solo si el nuevo texto es diferente al último texto agregado
                    if new_text != last_text:
                        transcription += new_text + ' '
                        last_text = new_text
            else:
                partial_result = json.loads(recognizer.PartialResult())
                if 'partial' in partial_result:
                    partial_text = partial_result['partial']

                    # Añadir solo si el texto parcial es diferente al último texto agregado
                    if partial_text != last_text:
                        transcription += partial_text + ' '
                        last_text = partial_text

            # Verifica si ha pasado el tiempo de grabación especificado
            if time.time() - start_time >= duracion_en_segundos:
                break

    finally:
        # Cerrar el flujo y liberar recursos
        stream.stop_stream()
        stream.close()
        p.terminate()

        print("Recording finished.")
        print(transcription)
    return transcription """