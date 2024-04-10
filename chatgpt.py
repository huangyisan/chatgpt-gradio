import openai
openai.api_key = 'anything'
openai.base_url = "https://chatgpt.iostat.io/v1/"
def send_ChatGPT(message):
    stream = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message,
        stream=True,
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content
