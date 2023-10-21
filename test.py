from fastapi.testclient import TestClient
import json
from app import app  # Replace 'main' with the name of your FastAPI script

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "html" in response.headers["content-type"]

def test_websocket_endpoint():
    with client.websocket_connect("/ws") as websocket:
        data = {
            'api_key': 'your_openai_api_key_here',  # Replace with your actual OpenAI API key for testing
            'model': 'gpt-3.5-turbo',  # Replace with a model name for testing
            'prompt': 'Translate the following English text to French: ',
            'text': 'Hello, world!'
        }
        websocket.send_json(data)
        response = json.loads(websocket.receive_text())
        assert 'output' in response
        # Add more specific assertions based on what you expect to receive

if __name__ == "__main__":
    test_read_root()
    test_websocket_endpoint()
