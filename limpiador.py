import json
import re

# ================= CONFIGURACIÓN =================
ARCHIVO_ENTRADA = 'dataset_compa.json'
ARCHIVO_SALIDA = 'dataset_limpio.txt'
# =================================================

def limpiar_dataset():
    print("Iniciando lavandería de mensajes...")
    
    with open(ARCHIVO_ENTRADA, 'r', encoding='utf-8') as f:
        mensajes_crudos = json.load(f)

    mensajes_limpios = []
    
    for msg in mensajes_crudos:
        texto = msg.get('texto', '')
        
        # 1. Eliminar URLs y links
        texto = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', texto)
        
        # 2. Eliminar menciones y etiquetas de Discord (ej. <@123456789>)
        texto = re.sub(r'<@!?\d+>', '', texto)
        
        # 3. Eliminar emojis custom de Discord (ej. <:pepe:12345>)
        texto = re.sub(r'<:\w+:\d+>', '', texto)
        
        # 4. Ignorar comandos de bots (empiezan con !, /, -, ?, o .)
        if texto.startswith(('!', '/', '-', '?', '.')):
            continue
            
        # Quitar espacios extra a los lados
        texto = texto.strip()
        
        # 5. Filtro de longitud: Ignorar mensajes vacíos o de menos de 4 letras 
        # (para quitar los "xd", "ah", "ok")
        if len(texto) > 4:
            mensajes_limpios.append(texto)

    # Guardamos el resultado en un archivo de texto plano
    # Es mucho más fácil pasarle un .txt a la IA que un JSON pesado
    with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as f:
        for linea in mensajes_limpios:
            f.write(linea + '\n')

    print(f"¡Limpieza terminada!")
    print(f"De {len(mensajes_crudos)} mensajes sucios, nos quedamos con {len(mensajes_limpios)} frases puras.")

if __name__ == '__main__':
    limpiar_dataset()