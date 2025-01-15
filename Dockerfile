# Dockerfile example with improvements for clarity and best practices
FROM python:3.11-slim

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

# Make the start_and_run.sh script executable
RUN chmod +x ./setup_and_run.sh

# Define volumes for Audio and Video directories
VOLUME ["/app/Audio", "/app/Video"]

# Use JSON array syntax for CMD
CMD ["sh", "./setup_and_run.sh"]
