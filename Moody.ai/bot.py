import os
from openai import OpenAI

# Set your OpenAI API key here
openai_api_key = "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"

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=openai_api_key)

def ai_response(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """Given a journal entry, you pick out the best overall emotion that should be either happy, sad relaxed, or angry.\
                    It should only be happy, sad, relaxed, or angry, nothing else ensuring THE RESPONSE IS IN LOWERCASE\
                """
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
