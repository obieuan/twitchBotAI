import twitchio
from twitchio.ext import commands
from twitchio.ext.commands import Context
from config import TWITCH_BOT_NAME, TWITCH_BOT_TOKEN, OPENAI_API_KEY, CHANNELS

import openai

# Configuración
bot_nick = TWITCH_BOT_NAME  # Nombre de tu bot en Twitch
channels = CHANNELS  # Lista de canales a los que te quieres conectar
openai.api_key = OPENAI_API_KEY  # Clave de API de OpenAI

# Clase del bot
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=TWITCH_BOT_TOKEN, prefix='!', initial_channels=[channel for channel in channels])
        self.chat_history = {}

    async def event_ready(self):
        for channel in channels:
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

        # Obtener el nombre del canal
        channel = message.channel.name

        # Verificar si el canal está en el historial del chat
        if channel not in self.chat_history:
            self.chat_history[channel] = []

        # Agregar el mensaje actual al historial del chat
        self.chat_history[channel].append(message.content)

        # Verificar si el mensaje contiene el prefijo "@obiai"
        if f'@{bot_nick.lower()}' in message.content.lower():
            # Eliminar el prefijo del mensaje para obtener el texto de entrada para ChatGPT
            input_text = message.content.lower().replace(f'@{bot_nick.lower()}', '').strip()

            # Obtener respuesta de ChatGPT
            response = self.get_chatgpt_response(channel, input_text)

            # Enviar la respuesta al chat
            await message.channel.send(f'@{message.author.name}, {response}')

    @commands.command()
    async def saludo(self, ctx):
        await ctx.send(f'Hola {ctx.author.name}!')

    def get_chatgpt_response(self, channel, message):
        # Obtener el historial del chat para el canal actual
        chat_history = self.chat_history[channel]

        # Combinar el historial del chat con el mensaje actual como contexto
        chat_context = '\n'.join(chat_history + [message])

        # Llamar a la API de ChatGPT con el contexto del chat
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=chat_context,
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

        # Agregar la respuesta al historial del chat
        chat_history.append(reply)

        # Limitar el historial del chat a un número máximo de mensajes
        max_history = 10
        if len(chat_history) > max_history:
            chat_history = chat_history[-max_history:]

        # Actualizar el historial del chat para el canal actual
        self.chat_history[channel] = chat_history

        return reply

# Crear instancia del bot
bot = Bot()

# Iniciar el bot
bot.run()
