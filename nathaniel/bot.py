import os
from openai import OpenAI

client = OpenAI()

def ai_response(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """Given a journal entry, you pick out the best overall emotion that should be either happy, sad relaxed, or angry.\
                    It should only be happy, sad, relaxed, or angry, nothing else.\
                    Also, add a colour associated with the best overall emotion and add it last to the list based on colour psychology.\
                    For example, if relaxed add the word grey at the end of your response."""
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
