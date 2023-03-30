import os
import gradio as gr
import requests
import json

def send_ChatGPT(message):
    url = "https://{}/v1/chat/completions".format(os.getenv("OPENAI_DOMAIN"))

    payload = json.dumps({
    "model": "gpt-3.5-turbo-0301",
    "messages": [
        {
        "role": "user",
        "content": message
        }
    ],
    "temperature": 0.9,
    "max_tokens": 150
    })
    headers = {
    'Authorization': 'Bearer {}'.format(os.getenv("OPENAI_API_KEY")),
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.json()["choices"][0]["message"]["content"]


import gradio as gr
def setup_gradio_gui():
    with gr.Blocks() as gui:
        name = gr.Textbox(label="提问", lines=2, placeholder="在这里输入你要提问的内容",type="text")
        output = gr.Textbox(label="回答",type="text")
        greet_btn = gr.Button("提交")
        greet_btn.click(fn=send_ChatGPT, inputs=name, outputs=output)
    gui.launch()
setup_gradio_gui()