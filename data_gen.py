# streaming_data_gen.py - SIMPLE DATA GENERATOR
import random
import time
import threading
from collections import deque

class RealTimeDataStreamer:
    def __init__(self):
        self.data_buffer = deque(maxlen=100)
        self.running = False
        self.thread = None

        # Starting values
        self.x = 0
        self.power = 200
        self.voltage = 200
        self.sound = 50
        self.torque = 300
        self.rpm = 1000
        self.vibrations = 0.5

    def start_streaming(self):
        """Start generating data"""
        self.running = True
        self.thread = threading.Thread(target=self._generate_loop)
        self.thread.daemon = True
        self.thread.start()
        print("✅ Data streaming started!")

    def _generate_loop(self):
        """Generate data every second"""
        while self.running:
            # Update values
            self.x += 1
            self.power += random.randint(-15, 20)
            self.voltage += random.randint(-10, 15)
            self.sound += random.randint(-5, 5)
            self.torque += random.randint(-10, 10)
            self.rpm += random.randint(-50, 50)
            self.vibrations += random.uniform(-0.1, 0.1)

            # Store data
            data_point = {
                'x_value': self.x,
                'Power': self.power,
                'Voltage': self.voltage,
                'Sound': self.sound,
                'Torque': self.torque,
                'rpm': self.rpm,
                'Vibrations': round(self.vibrations, 2)
            }

            self.data_buffer.append(data_point)
            time.sleep(1)

    def get_latest_data(self, num_points=50):
        """Get recent data points"""
        if not self.data_buffer:
            return []
        return list(self.data_buffer)[-num_points:]

    def get_latest_point(self):
        """Get most recent point"""
        if self.data_buffer:
            return self.data_buffer[-1]
        return None