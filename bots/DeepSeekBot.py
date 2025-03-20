import ollama
import os
from twitchio.ext import commands
from dotenv import load_dotenv
from utilities.ElevenLabs import text_to_speech_file
from audioplayer import AudioPlayer
from utilities.obs_websockets import OBSWebsocketsManager
# Load environment variables
load_dotenv(dotenv_path="config/keys.env")

TOKEN = os.getenv("TWITCH_OAUTH_TOKEN")
BOT_NICK = "Healy218AIChatBot"
CHANNEL = "Healy218"
OLLAMA_MODEL = "deepseek-r1:1.5b"  # Replace with your actual model name
DEFAULT_VOICE = "Rachel"  # Set a default ElevenLabs voice

# Debugging: Ensure token is loaded
if not TOKEN:
    print("Error: TWITCH_OAUTH_TOKEN is not being loaded from .env")
    exit()

print(f"Loaded Twitch OAuth Token: {TOKEN[:10]}... (hidden for security)")

obswebsockets_manager = OBSWebsocketsManager()

class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(token=TOKEN, prefix="!", initial_channels=[CHANNEL])
        self.voice = DEFAULT_VOICE  # ✅ Define self.voice in __init__

    async def event_ready(self):
        print(f"Logged in as {self.nick}")

    async def event_message(self, message):
        if message.author is None or message.author.name.lower() == self.nick.lower():
            return  # Ignore messages from the bot itself

        print(f"Received message: {message.content}")  # Debugging line

        if message.content.startswith("!ask"):
            query = message.content[5:].strip()
            if query:
                try:
                    response = ollama.chat(model=OLLAMA_MODEL, messages=[{"role": "user", "content": query}])
                    message_content = response["message"]["content"]

                    # Remove <think> and </think> tags if they exist
                    message_content = message_content.replace("<think>", "").replace("</think>", "")

                    # Function to send multiple messages if content exceeds 500 characters
                    async def send_in_chunks(content, channel):
                        chunk_size = 499
                        for i in range(0, len(content), chunk_size):
                            chunk = content[i:i+chunk_size]
                            await channel.send(f"@{message.author.name}, {chunk}")

                    # Check if the message is too long and send in chunks
                    if len(message_content) > 499:
                        await send_in_chunks(message_content, message.channel)
                    else:
                        await message.channel.send(f"@{message.author.name}, {message_content}")

                    #✅ Generate TTS 
                    tts_file = text_to_speech_file(message_content, bot_name="DEEPSEEK")

                    #activate filter on image
                    obswebsockets_manager.set_filter_visibility("Desktop Audio", "Gerry", True)
                    
                    # ✅ Play audio response
                    print(message_content)
                    player = AudioPlayer(tts_file)
                    player.play(block=True)
                    
                    #audio_manager.play(tts_file)

                except Exception as e:
                    print(f"Error with Ollama: {e}")
                    await message.channel.send("Error generating a response. Try again later.")

                #turn off filter in obs
                obswebsockets_manager.set_filter_visibility("Desktop Audio", "Gerry", False)

bot = TwitchBot()
bot.run()
