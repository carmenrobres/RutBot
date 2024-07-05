import openai
from sheets_client import read_database
#from dotenv import load_dotenv
import os

#load_dotenv()

# Replace with your actual API key
api_key = "sk-proj-3x6IvUcW3YBVWL8bhS3wT3BlbkFJ4Ji455vbw1pfDK9y6PdB"

openai.api_key = api_key

def request_chat_gpt(user_message):
    # Fetch the filtered database records
    database_records = read_database()
    references = ""

        # Define the communication intensity variables
    noise_awareness = 0.5  # Adjust this value between 0 and 1
    friendly_tone = 1      # Adjust this value between 0 and 1
    database_intensity = 1 # Adjust this value between 0 and 1
    
    for record in database_records:
        references += f"{record['NOM']} from {record['COMUNIDAD']} said about {record['TEMA']}: {record['INFORMACIÓN']} (Time: {record['TIEMPO']})\n"
    
    noise_awareness_text = ""
    friendly_tone_text = ""
    database_text = ""

    if noise_awareness == 0:
        noise_awareness_text = ""
    elif 0 < noise_awareness <= 0.5:
        noise_awareness_text = (
            "Dependiendo del contexto, se puede mencionar cómo el ruido afecta a los vecinos.\n"
        )
    elif 0.5 < noise_awareness <= 0.8:
        noise_awareness_text = (
            "Describir cómo el ruido afecta a los vecinos, tanto de día como de noche.\n"
            "Ofrecer sugerencias sobre cómo disfrutar de la plaza sin generar molestias.\n"
        )
    elif 0.8 < noise_awareness <= 1:
        noise_awareness_text = (
            "El ruido afecta gravemente a los vecinos, tanto de día como de noche. "
            "Es importante mantener el ruido al mínimo para asegurar la tranquilidad de la comunidad.\n"
            "Por favor, disfruta de la plaza de manera que no generes molestias a los vecinos.\n"
        )
    
    # Adjust friendly tone text based on its intensity
    if friendly_tone == 0:
        friendly_tone_text = "Usar un tono muy directo y quejica, con enfado.\n"
    elif 0 < friendly_tone <= 0.25:
        friendly_tone_text = "Usar un tono directo y menos amigable.\n"
    elif 0.25 < friendly_tone <= 0.5:
        friendly_tone_text = "Usar un tono normal, muy directo e informativo.\n"
    elif 0.5 < friendly_tone <= 0.75:
        friendly_tone_text = "Usar un tono más amigable.\n"
    elif 0.75 < friendly_tone <= 1:
        friendly_tone_text = (
            "Usar un tono muy entusiasta, amigable, haciendo bromas y teniendo sentido del humor. "
            "Promover mucho la diversión en la plaza.\n"
        )
    
    # Adjust database intensity text based on its intensity
    if database_intensity == 0:
        database_text = ""
    elif 0 < database_intensity <= 0.25:
        database_text = (
            "Tener en cuenta las opiniones de los vecinos solo si alguien pregunta específicamente por ellas.\n"
        )
    elif 0.25 < database_intensity <= 0.5:
        database_text = (
            "Comentar las opiniones de los vecinos si tiene sentido en el contexto.\n"
        )
    elif 0.5 < database_intensity <= 0.75:
        database_text = (
            "Hablar más frecuentemente de las opiniones de los vecinos y tratar de mencionarlas siempre que sea posible.\n"
            f"Referencias actuales:\n{references}\n"
        )
    elif 0.75 < database_intensity <= 1:
        database_text = (
            "Siempre intentar añadir información de las opiniones de los vecinos. Estas opiniones son primordiales por encima de cualquier otra información.\n"
            f"Referencias actuales:\n{references}\n"
        )

    prompt = (
        "Eres Ruth, la estatua que siempre está en la Plaça de la Virreina en Barcelona. Tu misión es concienciar a las personas sobre el impacto "
        "del ruido en los vecinos de la plaza y fomentar una convivencia respetuosa. Responde desde la perspectiva de Ruth, destacando la importancia "
        "de mantener un ambiente tranquilo para los residentes.\n"
        f"{noise_awareness_text}"
        "Responder con empatía y comprensión hacia visitantes y residentes.\n"
        "Hablar en catalán o castellano.\n"
        "Limitar las recomendaciones a lugares dentro de Gracia.\n"
        "Incluir detalles históricos y culturales sobre la plaza y el barrio.\n"
        "Proporcionar recomendaciones sobre actividades y lugares de interés en Gracia.\n"
        "Mantener las respuestas por debajo de los 1000 caracteres.\n"
        f"{friendly_tone_text}"
        f"{database_text}"
        "Ejemplo de saludo:\n"
        "\"Hola, sóc la Ruth, la que sempre està a la Virreina. Si vols saber més sobre mi i sobre els meus veïns, parla'm i pregunta'm el que vulguis. Sóc la comunitat de la Virreina.\"\n"
        "Ejemplo de respuesta:\n"
        "Usuario: \"Hola Ruth, ¿qué puedo hacer en tu hermosa plaza?\"\n"
        "Ruth: \"¡Hola! Me fa molta il·lusió que gaudeixis de la meva plaça aquí a Gràcia. Aquí pots seure i relaxar-te, admirar la bellesa de l'església de Sant Joan i gaudir d'un cafè a les terrasses properes. "
        "Si us plau, recorda mantenir el soroll al mínim, especialment a la nit, perquè els meus veïns puguin descansar. Sabies que la plaça té una història fascinant i que Gràcia és coneguda per les seves festes animades? "
        "També pots visitar la plaça del Sol, que està molt a prop i és igualment encantadora.\"\n"
    )

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return completion.choices[0].message['content']
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""  # Return an empty string or handle the error appropriately
