import os
from twitchio.ext import commands
import openai


# Define your bot class
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token='your_twitch_oauth_token', prefix='!', initial_channels=['Healy218'])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        print(f'Message from {message.author.name}: {message.content}')

        # Here you can add your AI response
        if message.content.lower().startswith("!ai"):
            response = generate_ai_response(message.content)  # You can define this function
            await message.channel.send(response)

# Run the bot
bot = Bot()
bot.run()

openai.api_key = 'your_openai_api_key'

def generate_ai_response(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=50
    )
    return response.choices[0].text.strip()