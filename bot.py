from pyrogram.types import Message
from pyrogram import Client , filters 
from animeflv import AnimeFLV
from config import API_HASH, API_ID, BOT_TOKEN
import cloudscraper
import requests
import asyncio
import sys

api = AnimeFLV()
bot = Client("bot",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN)

@bot.on_message(filters.private)
async def start(client: Client, message: Message):
    async def worker(client: Client, message: Message):
        send = message.reply
        out_message = message.text
        user = message.from_user.username
        if user != 'FrancyJ2M':
        	return
        	
        if out_message.startswith('/eval'):
        	text=message.text
        	splitmsg = text.replace("/eval", "")
        	try:
        	 code = str(eval(splitmsg))
        	 await message.reply(code)
        	except:
        		code = str(sys.exc_info())
        		await message.reply(code)

        if out_message.startswith('/start'):
            await send('**Bienvenido**, use /search <nombre-del-anime> (como sale en la pagina)\n\n**Ejemplo:** `/search isekai-shoukan-wa-nidome-desu`')
            return
        
        if out_message.startswith('/search'):
            anime_t = out_message.split(' ')[1]
            anime = f"anime/{anime_t}"
            requests.get(f'https://www3.animeflv.net/ver/{anime_t}')
            msg = await send('**Obteniendo informacion !!!**')
            episodios = await get_numero_episodios(anime)
            
            if episodios:
                await msg.edit(f'**Informacion obtenida de {episodios} capitulos**')
                
                for index in range(1, episodios + 1):
                    await asyncio.sleep(1)
                    reint = 0
                    while reint < 10:
                        requests.get(f'https://www3.animeflv.net/ver/{anime_t}-{index}')
                        print(f'{anime_t}-{index}')
                        try:
                            links = api.downloadLinksByEpisodeID(f'{anime_t}-{index}')
                            if links:
                                reint = 0
                                msg_send = f"**Episodio {index}**\n\n"
                                for element in links:
                                    msg_send += f'**{element["server"]}**: {element["url"]}\n'
                                await send(msg_send,disable_web_page_preview=True)
                                break
                        except Exception as ex:
                            print(ex)
                            reint += 1
                            continue
                return
            await msg.edit('Ha ocurrido un error al obtener la informacion!!')
    
    bot.loop.create_task(worker(client, message))



async def get_numero_episodios(anime):
    for _ in range(10):  # Realizar un máximo de 10 intentos
        await asyncio.sleep(1)
        search = api.getAnimeInfo(anime)  # Obtener información
        episodios = len(search.get('episodes', []))  # Obtener el número de episodios  
        try:
            float(episodios)  # Comprobar si se encontró el número de episodios
            return episodios
        except ValueError:
            pass
    return False


#Run...
print("started")
bot.start()
bot.loop.run_forever()
