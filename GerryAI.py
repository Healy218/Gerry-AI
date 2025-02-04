import ollama
import os
print("Current working directory:", os.getcwd())

import os
if os.path.exists(".env"):
    print(".env file found!")
else:
    print(".env file not found. Please check its location.")


from twitchio.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="C:/Users/mrhea/OneDrive/Documents/Coding Projects/Gerry AI/keys.env")

TOKEN = os.getenv("TWITCH_OAUTH_TOKEN")
BOT_NICK = "Healy218AIChatBot"
CHANNEL = "Healy218"
OLLAMA_MODEL = "deepseek-r1:1.5b"  # Replace with your actual model name

# Debugging: Print the token (be careful not to share this online)
if TOKEN is None:
    print("Error: TWITCH_OAUTH_TOKEN is not being loaded from .env")
    exit()

print(f"Loaded Twitch OAuth Token: {TOKEN[:10]}... (hidden for security)")

class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(token=TOKEN, prefix="!", initial_channels=[CHANNEL])

    async def event_ready(self):
        print(f"Logged in as {self.nick}")

    async def event_message(self, message):
        if message.author is None or message.author.name.lower() == self.nick.lower():
            return  # Ignore messages from the bot itself
        
        print(f"Received message: {message.content}")  # Debugging line
        
        if message.content.startswith("!ask"):
            query = message.content[5:].strip()  # Remove '!ask ' and trim spaces
            if query:
                try:
                    response = ollama.chat(model=OLLAMA_MODEL, messages=[{"role": "user", "content": query}])
                    print(response)
                    # Access the content from the Message object
                    message_content = response.get("message", {}).get("content", "Sorry, I couldn't generate a response.")

                    # Remove <think> and </think> tags if they exist
                    message_content = message_content.replace("<think>", "").replace("</think>", "")

                    # Function to send multiple messages if content exceeds 500 characters
                    async def send_in_chunks(message_content, channel):
                        # Split the content into 500-character chunks
                        chunk_size = 499
                        for i in range(0, len(message_content), chunk_size):
                            chunk = message_content[i:i+chunk_size]
                            await channel.send(f"@{message.author.name}, {chunk}")

                    # Check if the message is too long and send in chunks
                    if len(message_content) > 499:
                        await send_in_chunks(message_content, message.channel)
                    else:
                        await message.channel.send(f"@{message.author.name}, {message_content}")


                except Exception as e:
                    print(f"Error with Ollama: {e}")
                    await message.channel.send("Error generating a response. Try again later.")

# Run the bot
bot = TwitchBot()
bot.run()
