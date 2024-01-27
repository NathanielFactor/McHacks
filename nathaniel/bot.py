from openai import OpenAI

client = OpenAI()

def ai_response(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """Pick out keywords from the response that involve emotions."""
            },
            {
                "role": "user", #add the discord user as another function input
                "content": message #change this into the most optimal prompt for the ai
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
