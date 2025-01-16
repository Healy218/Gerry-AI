import openai

openai.api_key = 'your_openai_api_key'

def generate_ai_response(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=50
    )
    return response.choices[0].text.strip()