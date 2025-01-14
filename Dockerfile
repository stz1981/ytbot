# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install ffmpeg and other dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}

# Make the bash script executable
RUN chmod +x ./setup_and_run.sh
CMD ./setup_and_run.sh

# Run bot.py when the container launches
CMD ["python", "./bot.py"]
