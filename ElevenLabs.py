
import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv(dotenv_path="C:/Users/mrhea/OneDrive/Documents/Coding Projects/Gerry AI/keys.env")

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")


client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)

def text_to_speech_file(text: str) -> str:
    #ensure the audiobackup directory exists
    backup_dir = "audiobackup"
    os.makedirs(backup_dir, exist_ok=True)
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="viyyLJOwpZc4bofwHde1", # Gerry
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5", # use the turbo model for low latency
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.5,
            style=0.5,
            use_speaker_boost=True,
        ),
    )

    # uncomment the line below to play the audio back
    #play(response)

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