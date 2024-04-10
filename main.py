import gradio as gr
import chatgpt
import time

css = """
.my-plus-button .plus-button { display: none; } 
.my-scroll-hide .scroll-hide { margin-left: 0px; }
"""

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

def add_message(history, message):
    for x in message["files"]:
        history.append(((x,), None))
    if message["text"] is not None:
        history.append((message["text"], None))
    return history, gr.MultimodalTextbox(value=None, interactive=False)

with gr.Blocks(css=css) as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
    )
    
    chat_input = gr.MultimodalTextbox(interactive=True, file_types=["text"], placeholder="请输入内容 ...", show_label=False, elem_classes=["my-plus-button", "my-scroll-hide"])

    clear = gr.Button("清空所有记录")

    def user(user_message, history):
        return "", history + [[user_message, None]]
    
    chat_msg = chat_input.submit(add_message, [chatbot, chat_input], [chatbot, chat_input])
    bot_msg = chat_msg.then(generate_response, chatbot, chatbot, api_name="bot_response")
    bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])

    clear.click(lambda: None, None, chatbot, queue=False)
    
demo.queue()
demo.launch()
