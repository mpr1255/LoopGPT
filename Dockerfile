FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install git

# Install Python packages
RUN pip3 install openai markdown fastapi uvicorn websockets tiktoken

# Copy your code into the container
COPY . /app

# Set working directory
WORKDIR /app

# Run your application
CMD ["uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"]
