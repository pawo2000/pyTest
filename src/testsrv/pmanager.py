from testsrv.pworker import PWorker

class PManager:
    def __init__(self):
        self.workers = {}

    def add(self, name, address):
        if name in self.workers:
            return {"Thread already exists"}
        pw = PWorker(address)
        self.workers[name] = pw
        pw.start()
        return {f"Thread {name} initiated"}

    def start(self, name):
        if not (name in self.workers):
            return {f"Couln't find thread {name}"}
        pw = self.workers[name]
        pw.start()
        return {f"Thread {name} started"}

    def stop(self, name):
        if not (name in self.workers):
            return {f"Couln't find thread {name}"}
        pw = self.workers[name]
        pw.stop()
        return {f"Thread {name} stopped"}

    def remove(self, name):
        if not (name in self.workers):
            return {f"Couln't find thread {name}"}
        pw = self.workers[name]
        pw.stop()
        del self.workers[name]
        return  {f"Thread {name} removed"}

    def remove_all(self):
        for name, pw in self.workers.items():
            pw.init_stop()
        for name, pw in self.workers.items():
            pw.join()
        self.workers.clear()
        return {"All threads removed"}