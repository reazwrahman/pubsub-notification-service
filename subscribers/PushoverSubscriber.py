import concurrent.futures
from typing import override

import requests
from dotenv import load_dotenv

from subscriber_interface import Registration, SubscriberInterface, Message
from utility import handle_futures

load_dotenv()

URL = "https://api.pushover.net:443/1/messages.json"


class PushoverRegistration(Registration):
    def __init__(self, app_token, user_key):
        super().__init__()
        self.app_token = app_token
        self.user_key = user_key


class PushoverSubscriber(SubscriberInterface):
    def __init__(self):
        super().__init__()
        self.app_token = None
        self.user_key = None

    @override
    def register(self, registration_info: PushoverRegistration):
        if type(registration_info) != PushoverRegistration:
            raise TypeError("PushoverSubscriber::register input must be of type PushoverRegistration")

        super().register(registration_info)

    @override
    def notify_subscribers(self, message: Message):
        if len(self.registered_subscribers) < 1:
            raise RuntimeError("PushoverSubscriber::notify_subscribers at least one recipient needs to be defined")

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.registered_subscribers)) as executor:
            futures = [executor.submit(self.__send_payload, subscriber.app_token,
                                       subscriber.user_key, message)
                       for subscriber in self.registered_subscribers]

            handle_futures(futures)

    def __send_payload(self, token: str, user_key: str, message: Message):
        payload = {
            "token": token,
            "user": user_key,
            "message": message.body
        }

        response = requests.post(URL, data=payload)
        # Check if the request was successful
        if response.status_code != 200:
            print(
                f"PushoverSubscriber::notify_subscribers Failed to send notification. Status code: {response.status_code}")
            print(response.text)
