import concurrent.futures
import os
import smtplib
from typing import override

from dotenv import load_dotenv

# local imports
from subscribers.subscriber_interface import SubscriberInterface, Message, Registration
from utility import handle_futures

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
PORT = 587


class EmailRegistration(Registration):
    def __init__(self, recipient_email):
        super().__init__()
        self.email = recipient_email


class EmailSubscriber(SubscriberInterface):
    def __init__(self):
        super().__init__()
        self.app_password = None
        self.sender_email = None
        self.initialize_service()

    @override
    def initialize_service(self):
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.app_password = os.getenv("APP_PASSWORD")

    @override
    def register(self, registration_info: Registration):
        if type(registration_info) != EmailRegistration:
            raise TypeError("EmailSubscriber::register input must be of type EmailRegistration")

        super().register(registration_info)

    @override
    def notify_subscribers(self, message: Message):
        message = f"Subject: {message.subject}\n\n{message.body}"

        if len(self.registered_subscribers) < 1:
            raise RuntimeError("EmailSubscriber::notify_subscribers at least one recipient needs to be defined")

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.registered_subscribers)) as executor:
            futures = [executor.submit(self.__send_payload, each_recipient.email, message)
                       for each_recipient in self.registered_subscribers]

            handle_futures(futures)

    def __send_payload(self, recipient, message: Message):
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.starttls()
            server.login(self.sender_email, self.app_password)
            server.sendmail(self.sender_email, recipient, message)
