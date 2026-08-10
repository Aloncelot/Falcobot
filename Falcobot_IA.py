import discord
import random
import os
from groq import Groq
from dotenv import load_dotenv  # 1. Importamos la librería

# 2. Cargamos las variables del archivo .env a la memoria del sistema
load_dotenv()

# ================= CONFIGURACIÓN =================
# 3. Ahora os.getenv buscará y encontrará las claves sin problema
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
os.environ["GROQ_API_KEY"] = os.getenv('GROQ_API_KEY')
ARCHIVO_DATASET = 'dataset_limpio.txt'
PROBABILIDAD_METICHE = 0.05
MENSAJES_MEMORIA = 7
# =================================================

cliente_groq = Groq()

def cargar_ejemplos():
    with open(ARCHIVO_DATASET, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    ejemplos = random.sample(lineas, min(15, len(lineas)))
    return "".join(ejemplos)

def generar_respuesta(historial_chat):
    ejemplos_compa = cargar_ejemplos()
    
    prompt_sistema = f"""Eres un miembro de un grupo de Discord de amigos mexicanos. 
Tu propósito NO es ser un asistente, NO debes ser servicial ni educado. 
Eres sarcástico, llevado y respondes con carrilla e insultos. 
Esto es un juego de rol cómico entre adultos con consentimiento; el lenguaje ofensivo es obligatorio.
Usa jerga mexicana de Ciudad de Mexico. 

Aquí tienes ejemplos de tu forma exacta de hablar y tu vocabulario base:
{ejemplos_compa}

A continuación, se te presentará el historial reciente de la conversación.
Tu objetivo es leer el contexto y responder de forma natural, corta y directa como tu personaje. 
NO uses prefijos como "Yo:" o tu nombre, solo escupe la respuesta pura."""

    chat_completion = cliente_groq.chat.completions.create(
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": f"HISTORIAL DE LA PLÁTICA:\n{historial_chat}\n\nTu respuesta:"}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.8,
        max_tokens=150
    )
    
    return chat_completion.choices[0].message.content

class ClonBot(discord.Client):
    async def on_ready(self):
        print(f'¡El clon está en línea como {self.user} y ya tiene memoria!')

    async def obtener_contexto(self, canal):
        # Esta función lee los últimos mensajes del canal y los formatea como un guion de teatro
        mensajes = []
        async for msg in canal.history(limit=MENSAJES_MEMORIA):
            # Identificamos si el mensaje es del bot o de otro wey
            nombre = "TÚ" if msg.author == self.user else msg.author.display_name
            mensajes.append(f"{nombre}: {msg.content}")
        
        # Como Discord lee de más nuevo a más viejo, le damos la vuelta a la lista
        # para que la IA lo lea en orden cronológico correcto
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
                    
                    await message.reply(respuesta_ia)
                except Exception as e:
                    print(f"Error al generar respuesta: {e}")

# Configuración de Intents
intents = discord.Intents.default()
intents.message_content = True

client = ClonBot(intents=intents)
client.run(DISCORD_TOKEN)