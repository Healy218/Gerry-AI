import os
from twitchio.ext import commands
from collections import Counter
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv(dotenv_path="C:/Users/mrhea/OneDrive/Documents/Coding Projects/Gerry AI/keys.env")

TOKEN = os.getenv("TWITCH_OAUTH_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOT_NICK = "Healy218AIChatBot"
CHANNEL = "Healy218"

openai.api_key= "OPENAI_API_KEY"

models = openai.Model.list()

print(models)