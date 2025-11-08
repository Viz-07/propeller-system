# streaming_data_gen.py - Memory-based real-time data generation
import json
import random
import time
import threading
from collections import deque
from datetime import datetime
import redis  # pip install redis

class RealTimeDataStreamer:
    def __init__(self, max_points=1000, use_redis=False):
        self.max_points = max_points
        self.data_buffer = deque(maxlen=max_points)
        self.use_redis = use_redis

        if use_redis:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

        # Initialize starting values
        self.current_values = {
            'x_value': 0,
            'Power': 200,
            'Voltage': 200,
            'Sound': 50,
            'Torque': 300,
            'rpm': 1000,
            'Vibrations': 0.5,
            'timestamp': time.time()
        }

        self.running = False
        self.thread = None

    def start_streaming(self):
        """Start the background data generation thread"""
        self.running = True
        self.thread = threading.Thread(target=self._generate_data_loop)
        self.thread.daemon = True
        self.thread.start()
        print("🚀 Real-time data streaming started!")

    def stop_streaming(self):
        """Stop the data generation"""
        self.running = False
        if self.thread:
            self.thread.join()
        print("⏹️ Data streaming stopped.")

    def _generate_data_loop(self):
        """Background thread that generates data every second"""
        while self.running:
            # Generate new data point
            self.current_values['x_value'] += 1
            self.current_values['Power'] += random.randint(-15, 20)
            self.current_values['Voltage'] += random.randint(-10, 15)
            self.current_values['Sound'] += random.randint(-5, 5)
            self.current_values['Torque'] += random.randint(-10, 10)
            self.current_values['rpm'] += random.randint(-50, 50)
            self.current_values['Vibrations'] += random.uniform(-0.1, 0.1)
            self.current_values['timestamp'] = time.time()

            # Add to buffer
            data_point = self.current_values.copy()
            self.data_buffer.append(data_point)

            # Optional: Store in Redis for multi-process access
            if self.use_redis:
                self.redis_client.lpush('sensor_data', json.dumps(data_point))
                self.redis_client.ltrim('sensor_data', 0, self.max_points-1)

            # Print current values (optional)
            print(f"⚡ Generated: Power={data_point['Power']}, Voltage={data_point['Voltage']}, Sound={data_point['Sound']}")

            time.sleep(1)  # Generate every second

    def get_latest_data(self, num_points=None):
        """Get the latest data points"""
        if not self.data_buffer:
            return []

        if num_points is None:
            return list(self.data_buffer)
        else:
            return list(self.data_buffer)[-num_points:]

    def get_latest_point(self):
        """Get just the most recent data point"""
        if self.data_buffer:
            return self.data_buffer[-1]
        return None

# Usage example
if __name__ == "__main__":
    streamer = RealTimeDataStreamer(max_points=1000)

    try:
        streamer.start_streaming()

        # Keep running
        while True:
            time.sleep(5)
            latest = streamer.get_latest_point()
            if latest:
                print(f"📊 Latest readings: Power={latest['Power']}W, RPM={latest['rpm']}")

    except KeyboardInterrupt:
        streamer.stop_streaming()
        print("\n👋 Streaming stopped by user")