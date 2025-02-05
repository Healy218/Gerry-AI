import pyttsx3

engine = pyttsx3.init()

# Get a list of available voices
voices = engine.getProperty('voices')

# Print the voice names and their properties
for voice in voices:
    print(f"Voice: {voice.name}")
    print(f"ID: {voice.id}")
    #print(f"Language: {voice.languages[1].decode('utf-8')}")
    print(f"Gender: {voice.gender}")
    print("-" * 20)

# Set the voice by selecting a voice object from the list
engine.setProperty('voice', voices[0].id)

# Say something
engine.say("Hello, world!")
engine.runAndWait()