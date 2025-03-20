import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from config.voice_config import VOICE_IDS, VOICE_SETTINGS

# Load environment variables
load_dotenv(dotenv_path="config/keys.env")

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)

def text_to_speech_file(text: str, bot_name: str = "DEFAULT") -> str:
    """
    Convert text to speech using ElevenLabs API.
    
    Args:
        text (str): The text to convert to speech
        bot_name (str): The name of the bot to use its voice settings (DEFAULT, WSB, BG3, etc.)
    
    Returns:
        str: Path to the saved audio file
    """
    # Ensure the audiobackup directory exists
    backup_dir = "data/audiobackup"
    os.makedirs(backup_dir, exist_ok=True)

    # Get voice ID and settings for the specified bot
    voice_id = VOICE_IDS.get(bot_name, VOICE_IDS["DEFAULT"])
    voice_settings = VOICE_SETTINGS.get(bot_name, VOICE_SETTINGS["DEFAULT"])

    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id=voice_id,
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",  # use the turbo model for low latency
        voice_settings=VoiceSettings(**voice_settings),
    )

    # Generating a unique file name for the output MP3 file
    save_file_path = os.path.join(backup_dir, f"{uuid.uuid4()}.mp3")

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path

#text_to_speech_file("hello I'm gerry the polar bear")