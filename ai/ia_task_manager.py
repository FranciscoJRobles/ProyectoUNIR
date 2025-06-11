from .ia_client import ResponseType, process_message_with_AI
from src.models.task import Task

def create_task_description(task_dict: dict) -> dict:
    """
    Recibe un diccionario tipo Task (con description vacía) y devuelve el mismo diccionario
    pero con la descripción generada por la IA. Solo 'title' es obligatorio.
    """
    if not task_dict.get("title"):
        raise ValueError("El campo 'title' es obligatorio para generar la descripción.")

    # Construimos el contexto para la IA
    context = [
        {"role": "system", "content": "Eres un asistente experto en gestión de proyectos de software. Tu objetivo es generar una descripción clara y útil para una tarea que se te va a entregar en formato json en varios campos. El campo prioritario de donde debes basarte para generar al tarea es title, el resto son opcionales y solo debes usarlos para ayudarte por si ofrecen información extra. En la respuesta limítate a devolver exclusivamente la descripción que deberá ir en el campo description, así que evita redundancia de información que ya esté descrita en los otros campos. No más de 150 palabras."},
    ]

    # Construimos el mensaje del usuario solo con los campos presentes
    user_message = f"Título: {task_dict['title']} "
    if task_dict.get("priority"):
        user_message += f"Prioridad: {task_dict['priority']} "
    if task_dict.get("effort_hours") is not None:
        user_message += f"Esfuerzo estimado: {task_dict['effort_hours']} horas "
    if task_dict.get("category"):
        user_message += f"Categoría: {task_dict['category']} "
    if task_dict.get("risk_analysis"):
        user_message += f"Análisis de riesgos: {task_dict['risk_analysis']} "
    if task_dict.get("risk_mitigation"):
        user_message += f"Mitigación de riesgos: {task_dict['risk_mitigation']} "
    user_message += "Por favor, genera una descripción detallada y profesional para esta tarea."

    # Llamada a la IA
    descripcion_generada = process_message_with_AI(
        message=user_message,
        context=context,
        response_type=ResponseType.CREATIVE  # O el tipo que desees, por ejemplo ResponseType.TECHNICAL
    )

    # Devolvemos el mismo dict pero con la descripción generada
    task_dict["description"] = descripcion_generada
    return task_dict

def create_task_category(task_dict: dict) -> dict:
    """
    Recibe un diccionario tipo Task (con category vacía o None) y devuelve el mismo diccionario
    pero con la categoría generada por la IA (debe ser un valor válido de CategoryEnum).
    """
    if not task_dict.get("title") and not task_dict.get("description"):
        raise ValueError("El campo 'title' y 'description' es obligatorio para categorizar la tarea.")

    # Contexto para la IA
    context = [
        {"role": "system", "content": "Eres un asistente experto en gestión de proyectos de software. Tu objetivo es analizar la información de una tarea y clasificarla en una de las siguientes categorías: Backend, Frontend, Testing, Documentación, Otro. La categoría Otro sólo si no coincide con ninguna de las otras. Devuelve únicamente el nombre de la categoría más adecuada para el campo category."}
    ]

    # Mensaje del usuario con los campos relevantes
    user_message = f"Título: {task_dict['title']}, Description: {task_dict['description']} "
    if task_dict.get("risk_analysis"):
        user_message += f"Análisis de riesgos: {task_dict['risk_analysis']} "
    if task_dict.get("risk_mitigation"):
        user_message += f"Mitigación de riesgos: {task_dict['risk_mitigation']} "
    user_message += "¿A qué categoría pertenece esta tarea?"

    # Llamada a la IA
    categoria_generada = process_message_with_AI(
        message=user_message,
        context=context,
        response_type=ResponseType.ANALYTICS  # O el tipo que desees, por ejemplo ResponseType.TECHNICAL
    )

    # Devolvemos el mismo dict pero con la categoría generada
    task_dict["category"] = categoria_generada.strip()
    return task_dict

