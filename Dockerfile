FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install git

# Copy your code into the container
COPY . /app

# Set working directory
WORKDIR /app

RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Run the test suite
RUN pytest test.py

# Run your application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
