# arduino_sensor_reader.py - Real Arduino Sensor Interface
import serial
import serial.tools.list_ports
import time
import threading
from collections import deque

class ArduinoSensorReader:
    def __init__(self, port=None, baudrate=115200):
        """
        Arduino sensor reader for real-time propeller data

        Expected CSV format from Arduino:
        Power,Voltage,Sound,Torque,RPM,Vibration
        426.5,240.2,46.3,272.1,12500,0.53
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        self.running = False
        self.thread = None
        self.data_buffer = deque(maxlen=1000)

        # Sensor ranges (for validation)
        self.sensor_ranges = {
            'Power': (0, 1830),
            'Voltage': (0, 30),
            'Sound': (0, 50),
            'Torque': (0, 13),
            'rpm': (0, 6000),
            'Vibrations': (0, 10)
        }

        # Calibration (default: no calibration)
        self.calibration = {
            'Power': {'scale': 1.0, 'offset': 0.0},
            'Voltage': {'scale': 1.0, 'offset': 0.0},
            'Sound': {'scale': 1.0, 'offset': 0.0},
            'Torque': {'scale': 1.0, 'offset': 0.0},
            'rpm': {'scale': 1.0, 'offset': 0.0},
            'Vibrations': {'scale': 1.0, 'offset': 0.0}
        }

        self.x = 0

    def find_arduino_port(self):
        """Auto-detect Arduino COM port"""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if 'Arduino' in port.description or 'CH340' in port.description or 'USB' in port.description:
                return port.device
        # Return first available port if Arduino not found
        if ports:
            return ports[0].device
        return None

    def connect(self):
        """Connect to Arduino"""
        if self.port is None:
            self.port = self.find_arduino_port()

        if self.port is None:
            print("❌ No serial ports found!")
            return False

        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            print(f"✅ Connected to Arduino on {self.port}")
            return True
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    def parse_line(self, line):
        """Parse CSV line from Arduino"""
        try:
            # Format: Power,Voltage,Sound,Torque,RPM,Vibration
            parts = line.strip().split(',')
            if len(parts) != 6:
                return None

            # Convert to float
            power = float(parts[0])
            voltage = float(parts[1])
            sound = float(parts[2])
            torque = float(parts[3])
            rpm = float(parts[4])
            vibration = float(parts[5])

            # Apply calibration
            power = power * self.calibration['Power']['scale'] + self.calibration['Power']['offset']
            voltage = voltage * self.calibration['Voltage']['scale'] + self.calibration['Voltage']['offset']
            sound = sound * self.calibration['Sound']['scale'] + self.calibration['Sound']['offset']
            torque = torque * self.calibration['Torque']['scale'] + self.calibration['Torque']['offset']
            rpm = rpm * self.calibration['rpm']['scale'] + self.calibration['rpm']['offset']
            vibration = vibration * self.calibration['Vibrations']['scale'] + self.calibration['Vibrations']['offset']

            # Validate ranges
            if not (self.sensor_ranges['Power'][0] <= power <= self.sensor_ranges['Power'][1]):
                print(f"⚠️ Power out of range: {power}")
                return None
            if not (self.sensor_ranges['Voltage'][0] <= voltage <= self.sensor_ranges['Voltage'][1]):
                print(f"⚠️ Voltage out of range: {voltage}")
                return None
            if not (self.sensor_ranges['rpm'][0] <= rpm <= self.sensor_ranges['rpm'][1]):
                print(f"⚠️ RPM out of range: {rpm}")
                return None

            self.x += 1

            return {
                'x_value': self.x,
                'Power': round(power, 2),
                'Voltage': round(voltage, 2),
                'Sound': round(sound, 2),
                'Torque': round(torque, 2),
                'rpm': round(rpm, 2),
                'Vibrations': round(vibration, 3)
            }

        except Exception as e:
            print(f"⚠️ Parse error: {e}")
            return None

    def start_reading(self):
        """Start reading from Arduino"""
        if not self.connect():
            print("❌ Failed to connect. Using simulated data.")
            self._start_simulated()
            return

        self.running = True
        self.thread = threading.Thread(target=self._read_loop)
        self.thread.daemon = True
        self.thread.start()
        print("🚀 Arduino data reading started!")

    def _read_loop(self):
        """Background thread to read Arduino data"""
        while self.running:
            try:
                if self.serial_conn and self.serial_conn.in_waiting:
                    line = self.serial_conn.readline().decode('utf-8', errors='ignore')
                    data_point = self.parse_line(line)
                    if data_point:
                        self.data_buffer.append(data_point)
                        print(f"📊 Received: Power={data_point['Power']}W, RPM={data_point['rpm']}")
                else:
                    time.sleep(0.1)
            except Exception as e:
                print(f"❌ Read error: {e}")
                time.sleep(1)

    def _start_simulated(self):
        """Fallback: Start simulated data if Arduino not connected"""
        import random
        self.running = True

        def simulate():
            while self.running:
                self.x += 1
                data_point = {
                    'x_value': self.x,
                    'Power': round(200 + random.uniform(-50, 50), 2),
                    'Voltage': round(240 + random.uniform(-20, 20), 2),
                    'Sound': round(50 + random.uniform(-10, 10), 2),
                    'Torque': round(300 + random.uniform(-50, 50), 2),
                    'rpm': round(12000 + random.uniform(-1000, 1000), 2),
                    'Vibrations': round(0.5 + random.uniform(-0.2, 0.2), 3)
                }
                self.data_buffer.append(data_point)
                time.sleep(1)

        self.thread = threading.Thread(target=simulate)
        self.thread.daemon = True
        self.thread.start()
        print("⚠️ Using simulated data (Arduino not connected)")

    def get_latest_data(self, num_points=100):
        """Get latest N data points"""
        if not self.data_buffer:
            return []
        return list(self.data_buffer)[-num_points:]

    def get_latest_point(self):
        """Get most recent data point"""
        if self.data_buffer:
            return self.data_buffer[-1]
        return None

    def stop_reading(self):
        """Stop reading and close connection"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        if self.serial_conn:
            self.serial_conn.close()
        print("🛑 Arduino reader stopped")