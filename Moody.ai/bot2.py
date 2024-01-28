import os
from openai import OpenAI

openai_api_key = "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"

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=openai_api_key)

def ai_response(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """Given a specific emotion, write a 5 word quote that inspires the user to keep pushing through their day."""
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature = 1,
        max_tokens = 100,
        top_p = 1,
        frequency_penalty = 1,
        presence_penalty = 1
    )
    response = response.choices[0].message.content
    return response
