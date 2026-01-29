from httpcore import stream
from openai import OpenAI
from dotenv import load_dotenv
import os
from litellm import completion
import gradio as gr

ollama = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")



def messages(message, history, model):
    history = [{"role":h["role"],"content":h["content"]} for h in history]
    messages = [{"role":"system","content":"You are a helpful assistant."}] + history + [{"role":"user","content":message}]
    stream = completion(model=f"ollama/{model}",messages=messages,stream=True)
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''

        yield response
    
    return response    

with gr.Blocks() as demo:
    model = gr.Dropdown(choices=["llama2-uncensored","llama3.2","gemma2:9b","dolphin-phi"],value="llama2-uncensored",label="Choose a model to chat with")
    chatbot = gr.ChatInterface(fn=messages, additional_inputs=[model])

demo.launch(share=True)

