/*
 * Arduino Propeller Sensor Interface
 * Sends CSV data to Python dashboard
 * 
 * Expected CSV format:
 * Power,Voltage,Sound,Torque,RPM,Vibration
 * 426.5,240.2,46.3,272.1,12500,0.53
 */

// Pin definitions (adjust based on your sensors)
const int POWER_PIN = A0;
const int VOLTAGE_PIN = A1;
const int SOUND_PIN = A2;
const int TORQUE_PIN = A3;
const int RPM_PIN = 2;  // Digital pin for RPM sensor
const int VIBRATION_PIN = A4;

// Timing
unsigned long lastSendTime = 0;
const int SEND_INTERVAL = 1000;  // Send every 1 second

void setup() {
  Serial.begin(115200);
  pinMode(RPM_PIN, INPUT);

  // Wait for serial connection
  while (!Serial) {
    delay(10);
  }

  Serial.println("Arduino Ready");
}

void loop() {
  unsigned long currentTime = millis();

  if (currentTime - lastSendTime >= SEND_INTERVAL) {
    lastSendTime = currentTime;

    // Read sensors (replace with your actual sensor reading code)
    float power = readPower();
    float voltage = readVoltage();
    float sound = readSound();
    float torque = readTorque();
    float rpm = readRPM();
    float vibration = readVibration();

    // Send CSV data
    Serial.print(power);
    Serial.print(",");
    Serial.print(voltage);
    Serial.print(",");
    Serial.print(sound);
    Serial.print(",");
    Serial.print(torque);
    Serial.print(",");
    Serial.print(rpm);
    Serial.print(",");
    Serial.println(vibration);
  }
}

// Sensor reading functions (implement based on your sensors)
float readPower() {
  // Read power sensor
  int rawValue = analogRead(POWER_PIN);
  float power = map(rawValue, 0, 1023, 0, 1000);  // Scale to 0-1000W
  return power;
}

float readVoltage() {
  // Read voltage sensor
  int rawValue = analogRead(VOLTAGE_PIN);
  float voltage = map(rawValue, 0, 1023, 0, 300);  // Scale to 0-300V
  return voltage;
}

float readSound() {
  // Read sound level meter
  int rawValue = analogRead(SOUND_PIN);
  float sound = map(rawValue, 0, 1023, 0, 120);  // Scale to 0-120dB
  return sound;
}

float readTorque() {
  // Read torque sensor
  int rawValue = analogRead(TORQUE_PIN);
  float torque = map(rawValue, 0, 1023, 0, 500);  // Scale to 0-500Nm
  return torque;
}

float readRPM() {
  // Read RPM sensor (Hall sensor)
  // This is a simplified example - implement proper RPM calculation
  int rawValue = pulseIn(RPM_PIN, HIGH, 100000);
  float rpm = (rawValue > 0) ? (60000.0 / rawValue) : 0;
  rpm = constrain(rpm, 0, 20000);
  return rpm;
}

float readVibration() {
  // Read IMU vibration sensor
  int rawValue = analogRead(VIBRATION_PIN);
  float vibration = map(rawValue, 0, 1023, 0, 1000) / 100.0;  // Scale to 0-10Hz
  return vibration;
}
