import logging

class TLogger:

    @classmethod
    @staticmethod
    def create_logger(thread_name):
        logger = logging.getLogger(thread_name)
        if not logger.hasHandlers():
            logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)

            file_handler = logging.FileHandler(f"{thread_name}.log")
            file_handler.setFormatter(formatter)

            logger.addHandler(stream_handler)
            logger.addHandler(file_handler)
        return logger