import gradio as gr
import chatgpt
import time

def generate_context_messages(messages: list):
    context_messages = [
        # system role
        {
            "role": "system",
            "content": "You are a helpful assistant."
        }
    ]
    for m in messages:
        # m[0]是用户发出, m[1]是chatgpt应答内容, 存储在gradio的chatbot里
        context_messages.append({
            'role': 'user',
            'content': m[0]
        })
        if m[1]:
            context_messages.append({
                'role': 'assistant',
                'content': m[1]
            })
    return context_messages

def generate_response(chat_history):
    messages = generate_context_messages(chat_history)
    bot_messages = chatgpt.send_ChatGPT(messages)
    # 最后一条内容的[1],也就是chatgpt的内容
    chat_history[-1][1] = ''
    for bm in bot_messages:
        chat_history[-1][1] += bm
        # 输出间隔.
        time.sleep(0.02)
        yield chat_history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def user(user_message, history):
        return "", history + [[user_message, None]]

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        generate_response, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)
    
demo.queue()
demo.launch()
