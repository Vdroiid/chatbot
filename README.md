# **Chatbot de Diagnóstico Médico por Voz**

Este proyecto es un **chatbot de diagnóstico médico** que utiliza tecnología de reconocimiento de voz para identificar síntomas en los usuarios. A partir de los síntomas mencionados por el usuario, el sistema proporciona una lista de posibles enfermedades que podrían coincidir con esos síntomas. El chatbot proporciona los resultados en voz alta.

## **Características**

- **Entrada de voz**: El chatbot recibe la información sobre los síntomas a través de comandos de voz.
- **Diagnóstico de enfermedades**: El chatbot evalúa los síntomas y, si coinciden con 4 o más síntomas predefinidos, proporciona un diagnóstico probable.
- **Salida en voz**: El chatbot devuelve el diagnóstico en voz alta para que el usuario pueda escucharlo.
- **Fácil de usar**: Solo se necesitan unos pocos comandos para obtener un diagnóstico médico inicial basado en los síntomas proporcionados.

## **Cómo funciona**

1. El usuario dicta sus síntomas usando el micrófono.
2. El chatbot analiza la lista de síntomas proporcionados y compara con una base de datos interna.
3. Si se encuentra una coincidencia con 4 o más síntomas, el chatbot informa al usuario de la enfermedad probable en voz alta.

Este sistema no debe considerarse un diagnóstico médico profesional, sino solo una herramienta básica para proporcionar información preliminar basada en síntomas comunes.

## **Instalación**

Para ejecutar el chatbot en tu máquina, necesitas instalar algunos paquetes de Python. Puedes hacerlo de forma global o usando un entorno virtual.

### **Requisitos**
- Paquetes necesarios (revisar requirements.txt)

### **Instrucciones de instalación**

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/Vdroiid/chatbot.git
   cd chatbot
