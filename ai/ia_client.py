import os
from dotenv import load_dotenv
from openai import AzureOpenAI


# Cargar variables de entorno
load_dotenv()

# clase Enum para los tipos de respuesta
class ResponseType:
    TECHNICAL = "technical"
    CREATIVE = "creative"
    ANALYTICS = "analytics"
    DEFAULT = "default"

# Configuración de parámetros de OpenAI por defecto
v_max_tokens = 4096  # Máximo de tokens para la respuesta
v_temperature = 1.0  # Controla la aleatoriedad de las respuestas
v_top_p = 1.0  # Controla la diversidad de las respuestas
v_frecuency_penalty = 0.0  # Penaliza la repetición de palabras
v_presence_penalty = 0.0  # Penaliza la repetición de temas  

#Configuración de parámetros de IA para diferentes tipos de respuestas
def set_parameters_to_technical():
    global v_max_tokens, v_temperature, v_top_p, v_frecuency_penalty, v_presence_penalty
    """Configura los parámetros de IA para respuestas técnicas."""
    v_max_tokens = 4096
    v_temperature = 0.2
    v_top_p = 0.4
    v_frecuency_penalty = 0.0
    v_presence_penalty = 0.0

def set_parameters_to_creative():
    global v_max_tokens, v_temperature, v_top_p, v_frecuency_penalty, v_presence_penalty
    """Configura los parámetros de IA para respuestas creativas."""
    v_max_tokens = 4096
    v_temperature = 1.5
    v_top_p = 1.0
    v_frecuency_penalty = 0.0
    v_presence_penalty = 1.0

def set_parameters_to_analitycs():  
    global v_max_tokens, v_temperature, v_top_p, v_frecuency_penalty, v_presence_penalty
    """Configura los parámetros de IA para respuestas analíticas."""
    v_max_tokens = 4096
    v_temperature = 0.5
    v_top_p = 0.8
    v_frecuency_penalty = 0.5
    v_presence_penalty = 0.0
    
def set_parameters_to_default():    
    global v_max_tokens, v_temperature, v_top_p, v_frecuency_penalty, v_presence_penalty
    """Configura los parámetros de IA a los valores por defecto."""
    v_max_tokens = 4096
    v_temperature = 1.0
    v_top_p = 1.0
    v_frecuency_penalty = 0.0
    v_presence_penalty = 0.0      


def create_ai_client():
    """
    Crea un cliente de OpenAI configurado para Azure.
    """
    try:
        client = AzureOpenAI(
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
        return client
    except Exception as e:
        print(f"Error al crear el cliente de OpenAI: {e}")
        return None

def process_message_with_AI(message, context, response_type=ResponseType.DEFAULT, schema=None):
    client = create_ai_client()
    if not client:
        return "Error al crear el cliente de OpenAI."

    # Switch para seleccionar el método según response_type
    parameter_setters = {
        ResponseType.TECHNICAL: set_parameters_to_technical,
        ResponseType.CREATIVE: set_parameters_to_creative,
        ResponseType.ANALYTICS: set_parameters_to_analitycs,
        ResponseType.DEFAULT: set_parameters_to_default
    }
    parameter_setters.get(response_type, set_parameters_to_default)()

    try:
        if schema:
            # Usar el método parse si se pasa un schema
            response = client.beta.chat.completions.parse(
                model=os.getenv("AZURE_OPENAI_MODEL"),
                messages=context + [{"role": "user", "content": message}],
                response_format=schema,
                max_tokens=v_max_tokens,
                temperature=v_temperature,
                top_p=v_top_p,
                frequency_penalty=v_frecuency_penalty,
                presence_penalty=v_presence_penalty
            )
            return response.choices[0].message.content
        else:
            # Usar el método estándar si no hay schema
            response = client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_MODEL"),
                messages=context + [{"role": "user", "content": message}],
                max_tokens=v_max_tokens,
                temperature=v_temperature,
                top_p=v_top_p,
                frequency_penalty=v_frecuency_penalty,
                presence_penalty=v_presence_penalty
            )
            return response.choices[0].message.content
    except Exception as e:
        return f"Error al procesar el mensaje con IA: {e}"

