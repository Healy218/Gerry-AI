import os
import random
import anthropic
from twitchio.ext import commands

# Set up your Anthropic API key (for Claude responses)
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', 'your_anthropic_api_key_here')

# Initialize the Anthropic client
claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Twitch credentials
TMI_TOKEN = os.environ.get('TMI_TOKEN', 'your_oauth_token_here')
CLIENT_ID = os.environ.get('CLIENT_ID', 'your_client_id_here')
BOT_NICK = os.environ.get('BOT_NICK', 'your_bot_nickname_here')
BOT_PREFIX = os.environ.get('BOT_PREFIX', '!')
CHANNEL = os.environ.get('CHANNEL', 'your_channel_name_here')

# Initialize the bot
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TMI_TOKEN,
            client_id=CLIENT_ID,
            nick=BOT_NICK,
            prefix=BOT_PREFIX,
            initial_channels=[CHANNEL]
        )
        
        # Store recent messages to provide context for AI responses
        self.recent_messages = []
        self.max_context_messages = 10
        
    async def event_ready(self):
        """Called once when the bot goes online."""
        print(f"{BOT_NICK} is online!")
        await self._ws.send_privmsg(CHANNEL, f"/me has landed!")

    async def event_message(self, message):
        """Runs every time a message is sent in chat."""
        # Make sure the bot ignores itself and the streamer
        if message.echo:
            return

        # Store the message for context
        self.recent_messages.append(f"{message.author.name}: {message.content}")
        if len(self.recent_messages) > self.max_context_messages:
            self.recent_messages.pop(0)
            
        # Print the message content to console
        print(f"{message.author.name}: {message.content}")
        
        # Handle commands
        await self.handle_commands(message)
        
        # Randomly respond to messages (5% chance)
        if random.random() < 0.05:
            await self.generate_response(message)
        
        # Check for direct mentions of the bot
        if BOT_NICK.lower() in message.content.lower():
            await self.generate_response(message)

    async def generate_response(self, message):
        """Generate a Claude response to the chat message."""
        try:
            # Create a prompt with recent context
            context = "\n".join(self.recent_messages[-5:])
            
            # Send request to Claude using Anthropic's API
            response = claude_client.messages.create(
                model="claude-3-7-sonnet-20250219",  # Use the latest Claude model
                max_tokens=100,
                temperature=0.7,
                system="You are a friendly Twitch bot assistant. Keep your responses brief, casual, and entertaining (maximum 150 characters). Add occasional emotes or emojis for personality.",
                messages=[
                    {
                        "role": "user", 
                        "content": f"Recent chat context:\n{context}\n\nThe latest message was from {message.author.name}: \"{message.content}\"\n\nWrite a brief, friendly response to this message or conversation."
                    }
                ]
            )
            
            # Send the response to chat
            bot_response = response.content[0].text
            # Ensure the response isn't too long for Twitch
            if len(bot_response) > 500:
                bot_response = bot_response[:497] + "..."
                
            await message.channel.send(bot_response)
            
        except Exception as e:
            print(f"Error generating response: {e}")
            # Fallback responses if API fails
            fallbacks = [
                f"Hey @{message.author.name}! 👋",
                "That's interesting!",
                "Tell me more about that!",
                "Cool cool cool 😎",
                "I'm just a bot, but that sounds neat!"
            ]
            await message.channel.send(random.choice(fallbacks))
            
    @commands.command(name="ping")
    async def ping_command(self, ctx):
        """Responds with pong to check if bot is alive."""
        await ctx.send(f"Pong! @{ctx.author.name}")
        
    @commands.command(name="dice")
    async def dice_command(self, ctx):
        """Rolls a dice."""
        dice_result = random.randint(1, 6)
        await ctx.send(f"@{ctx.author.name} rolled a {dice_result}! 🎲")
        
    @commands.command(name="ask")
    async def ask_command(self, ctx):
        """Ask Claude a specific question."""
        # Extract the question (everything after !ask)
        question = ctx.message.content[len(f"{BOT_PREFIX}ask"):].strip()
        
        if not question:
            await ctx.send(f"@{ctx.author.name}, please include a question after !ask")
            return
            
        try:
            # Send direct question to Claude
            response = claude_client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=150,
                temperature=0.7,
                system="You are assisting in a Twitch chat. Keep responses concise, informative, and friendly. Maximum 2-3 short sentences.",
                messages=[{"role": "user", "content": question}]
            )
            
            # Send response to chat
            bot_response = response.content[0].text
            # Ensure the response isn't too long for Twitch
            if len(bot_response) > 500:
                bot_response = bot_response[:497] + "..."
                
            await ctx.send(f"@{ctx.author.name}: {bot_response}")
            
        except Exception as e:
            print(f"Error in ask command: {e}")
            await ctx.send(f"@{ctx.author.name}, I couldn't process that question right now.")

# Run the bot
bot = Bot()
bot.run()