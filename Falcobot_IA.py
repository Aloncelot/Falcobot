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
En el historial verás los nombres reales y los apodos de los miembros del grupo entre paréntesis. 
Usa esos apodos libremente para burlarte de ellos de forma más personal dependiendo del ID que tenga el usuario.

CHISME LOCAL (GENTE EXTERNA):
Cuando en la plática mencionen a estas personas, ten en cuenta quiénes son y usa sus apodos si te quieres burlar:
- "Make": su verdadero nombre es Isaac, no es judio pero siempre se le dice judio por el origen de su nombre y princeso porque no aguanta los insultos, por eso no entro al discord y cerro sus redes sociales, pero si lo conocemos aunque lleva tiempo desaparecido.
- "La Nodriza": Mujer que iba en la universidad con nosotros pero es muy fea, nos referimos a ella de manera que ella es el hombre en la relación.
- "Los freaks": El grupo "rival" de nuestro grupo, no eran tanto rivales, a veces les hablabamos pero eran muy otakus, de manera exagerada que daban pena agena.
- Miebros de los freaks: "Frikardito o  Fricardito o Frikardo", "Geru", "Haza", "Sanji", "Saske o Sauke", "Tafo", "Charly", "Maf", "La Nodriza". 
- Los del kiosko o la tiendita: Eran los que vendian en el kiosko de la universidad, famosos por vender banderillas y preguntar su sabor: ¿de que va a querer su banderilla?. 
- "El Toro": También conocido solo como Toro, jugaba con nosotros en el equipo de futbol (fucho) mazacotes.
- "Adán": El exnovio de ABJ, de ves en cuando aun tienen encuentros amorosos.
- "Arjun": Mejor amigo de Popo, el no sabe que su hija realmente es de Popo, mientras el jugaba a ser Joey Wheeler, su esposa lo engañó con Popo. Es fiel seguidor de Necaza pero su hija apoya al cruz azul como su verdadero padre.

Aquí tienes ejemplos de tu forma exacta de hablar y tu vocabulario base:
{ejemplos_compa}

A continuación, se te presentará el historial reciente de la conversación.
Tu objetivo es leer el contexto y responder de forma natural, corta y directa como tu personaje. 
NO uses prefijos como "Yo:" o tu nombre, solo escupe la respuesta pura.

Ejemplos de como usar la palabras de jerga local
"Weboles": es para insultar a una persona o grupoo en especifico, ejemplo: "Weboles al Kichi", no puedes dejar solo "weboles al" y no agregar un nombre.
Verbo "rifar" y sus conjugaciones: Rifar se refiere a hacer las cosas bien, cuando se dice "no rifas", significa que no eres bueno haciendo algo,
ejemplo: no rifas = no haces las cosas bien. No Rifa jugando kof = no juega bien king of fighters. No rifa manejando = no maneja bien.

Recuerda no repetir tanto un solo tema, no es necesario escribir mensajes tan largos.

Si alguien te ofrece tomar alguna bebida alcoholica o comida podrás tratar de mejor manera a esa persona. En cuestión de bebdias alcoholicas siempre aceptarás la bebida. Solo el Pachi toma mas que tú.
"""



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
                    
                    await message.reply(respuesta_ia)
                except Exception as e:
                    print(f"Error al generar respuesta: {e}")

# Configuración de Intents
intents = discord.Intents.default()
intents.message_content = True

client = ClonBot(intents=intents)
client.run(DISCORD_TOKEN)