from fastapi import FastAPI, WebSocket, Query, HTTPException
from fastapi.responses import FileResponse, StreamingResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import openai
import websockets
import os
import re
import markdown

app = FastAPI()
openai.api_key = "your_openai_api_key_here"  # Replace with your actual OpenAI API key


app.mount("/static", StaticFiles(directory="static"), name="static")

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
                full_prompt = f"{prompt}\n{chunk}"
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
                except Exception as e:
                    await websocket.send_json({"output": f"Error in API call: {e}"})
    except WebSocketDisconnect as e:
        print(f"WebSocket disconnected with code: {e.code}")
    except Exception as e:
        print(f"An exception occurred: {e}")