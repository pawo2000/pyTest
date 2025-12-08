import threading
import time
from testsrv.tlogger import TLogger
from testsrv.pdispatcher import PDispatcher

class PWorker:

    ICMP_LOOP_INTERVAL = 1.0  

    def __init__(self, address, timeout=1.0):
        self.started = False
        self.address = address
        self.timeout = timeout
        self.dispatcher = PDispatcher(self.address, self.timeout)
        self._thread = threading.Thread(target=self._run, daemon=True)
        self.logger = TLogger.create_logger(f"PWorker-{self.address}")
        self.logger.info(f"Initialized PWorker for address: {self.address}")
    
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
        self.dispatcher.init_stop()

    def join(self):
        self._thread.join()   

    def stop(self):
        self.init_stop()
        self._thread.join()   

    def _run(self):
        self.logger.info(f"Worker running at {self.address}")
        while self.started:
            rtt = self.dispatcher.send_icmp_packet()
            self.logger.info(f"Ping {self.address} RTT: {rtt} ms")
            # Control loop timing
            if self.started:
                if(rtt is None):
                    diff = 0
                else:
                    diff = PWorker.ICMP_LOOP_INTERVAL-(rtt/1000.0)
                if(diff>0):
                    time.sleep(diff)
        self.logger.info(f"Worker at {self.address} stopped")
