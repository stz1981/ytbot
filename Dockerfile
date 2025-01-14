# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Create a non-root user
RUN useradd -ms /bin/bash ytbotuser

# Change to the non-root user
USER ytbotuser

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Set environment variables (for non-sensitive data)
ENV TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x ./start_and_run.sh
CMD ["sh", "./start_and_run.sh"]
