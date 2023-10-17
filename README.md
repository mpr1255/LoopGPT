# LoopGPT

This is an absolutely barebones implementation of the idea: "I want chatgpt to loop over this input with the same prompt each time." 

Mainly done for learning purposes and a small work thing. Of course this entire readme and all the code was straight up gpt4 with some angry prompting. 

## Dependencies

- Flask
- OpenAI
- Markdown

## Setup

1. Clone this repository to your local machine.

   ```bash
   git clone <repository_url>
   ```

2. Navigate to the project directory.

   ```bash
   cd <project_directory>
   ```

3. Build the Docker image (assuming you have Docker installed).

   ```bash
   docker build -t flask-openai-app .
   ```

4. Run the Docker container.

   ```bash
   docker run -p 5001:5001 flask-openai-app
   ```

   This will start the application and make it accessible at `http://localhost:5001`.

## Usage

1. Open a web browser and navigate to `http://localhost:5001`.

2. You'll find fields for entering your OpenAI API key, the model to use, a prompt, and text that you want to process.

3. After filling in these fields, click on the 'Submit' button to process the text. The resulting text will be displayed on the page.

## Features

- **Chat Completion**: Uses OpenAI's API to perform chat completion based on the given model and prompt.
- **Markdown Rendering**: The output text is rendered as Markdown.

## Code Structure

- `Dockerfile`: Sets up the Docker image.
- `app.py`: Contains the Flask application logic.
- `index.html`: The HTML file that creates the frontend.

## License

This project is licensed under the MIT License.