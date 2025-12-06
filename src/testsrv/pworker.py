import threading
import time
from testsrv.tlogger import TLogger

class PWorker:

    def __init__(self, address):
        self.started = False
        self.address = address
        self.logger = TLogger.create_logger(f"PWorker-{self.address}")
        self._thread = threading.Thread(target=self._run, daemon=True)
        self.logger.info(f"Initialized PWorker for address: {self.address}");
    
    def start(self):
        if(self.started == True):
            return
        self.started = True
        self._thread.start()

    def init_stop(self):
        if(self.started == False):
            return
        self.started = False
        self.logger.info(f"Stop signal sent to worker at {self.address}")

    def join(self):
        self._thread.join()   

    def stop(self):
        self.init_stop()
        self._thread.join()   

    def _run(self):
        while self.started:
            self.logger.info(f"Worker running at {self.address}")
            time.sleep(1)
        self.logger.info(f"Worker at {self.address} stopped")
