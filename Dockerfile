# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Create a non-root user
RUN useradd -ms /bin/bash ytbotuser

# Change to the non-root user
USER ytbotuser

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Copy the .env file into the container
COPY .env .env

# Set environment variables (for non-sensitive data)
ENV TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}

# Add local bin to PATH
ENV PATH="/home/ytbotuser/.local/bin:${PATH}"

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip --root-user-action=ignore
RUN pip install --no-cache-dir -r requirements.txt  --root-user-action=ignore

# Change to the non-root user
USER root

# Make the start_and_run.sh script executable
RUN chmod +x ./setup_and_run.sh

# Use JSON array syntax for CMD
CMD ["sh", "./setup_and_run.sh"]
