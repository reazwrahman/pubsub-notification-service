class Registration(object):
    def __init__(self):
        pass


class Message(object):
    def __init__(self, body, subject=None):
        self.subject = subject
        self.body = body


class SubscriberInterface(object):
    def __init__(self):
        self.registered_subscribers: list[Registration] = []

    def initialize_service(self):
        pass

    def register(self, registration_info: Registration):
        self.registered_subscribers.append(registration_info)

    def notify_subscribers(self, message: Message):
        pass
