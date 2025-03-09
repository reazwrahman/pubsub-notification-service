# PubSub Notification Service

A simple, extensible **Pub/Sub Notification Service** that allows a single message to be published to **multiple subscribers** across different communication channels. 

The project leverages multithreading and multiprocessing to concurrently publish messages to multiple subscribers.

![IMG_1382](https://github.com/user-attachments/assets/894ed5bb-a0a1-4c7d-a002-b4df8f526d6c)

## ✨ Features

- Publish a single message to multiple subscriber channels
- Currently supports:
  - 📧 Email notifications
  - 🤖 Telegram Bot notifications
  - 📲 Pushover notifications
- Easily extendable to support additional mediums
- Designed to be **reused as a library** in other projects

## 📦 Use Case

This package was built to serve as a **reusable notification module** that can be integrated into various projects. Whenever a notification needs to be published across multiple channels, simply plug in this service.

## 📚 How It Works

- A message is published once.
- The service distributes the message to all configured subscribers across the available channels.
- Each notification medium can have **multiple subscribers**.
- The `subscribers` package is modular and designed to support more subscriber types in the future.

## 🔧 Current Subscribers

| Medium      | Description                              |
|-------------|------------------------------------------|
| Email       | Sends emails using SMTP                  |
| Telegram    | Sends messages via Telegram Bot API      |
| Pushover    | Sends push notifications to Pushover app |

## 🔌 Example Usage
Take a look at the message_publisher.py file for example usage. 

## Sample .env file
```
#email
SENDER_EMAIL=
APP_PASSWORD=

#telegram
BOT_TOKEN=
CHAT_ID=

#pushover
APP_TOKEN=
USER_KEY=

```

