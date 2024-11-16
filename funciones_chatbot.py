import speech_recognition as sr
from gtts import gTTS
import pygame, os

""" Variables globales """
sintomas_gripa = ['Fiebre', 'Dolor de cabeza', 'Dolor muscular', 'Cansancio', 'Secreción nasal', 'Dolor de garganta', 'Tos']
sintomas_resfriado = ['Secreción nasal', 'Dolor de garganta', 'Tos', 'Estornudo']
sintomas_alergia = ['Estornudo', 'Secreción nasal', 'Picazón en los ojos', 'Picazón en la piel', 'Congesión nasal']
numero_ordinal = ["primera", "segunda", "tercera", "cuarta", "quinta", "sexta", "septima"]

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
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Cargar y reproducir el archivo de audio
    pygame.mixer.music.load(archivo_audio)
    pygame.mixer.music.play()
    
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
        return False

    return texto
