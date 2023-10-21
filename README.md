# LoopGPT

This minimal implementation enables a continuous loop of interactions with ChatGPT over a given input, using the same prompt each time, further enriched to handle URLs.

Mainly crafted for learning and a minor work requirement, with some inspiration from GPT-4.

## Dependencies

- FastAPI
- OpenAI
- Markdown
- BeautifulSoup
- requests

## Setup

1. Clone this repository to your local machine:

   ```bash
   git clone <repository_url>
   ```

2. Navigate to the project directory:

   ```bash
   cd <project_directory>
   ```

3. Build the Docker image (ensure Docker is installed):

   ```bash
   docker build -t loopgpt .
   ```

4. Run the Docker container:

   ```bash
   docker run -d -p 8000:8000 loopgpt
   ```

   Now, the application is accessible at `http://localhost:8000`.

## Usage

1. Open a browser and navigate to `http://localhost:8000`.
2. Provide your OpenAI API key, choose the model, specify a prompt, and enter text or URLs.
3. Click 'Submit' to process. The output is displayed on the right.

## Features

- **Chat Completion**: Utilizes OpenAI's API for chat completion based on the specified model and prompt.
- **URL Content Fetching**: Extracts and processes text content from provided URLs.
- **Text Truncation**: Handles large text inputs by truncating them to fit model's token limits.
- **Markdown Rendering**: Outputs are rendered as Markdown.
- **Real-Time Interaction**: Utilizes WebSocket for real-time interaction with the model.

## Code Structure

- `Dockerfile`: Defines the Docker image setup.
- `app.py`: Holds the FastAPI application logic.
- `index.html`: Provides the frontend interface.

## License

This project is under the MIT License.