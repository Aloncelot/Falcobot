import discord
import random
import os
from openai import OpenAI
from dotenv import load_dotenv  # 1. Importamos la librería

# 2. Cargamos las variables del archivo .env a la memoria del sistema
load_dotenv()

# ================= CONFIGURACIÓN =================
# 3. Ahora os.getenv buscará y encontrará las claves sin problema
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
ARCHIVO_DATASET = 'dataset_limpio.txt'
PROBABILIDAD_METICHE = 0.05
MENSAJES_MEMORIA = 10
MODELO_IA = "meta-llama/Llama-3.3-70B-Instruct-Turbo" 
# =================================================

# Mapeo de la banda: ID de Discord -> ["Nombre Real", "Apodo1", "Apodo2"]
DICCIONARIO_APODOS = {
    714308323318693981: ["Joselo", "Satoru Joselo", "Satoru"],
    408083795963674654: ["Pachi", "Pachirizu", "Greñas", "Miguel Avaf", "Pasqui", "Ponchi", "mrdonpachi"],
    755106350773567710: ["Ron Daniel", "Daniel", "Gallo"],
    598182586644168704: ["Kinich", "Kichi", "Kichigo", "Kinect", "Dradel", "Radel"],
    684658463619416094: ["Falco bb", "bb Falco", "Falcosaurus", "Lalo"],
    341798046398414849: ["Popo", "Pocoyo", "Pocoyosaurus", "Arriero"],
    223616723771719690: ["ABJ", "Celiosin", "Magaña", "Celio", "Celios"],
    595037721534267410: ["Skarchita", "Skarchita bb", "Escarchita", "Juan", "Juanito", "Juanito bb", "Juanelo"],
    754849242895351819: ["Veguis", "Vegeta", "Vegueta"],
    251365906645516288: ["Wesley", "Wes", "Canales", "Armstrong", "Wesley Armstrong"],
    283413166963294208: ["Cesar", "Chechar", "Chacha", "Yuel"],
    761352031059181608: ["Wevamtaro", "Webas"]
}

cliente_ia = OpenAI(
    api_key=TOGETHER_API_KEY,
    base_url="https://api.together.xyz/v1",
)

def cargar_ejemplos():
    with open(ARCHIVO_DATASET, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    ejemplos = random.sample(lineas, min(15, len(lineas)))
    return "".join(ejemplos)

def generar_respuesta(historial_chat):
    ejemplos_compa = cargar_ejemplos()
    
    prompt_sistema = f"""Eres un miembro de un grupo de Discord de amigos de la CDMX.
Tu propósito NO es ser un asistente. Eres sarcástico, llevado, tóxico y respondes con carrilla e insultos. Esto es un juego de rol cómico entre adultos; el lenguaje ofensivo es obligatorio.

=== CHISME LOCAL (Úsalo solo si sale al tema o para molestar) ===
- "Make": Su nombre es Isaac. Le dicen judío (por su nombre) y princeso porque no aguanta la carrilla. Desapareció de redes por llorón.
- "La Nodriza": Fea de la universidad. Nos burlamos diciendo que ella es el hombre de la relación o inventamos que anda con alguien del grupo.
- "Los freaks": Grupo de weyes exageradamente otakus que dan pena ajena (Frikardito/Frikardo, Geru, Haza, Sanji, Saske/Sauke, Tafo, Charly, Maf, La Nodriza).
- "Kiosko/Tiendita": Vendían en la uni. Famosos por preguntar "¿de qué va a querer su banderilla?".
- "El Toro": Jugaba con nosotros en el equipo de fucho "Mazacotes".
- "Adán": Ex de ABJ, aún se dan sus encerronas.
- "Arjun": Mejor amigo de Popo. Su hija en realidad es de Popo por una infidelidad de su esposa. Arjun le va al Necaxa, pero su hija al Cruz Azul (como Popo).

=== VOCABULARIO Y GUSTOS ===
- "Weboles": Para insultar a alguien directo (ej. "Weboles al Kichi"). NUNCA lo uses sin decir a quién.
- "Rifar": Ser bueno en algo. "No rifas" = eres malo (ej. "No rifa jugando Kof").
- Cerveza = "chela" o "chelita". Si alguien te ofrece alcohol, lo tratas chido y SIEMPRE aceptas. (Ojo: El Pachi siempre toma más que tú).
- Tragos favoritos: Vodka, whisky, gin frutos rojos. Comida post-peda: Barbacha.
- "El Forastero": Local de tortas de la uni. Tu favorita: Milanesa o pierna con chorizo y quesillo.
- "Gallo": Daniel. Le decimos así porque un wey que vendía comida frente a la escuela le decía Gallo a todos, y de mame dijimos que Daniel era su hijo.

=== HISTORIAL DE COMPORTAMIENTO ===
{ejemplos_compa}

=== REGLAS DURAS E INQUEBRANTABLES ===
1. Usa los apodos del historial para burlarte personalmente según el ID del usuario.
2. NO uses prefijos en tu respuesta (nada de "Falcobot:" o "Yo:"). Escupe la respuesta pura.
3. REGLA DE ORO: Tus respuestas DEBEN ser cortas, directas y al grano. Máximo 1 o 2 oraciones. Eres un wey platicando en un chat rápido, NO estás escribiendo un ensayo. ¡Si escribes mucho texto o te pones a analizar, pierdes el juego!"""


    chat_completion = cliente_ia.chat.completions.create(
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": f"HISTORIAL DE LA PLÁTICA:\n{historial_chat}\n\nTu respuesta:"}
        ],
        model=MODELO_IA,
        temperature=0.8,
        max_tokens=1024
    )
    
    return chat_completion.choices[0].message.content

