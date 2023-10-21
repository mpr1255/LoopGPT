print('test')
from fastapi import FastAPI, WebSocket, Query, HTTPException, WebSocketDisconnect
from fastapi.responses import FileResponse, StreamingResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import openai
import tiktoken
import websockets
import os
import re
import markdown

app = FastAPI()
openai.api_key = "your_openai_api_key_here"  # Replace with your actual OpenAI API key


app.mount("/static", StaticFiles(directory="static"), name="static")


def truncate_text(text, max_tokens=3500):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    total_tokens = len(tokens)
    if total_tokens <= max_tokens:
        return text  # Return the original text if it's short enough

    keep_each_side = max_tokens // 2
    truncated_tokens = tokens[:keep_each_side] + tokens[-keep_each_side:]
    truncated_text = encoding.decode(truncated_tokens)
    return truncated_text

@app.get("/")
def read_root():
    return RedirectResponse(url='/static/index.html')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # await websocket.send_json({"output": "Connection established!!"})
        while True:
            data = await websocket.receive_json()
            api_key = data['api_key']
            model = data['model']
            prompt = data['prompt']
            text = data['text']

            split_text_chunks = re.split(r'\n[=]+\n', text)
            split_text_chunks = [chunk.strip() for chunk in split_text_chunks if chunk.strip()]

            openai.api_key = api_key  # Setting API key dynamically

            for chunk in split_text_chunks:
                truncated_chunk = truncate_text(chunk)
                full_prompt = f"{prompt}\n{truncated_chunk}"
                try:
                    response = openai.ChatCompletion.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": full_prompt},
                        ],
                        stream=True
                    )
                    for message_chunk in response:
                        if 'choices' in message_chunk:
                            delta_content = message_chunk['choices'][0].get('delta', {}).get('content', '')
                            if delta_content:
                                # print(delta_content)
                                await websocket.send_json({"output": delta_content})
                            else:
                                await websocket.send_json({"output": "\n\n"})
                except Exception as e:
                    await websocket.send_json({"output": f"Error in API call: {e}"})
    except WebSocketDisconnect as e:
        print(f"WebSocket disconnected with code: {e.code}")
    except Exception as e:
        print(f"An exception occurred: {e}")