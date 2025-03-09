import concurrent.futures
from typing import override

import requests
from dotenv import load_dotenv

from subscriber_interface import Registration, SubscriberInterface, Message
from utility import handle_futures

load_dotenv()


class TelegramRegistration(Registration):
    def __init__(self, bot_token: str, chat_id: str):
        super().__init__()
        self.bot_token = bot_token
        self.chat_id = chat_id


class TelegramSubscriber(SubscriberInterface):
    def __init__(self):
        super().__init__()

    @override
    def register(self, registration_info: Registration):
        if type(registration_info) != TelegramRegistration:
            raise TypeError("TelegramRegistration::register input must be of type PushoverRegistration")
        super().register(registration_info)

    @override
    def notify_subscribers(self, message: Message):
        if len(self.registered_subscribers) < 1:
            raise RuntimeError("TelegramSubscriber::notify_subscribers at least one recipient needs to be defined")

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.registered_subscribers)) as executor:
            futures = [executor.submit(self.__send_payload, subscriber.bot_token, subscriber.chat_id,
                                       message) for subscriber in self.registered_subscribers]

            handle_futures(futures)

    def __send_payload(self, bot_token: str, chat_id: str, message: Message):
        requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage", params={
            "chat_id": chat_id,
            "text": message.body
        })
