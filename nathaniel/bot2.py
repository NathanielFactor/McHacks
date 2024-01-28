import os
from openai import OpenAI

client = OpenAI()

def ai_response(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """Given a specific emotion, write a quote that inspires the user to keep pushing through their day."""
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature = 1,
        max_tokens = 500,
        top_p = 1,
        frequency_penalty = 1,
        presence_penalty = 1
    )
    response = response.choices[0].message.content
    return response