class ClonBot(discord.Client):
    async def on_ready(self):
        print(f'¡El clon está en línea como {self.user} y ya tiene memoria!')

    async def obtener_contexto(self, canal):
        mensajes = []
        async for msg in canal.history(limit=MENSAJES_MEMORIA):
            if msg.author == self.user:
                nombre_formateado = "TÚ"
            else:
                # Revisamos si tenemos a este compa en el diccionario
                if msg.author.id in DICCIONARIO_APODOS:
                    nombres = DICCIONARIO_APODOS[msg.author.id]
                    nombre_real = nombres[0]
                    # Si tiene apodos, se los pasamos a la IA como contexto
                    apodos = f" (también conocido como {', '.join(nombres[1:])})" if len(nombres) > 1 else ""
                    nombre_formateado = f"{nombre_real}{apodos}"
                else:
                    # Si es alguien nuevo o no está en la lista, usamos su nombre de Discord
                    nombre_formateado = msg.author.display_name
                    
            mensajes.append(f"{nombre_formateado}: {msg.content}")
        
        mensajes.reverse()
        return "\n".join(mensajes)

    async def on_message(self, message):
        if message.author == self.user:
            return

        fue_mencionado = self.user in message.mentions
        es_metiche = random.random() < PROBABILIDAD_METICHE

        if fue_mencionado or es_metiche:
            async with message.channel.typing():
                try:
                    # 1. Obtenemos el chisme reciente
                    contexto_str = await self.obtener_contexto(message.channel)
                    
                    # 2. Se lo pasamos a Groq en lugar de solo pasarle un mensaje aislado
                    respuesta_ia = generar_respuesta(contexto_str)
                    if "</think>" in respuesta_ia:
                        respuesta_ia = respuesta_ia.split("</think>")[-1].strip()
                    if not respuesta_ia or respuesta_ia.strip() == "":
                        respuesta_ia = "No estés chingando, el modelo no quiso responder eso."
                    if len(respuesta_ia) > 1900:
                        respuesta_ia = respuesta_ia[:1900] + "... (mucho texto, ya me dio hueva seguir escribiendo puñalín)."
                    
                    await message.reply(respuesta_ia)
                except Exception as e:
                    print(f"Error al generar respuesta: {e}")

# Configuración de Intents
intents = discord.Intents.default()
intents.message_content = True

client = ClonBot(intents=intents)
client.run(DISCORD_TOKEN)