from logging import getLogger


class BaseDevice():
    def __init__(self, serializer):
        self.serializer = serializer
        self.logger = getLogger("BaseDevice")
