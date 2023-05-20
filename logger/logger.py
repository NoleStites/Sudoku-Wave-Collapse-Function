
from threading import Lock, Thread


class LoggerMeta(type):
    """
    This is a thread-safe implementation of a Singleton Logger. 
    Taken from the example code in the Logger lab due to its complexity.
    """
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            # The first thread to acquire the lock creates 
            # Singleton instance
            # Other threads cannot access until lock is realesed
            # They won't create new object
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Logger(metaclass=LoggerMeta):
    """
    This class is used to log any desired content to a given file.
    """
    def __init__(self, file_path: str):
        # File path of the file to write to
        self.file_path = file_path

    def log(self, string_to_log: str):
        """
        Takes in a string and appends it to the given file.
        """
        # Open the file and write to it
        open_file = open(self.file_path, "a")
        open_file.write(string_to_log)

        # Done writing so close file
        open_file.close()
