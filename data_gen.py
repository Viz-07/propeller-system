# python data_gen.py
import csv
import random
import time

x_value = 0
Power = 200
Voltage = 200
Sound = 50
Torque = 300
rpm = 1000
Vibrations = 0.5

fieldnames = ["x_value", "Power", "Voltage", "Sound", "Torque", "rpm", "Vibrations"]


with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while x_value <= 80:
    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "x_value": x_value,
            "Power": Power,
            "Voltage": Voltage,
            "Sound": Sound,
            "Torque": Torque,
            "rpm": rpm,
            "Vibrations": round(Vibrations,3)
        }

        csv_writer.writerow(info)
        print(x_value, Power, Voltage, Sound, Torque, rpm, Vibrations)

        x_value += 1
        Power += random.randint(-15, 20)
        Voltage += random.randint(-10, 15)
        Sound += random.randint(-5, 5)
        Torque += random.randint(-10, 10)
        rpm += random.randint(-50, 50)
        Vibrations += random.uniform(-0.1, 0.1)
        # Simulate a delay to mimic real-time data generation
    time.sleep(1)
    