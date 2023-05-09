from threading import Lock


class Singleton:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    # cls._instance.cache = {}
        return cls._instance

    def __init__(self):
        if not self.__getattribute__('cache'):
            self.cache = {}

    def add_to_cache(self, key, value):
        self.cache[key] = value





