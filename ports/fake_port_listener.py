import tkinter as tk
import threading
import random
import time


class FakePortListener:
    def __init__(self, port_id):
        self.port_id = port_id
        self.running = False
        self.paused = False
        self.subscribers = []
        self.data = [0] * 100
        self.thread = None

    def start(self):
        if self.thread is None:
            self.running = True
            self.paused = False
            self.thread = threading.Thread(target=self._listen, daemon=True)
            self.thread.start()
        else:
            self.paused = False

    def pause(self):
        self.paused = True

    def stop(self):
        self.running = False
        self.thread = None

    def subscribe(self, cb):
        self.subscribers.append(cb)

    def _notify_subscribers(self):
        for cb in self.subscribers:
            cb(self.data)

    def _listen(self):
        while self.running:
            if self.paused:
                time.sleep(0.05)
                continue

            self.data = [random.randint(0, 100) for _ in range(100)]
            self._notify_subscribers()
            time.sleep(0.05)
