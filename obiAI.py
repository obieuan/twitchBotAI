import twitchio
from twitchio.ext import commands
from twitchio.ext.commands import Context
from config import TWITCH_CLIENT_ID, TWITCH_BOT_NAME, TWITCH_BOT_TOKEN, OPENAI_API_KEY


import openai

# Configuración
bot_nick = TWITCH_BOT_NAME  # Nombre de tu bot en Twitch
channel = TWITCH_CLIENT_ID  # Nombre del canal al que te quieres conectar
#channels = ['channel1', 'channel2', 'channel3']  # Lista de canales a los que te quieres conectar
openai.api_key = OPENAI_API_KEY  # Clave de API de OpenAI

# Clase del bot
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=TWITCH_BOT_TOKEN, prefix='!', initial_channels=[channel])

    async def event_ready(self):
        print(f'Conectado a {channel}')        

        # Enviar mensaje de bienvenida al canal
        channel_obj = self.get_channel(channel)  # Obtener objeto Channel del canal
        if channel_obj:
            await channel_obj.send("Hola soy una IA")
        else:
            print(f"No se pudo obtener el objeto Channel para el canal {channel}")

    async def event_message(self, message):
        # Ignorar mensajes propios
        if message.author and message.author.name.lower() == bot_nick.lower():
            return

        # Verificar si el mensaje contiene el prefijo "@obiai"
        if f'@{bot_nick.lower()}' in message.content.lower():
            # Eliminar el prefijo del mensaje para obtener el texto de entrada para ChatGPT
            input_text = message.content.lower().replace(f'@{bot_nick.lower()}', '').strip()

            # Obtener respuesta de ChatGPT
            response = self.get_chatgpt_response(input_text)

            # Enviar la respuesta al chat
            await message.channel.send(f'@{message.author.name}, {response}')

    @commands.command()
    async def saludo(self, ctx):
        await ctx.send(f'Hola {ctx.author.name}!')

    def get_chatgpt_response(self, message):
        # Llamar a la API de ChatGPT
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=message,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        # Obtener la respuesta generada por ChatGPT
        reply = response.choices[0].text.strip()

        return reply

# Crear instancia del bot
bot = Bot()

# Iniciar el bot
bot.run()