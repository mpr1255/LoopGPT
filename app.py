#%%
from fastapi import FastAPI, WebSocket, Query, HTTPException, WebSocketDisconnect
from fastapi.responses import FileResponse, StreamingResponse, RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import openai
import logging
import tiktoken
import websockets
import os
import re
import markdown
from bs4 import BeautifulSoup
import requests
import re

app = FastAPI()
openai.api_key = "your_openai_api_key_here"  # Replace with your actual OpenAI API key

logging.basicConfig(filename='app.log', level=logging.DEBUG)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
root_logger.addHandler(stream_handler)

uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.setLevel(logging.DEBUG)

app.mount("/static", StaticFiles(directory="static"), name="static")
#%%
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def truncate_text(chunk, prompt, max_tokens=3800):
    encoding = tiktoken.get_encoding("cl100k_base")
    
    prompt_tokens = encoding.encode(prompt)
    prompt_token_count = len(prompt_tokens)
    
    adjusted_max_tokens = max_tokens - prompt_token_count
    
    tokens = encoding.encode(chunk)
    total_tokens = len(tokens)
    
    if total_tokens <= adjusted_max_tokens:
        print('returned unedited')
        return chunk  # Return the original text if it's short enough
    
    excess_tokens = total_tokens - adjusted_max_tokens
    truncate_each_side = excess_tokens // 2
    print('halving chunk')
    
    truncated_tokens = tokens[truncate_each_side:-truncate_each_side]
    truncated_text = encoding.decode(truncated_tokens)
    return truncated_text


# @app.get("/")
# def read_root():
#     return RedirectResponse(url='/static/index.html')

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r") as f:
        content = f.read()
    return content


def extract_urls(text):
    url_regex = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return url_regex.findall(text)

def fetch_url_content(urls):
    text_content = ""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content += soup.get_text(separator='\n', strip=True) + '\n'
        except requests.RequestException as e:
            text_content += f"Error fetching {url}: {str(e)}\n"
    return text_content


#%%

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            api_key = data['api_key']
            model = data['model']
            prompt = data['prompt']
            text = data['text']
            is_url = data.get('is_url', False)  # Assumes a new 'is_url' field from frontend

            openai.api_key = api_key  # Setting API key dynamically

            # Determine chunks based on is_url flag
            # is_url = True
            if is_url:
                urls = extract_urls(text)
                chunks = [{"url": url, "content": fetch_url_content([url])} for url in urls]
            else:
                chunks = [{"content": chunk.strip()} for chunk in re.split(r'\n[=]+\n', text) if chunk.strip()]

            for chunk in chunks:
                truncated_chunk = truncate_text(chunk["content"], prompt)  # Truncate if necessary
                full_prompt = f"{prompt}\n{chunk.get('url', '')}\n{truncated_chunk}"
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
                        logging.debug(message_chunk)
                        if 'choices' in message_chunk:
                            delta_content = message_chunk['choices'][0].get('delta', {}).get('content', '')
                            if delta_content:
                                logging.debug(delta_content)
                                await websocket.send_json({"output": delta_content})
                            else:
                                await websocket.send_json({"output": "\n\n"})
                except Exception as e:
                    await websocket.send_json({"output": f"Error in API call: {e}"})

    except WebSocketDisconnect as e:
        print(f"WebSocket disconnected with code: {e.code}")
    except Exception as e:
        print(f"An exception occurred: {e}")
        # Optionally log the full traceback
        import traceback
        print(traceback.format_exc())
