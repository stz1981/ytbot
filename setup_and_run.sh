#!/bin/bash

# Update and install dependencies
apt-get update
apt-get install -y ffmpeg cron

# Install Python dependencies
pip install --upgrade pip --root-user-action=ignore
pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

# Add crontab file in the cron directory
cp crontab /etc/cron.d/container-cron

# Give execution rights on the cron job
chmod 0644 /etc/cron.d/container-cron

# Apply cron job
crontab /etc/cron.d/container-cron

# Create the log file to be able to run tail
touch /var/log/cron.log

# Start cron and the bot script
cron
python ./bot.py
