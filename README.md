# ytbot: Your YouTube Downloader Telegram Bot

Welcome to **ytbot**, a Telegram bot that makes downloading videos and audio from YouTube as easy as sending a message. Just share the YouTube URL, select the format and quality, and receive your file instantly—all within Telegram!

## 🌟 Features

- **Video Downloads**: Supports resolutions like 8K, UHD, 4K, Full HD, HD, and more.
- **Audio Downloads**: Choose from various bitrates including 320 kbps, 256 kbps, 160 kbps, and 128 kbps.
- **User-Friendly**: Simple and efficient—just share a link, select options, and you're done!

## 🛠 Prerequisites

Before setting up the bot, ensure you have the following:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Telegram Bot Token**: Create a bot via [BotFather](https://core.telegram.org/bots#botfather) and get your API token.

---

## 🚀 Running the Bot with Docker

### 1. Clone the Repository

Start by cloning the repository and navigating to the project folder:

```bash
git clone https://github.com/stz1981/ytbot.git
cd ytbot
```

### 2. Run the Bot Using Docker

To start the bot as a Docker container, run the following command:

```bash
docker run -d \
  --name ytbot \
  -e TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN \
  talalzaki/ytbot:latest
```

Make sure to replace `$TELEGRAM_BOT_TOKEN` with your actual token.

---

## 🧩 Running with Docker Compose

Alternatively, you can use **Docker Compose** for easier management. Create a `docker-compose.yml` file with the following content:

```yaml
version: "3.8"

services:
  ytbot:
    container_name: ytbot
    image: talalzaki/ytbot:latest
    environment:
      - TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
```

Then, run the bot with:

```bash
docker compose up -d
```

---

## 🎉 Enjoy the Experience!

Your bot is now live and ready to help users download their favorite YouTube videos and audio files. Share your bot with others and let them enjoy the seamless experience too!

For any questions or issues, feel free to open an issue on [GitHub](https://github.com/stz1981/ytbot). 💬
```