def create_task_effort_estimate(task_dict: dict) -> dict:
    """
    Recibe un diccionario tipo Task (sin effort_hours) y devuelve el mismo diccionario
    pero con el esfuerzo estimado en horas generado por la IA (campo numérico).
    """
    if not task_dict.get("title"):
        raise ValueError("El campo 'title' es obligatorio para estimar el esfuerzo.")
    if not task_dict.get("description"):
        raise ValueError("El campo 'description' es obligatorio para estimar el esfuerzo.")
    if not task_dict.get("category"):
        raise ValueError("El campo 'category' es obligatorio para estimar el esfuerzo.")

    context = [
        {"role": "system", "content": "Eres un asistente experto en gestión de proyectos de software. Tu objetivo es estimar el esfuerzo en horas necesario (para una persona con perfil ingeniero informático) para completar una tarea, basándote en su título, descripción y categoría. Devuelve únicamente un número entero o decimal representando las horas estimadas, sin texto adicional."}
    ]

    user_message = (
        f"Título: {task_dict['title']}\n"
        f"Descripción: {task_dict['description']}\n"
        f"Categoría: {task_dict['category']}\n"
        "¿Cuántas horas estimas que llevará completar esta tarea?"
    )

    estimate_str = process_message_with_AI(
        message=user_message,
        context=context,
        response_type=ResponseType.ANALYTICS
    )

    # Intentar convertir la respuesta a float
    try:
        effort_hours = float(estimate_str.strip().replace(",", "."))
    except Exception:
        raise ValueError(f"No se pudo interpretar la estimación de esfuerzo: '{estimate_str}'")

    task_dict["effort_hours"] = effort_hours
    return task_dict

def create_task_audit(task_dict: dict) -> dict:
    """
    Recibe un diccionario tipo Task (sin risk_analysis ni risk_mitigation) y devuelve el mismo diccionario
    con ambos campos generados por la IA. Los campos obligatorios son: title, description, priority y category.
    """
    required_fields = ["title", "description", "priority", "category"]
    for field in required_fields:
        if not task_dict.get(field):
            raise ValueError(f"El campo '{field}' es obligatorio para auditar la tarea.")

    # --- PRIMERA PETICIÓN: Análisis de riesgos ---
    context_risk = [
        {"role": "system", "content": "Eres un experto en gestión de proyectos de software. Analiza los posibles riesgos de la siguiente tarea y devuelve solo el análisis de riesgos, sin texto adicional. No más de 100 palabras."}
    ]
    user_message_risk = (
        f"Título: {task_dict['title']}\n"
        f"Descripción: {task_dict['description']}\n"
        f"Prioridad: {task_dict['priority']}\n"
        f"Categoría: {task_dict['category']}\n"
        f"Responsable: {task_dict.get('assigned_to', '')}\n"
        "¿Qué riesgos pueden surgir en esta tarea?"
    )
    risk_analysis = process_message_with_AI(
        message=user_message_risk,
        context=context_risk,
        response_type=ResponseType.ANALYTICS
    )
    task_dict["risk_analysis"] = risk_analysis.strip()

    # --- SEGUNDA PETICIÓN: Plan de mitigación ---
    context_mitigation = [
        {"role": "system", "content": "Eres un experto en gestión de proyectos de software. A partir del análisis de riesgos y los datos de la tarea, genera un plan de mitigación de riesgos. Devuelve solo el plan, sin texto adicional. No más de 100 palabras"}
    ]
    user_message_mitigation = (
        f"Título: {task_dict['title']}\n"
        f"Descripción: {task_dict['description']}\n"
        f"Prioridad: {task_dict['priority']}\n"
        f"Categoría: {task_dict['category']}\n"
        f"Responsable: {task_dict.get('assigned_to', '')}\n"
        f"Análisis de riesgos: {task_dict['risk_analysis']}\n"
        "¿Qué plan de mitigación propones para estos riesgos?"
    )
    risk_mitigation = process_message_with_AI(
        message=user_message_mitigation,
        context=context_mitigation,
        response_type=ResponseType.ANALYTICS
    )
    task_dict["risk_mitigation"] = risk_mitigation.strip()

    return task_dict