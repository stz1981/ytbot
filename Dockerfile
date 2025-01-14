# Dockerfile example with improvements for clarity and best practices
FROM python:3.11-slim

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

# Set environment variables (for non-sensitive data)
ENV TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}

# Make the start_and_run.sh script executable
RUN chmod +x ./setup_and_run.sh

# Use JSON array syntax for CMD
CMD ["sh", "./setup_and_run.sh"]
