import concurrent.futures
import datetime
import os

from dotenv import load_dotenv

from subscribers.PushoverSubscriber import PushoverSubscriber, PushoverRegistration
from subscribers.TelegramSubscriber import TelegramSubscriber, TelegramRegistration
from subscribers.email_subscriber import EmailSubscriber, EmailRegistration
from subscribers.subscriber_interface import Message
from utility import handle_futures

load_dotenv()


def register_email_subscribers() -> EmailSubscriber:
    email_subscriber: EmailSubscriber = EmailSubscriber()
    email_subscriber.register(EmailRegistration(os.getenv("SENDER_EMAIL")))
    return email_subscriber


def register_pushover_subscribers() -> PushoverSubscriber:
    pushover_subscriber = PushoverSubscriber()
    pushover_subscriber.register(PushoverRegistration(
        app_token=os.getenv("APP_TOKEN"),
        user_key=os.getenv("USER_KEY")
    ))
    return pushover_subscriber


def register_telegram_subscribers() -> TelegramSubscriber:
    telegram_subscriber = TelegramSubscriber()
    telegram_subscriber.register(TelegramRegistration(
        bot_token=os.getenv("BOT_TOKEN"),
        chat_id=os.getenv("CHAT_ID")
    ))
    return telegram_subscriber


def publish(message: Message):
    subscribers = [register_email_subscribers(), register_pushover_subscribers(),
                   register_telegram_subscribers()]

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        futures: list[concurrent.futures.Future] = [executor.submit(each.notify_subscribers, message) for each in
                                                    subscribers]
        handle_futures(futures)


if __name__ == "__main__":
    message = Message(body=f"Notification {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}",
                      subject=f"Test Notification {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
    publish(message)
