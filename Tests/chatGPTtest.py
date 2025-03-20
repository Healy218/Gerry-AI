import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="C:/Users/mrhea/OneDrive/Documents/Coding Projects/Gerry AI/keys.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY is missing!")
    exit()

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def chat_with_gpt(query):
    try:
        print(f"Sending query: {query}")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a dungeon master in a fantasy world. You relay commands and describe the world vividly."},
                {"role": "user", "content": "As a dungeon master, " + query}
            ],
            max_tokens=100
        )
        
        if not response or not response.choices:
            print("Error: Empty response from OpenAI API.")
            return "No response received."
        
        answer = response.choices[0].message.content.strip()
        print("AI Response:", answer)
        return answer
    except Exception as e:
        print(f"Error during OpenAI request: {e}")
        return "Error generating response. Try again later."

if __name__ == "__main__":
    while True:
        user_input = input("Enter your message (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        response = chat_with_gpt(user_input)
        print("ChatGPT:", response)
