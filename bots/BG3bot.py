import os
from twitchio.ext import commands
from collections import Counter
from dotenv import load_dotenv
from openai import OpenAI
from utilities.ElevenLabs import text_to_speech_file
from audioplayer import AudioPlayer
from utilities.obs_websockets import OBSWebsocketsManager

# Load environment variables
load_dotenv(dotenv_path="config/keys.env")

TOKEN = os.getenv("TWITCH_OAUTH_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOT_NICK = "Healy218AIChatBot"
CHANNEL = "Healy218"
DEFAULT_VOICE = "Rachel"  # Default ElevenLabs voice

if not TOKEN:
    print("Error: TWITCH_OAUTH_TOKEN is not being loaded from .env")
    exit()

print(f"Loaded Twitch OAuth Token: {TOKEN[:10]}... (hidden for security)")

# Initialize the modern OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize OBS websockets manager
obswebsockets_manager = OBSWebsocketsManager()

class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(token=TOKEN, prefix="!", initial_channels=[CHANNEL])
        self.voice = DEFAULT_VOICE
        self.messages = []  # For collecting non-command messages to summarize

    async def event_ready(self):
        print(f"Logged in as {self.nick}")

    async def event_message(self, message):
        if message.author is None or message.author.name.lower() == self.nick.lower():
            return  # Skip messages from the bot itself

        print(f"Received message: {message.content}")

        if message.content.startswith("!ask"):
            query = message.content[5:].strip()
            if query:
                await self.handle_query(query, message.channel, message.author.name)
        elif message.content.startswith("!bg3"):
            # Collect regular messages for summarization
            self.messages.append(message.content[5:].lower())
            if len(self.messages) >= 9:
                await self.handle_summarization(message.channel)

    async def handle_query(self, query, channel, author):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Make sure this model is available for you
                messages=[
                    {"role": "system", "content": "You are a bloodythirsty Orc woman relaying chat commands in 30 words or less."},
                    {"role": "user", "content": query}
                ],
                max_tokens=60
            )
            answer = response.choices[0].message.content.strip()
            await self.send_response_in_chunks(channel, author, answer)
            await self.generate_and_play_tts(answer)
        except Exception as e:
            print(f"Error with chat completions: {e}")
            await channel.send("Error generating response. Try again later.")

    async def handle_summarization(self, channel):
        # Count the three most common messages
        most_common = Counter(self.messages).most_common(3)
        common_phrases = [f'"{phrase}" ({count} times)' for phrase, count in most_common]
        prompt = (
            "Rank the messages from Twitch chat by frequency as a bloodthirsty Orc Woaman in 30 words or less:\n\n"
            + "\n".join(common_phrases)
        )
        try:
            response = response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a genz Orc woman relaying chat commands in 30 words or less."},
                {"role": "user", "content": "As a genZ Orc Woman, " + prompt}
            ],
            max_tokens=100
        )
            summary = response.choices[0].message.content.strip()
            await channel.send(f"Chat Summary: {summary}")
            await self.generate_and_play_tts(summary)
        except Exception as e:
            print(f"Error with summarization: {e}")
            await channel.send("Error generating summary. Try again later.")
        finally:
            self.messages.clear()  # Reset messages after processing

    async def generate_and_play_tts(self, text):
        try:
            # Generate TTS audio file using ElevenLabs
            tts_file = text_to_speech_file(text)
            # Activate OBS filter before playing audio
            obswebsockets_manager.set_source_visibility("BG3", "OrcLady2", True)
            obswebsockets_manager.set_filter_visibility("Desktop Audio", "OrcLady", True)
            # Play the generated audio
            player = AudioPlayer(tts_file)
            player.play(block=True)
        except Exception as e:
            print(f"Error in TTS generation or audio playback: {e}")
        finally:
            # Turn off the OBS filter
            obswebsockets_manager.set_filter_visibility("Desktop Audio", "OrcLady", False)
            obswebsockets_manager.set_source_visibility("BG3", "OrcLady2", False)

bot = TwitchBot()
bot.run()
