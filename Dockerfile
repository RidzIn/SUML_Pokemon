# Dockerfile

# Base image for Python
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for the application
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk \
    libx11-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run the application
CMD ["python", "app.py"]
