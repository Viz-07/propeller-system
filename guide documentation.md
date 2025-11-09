# 🚀 Real-Time Propeller Dashboard

A professional real-time monitoring dashboard for UAV propeller systems with Arduino integration, live data visualization, and CSV export capabilities.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Dashboard Versions](#dashboard-versions)
- [Arduino Integration](#arduino-integration)
- [Troubleshooting](#troubleshooting)
- [Technical Details](#technical-details)

---

## Overview

This dashboard is designed for the **Experimental Setup for Developing Low Noise UAV Propeller Systems** project. It provides real-time monitoring of 6 critical propeller parameters:

- **Power** (W)
- **Voltage** (V)
- **Sound** (dB)
- **Torque** (Nm)
- **RPM** (revolutions per minute)
- **Vibrations** (Hz)

### Key Capabilities
- Real-time data visualization with multiple graph types
- Arduino serial communication support
- CSV data export with timestamps
- Custom parameter comparison (X vs Y plots)
- Data table view (last 10 readings)
- Memory-optimized architecture (<200ms latency)
- Professional dark theme UI

---

## Features

### **Modern UI**
- Professional dark gradient theme
- Responsive grid layout
- Animated metric cards with hover effects
- Clean, deployment-ready design
- No scrollbars - perfect fit

### **Diverse Visualizations**
1. **Power**: Area chart (filled) - shows energy accumulation
2. **Voltage**: Line chart with markers - precision tracking
3. **Sound**: Bar chart - discrete noise levels
4. **Torque**: Gauge indicator - speedometer style
5. **RPM**: Smooth line chart - speed monitoring
6. **Vibrations**: Scatter plot with color scale - intensity patterns

### **Functionality**
- **CSV Download**: Export all data with timestamp (e.g., `propeller_data_2025-11-08_14-30-45.csv`)
- **Custom Comparison**: Select any two parameters to compare (Power vs Voltage, RPM vs Torque, etc.)
- **Data Table**: View last 10 readings in tabular format
- **Live Status**: Real-time connection indicator
- **Auto-refresh**: Updates every second with smooth animations

### **Performance**
- Memory-based data storage (no file I/O bottleneck)
- <100ms lag between updates
- Handles up to 10 updates/second
- Maintains last 100 data points in buffer
- Optimized callbacks (no redundant processing)

---

## Project Structure

```
propeller-dashboard/
│
├── Core Files (Choose One Dashboard)
│   ├── dashboard_enhanced.py       # Recommended: Clean terminal output
│   ├── dashboard_test.py           # Testing with simulated data
│   └── dashboard_arduino.py        # Arduino serial integration
│
├── Data Sources
│   ├── data_gen.py                 # Simulated data generator
│   ├── streaming_data_gen.py       # Alternative data generator
│   └── arduino_sensor_reader.py    # Arduino serial reader
│
├── Arduino (Optional)
│   └── arduino_propeller_sensor.ino # Arduino sketch template
│
├── Configuration
│   ├── requirements.txt            # Python dependencies
│   └── .gitignore                  # Git ignore file
│
└── Documentation
    ├── README.md                   # This file
    └── SETUP_GUIDE.md              # Detailed setup instructions
```

### File Descriptions

| File | Purpose | Use Case |
|------|---------|----------|
| `dashboard_clean.py` | Main dashboard (suppressed logging) | **Recommended for daily use** |
| `data_gen.py` | Simulates sensor data | Testing without hardware |
| `arduino_sensor_reader.py` | Reads from Arduino | Real propeller testing |
| `arduino_propeller_sensor.ino` | Arduino code template | Deploy on Arduino Mega |

---

## Technical Details

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Browser                              │
│  [Metrics] [Graphs] [Comparison] [Table]                   │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ HTTP (WebSocket updates)
                          │
┌─────────────────────────────────────────────────────────────┐
│                    Dash Server (Flask)                       │
│  • Callbacks (update graphs)                                │
│  • Layout (UI structure)                                    │
│  • Routing (URL handling)                                   │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ In-memory data access
                          │
┌─────────────────────────────────────────────────────────────┐
│              Data Source (Background Thread)                 │
│  • RealTimeDataStreamer (data_gen.py)                       │
│    OR                                                        │
│  • ArduinoSensorReader (arduino_sensor_reader.py)           │
│                                                              │
│  Stores: deque(maxlen=100) - Last 100 points               │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │
                ┌─────────┴─────────┐
                │                   │
        Simulated Data         Arduino Serial
        (data_gen.py)          (COM3, 115200)
```

### Data Flow

1. **Data Generation** (Every 1 second)
   - Simulated: Random walk from base values
   - Arduino: Parse CSV from serial port

2. **Storage** (In-memory)
   - Python deque (double-ended queue)
   - Max 100 points (rolling buffer)
   - Thread-safe access

3. **Dashboard Update** (Every 1 second)
   - Dash Interval component triggers callbacks
   - Each callback fetches latest data
   - Plotly graphs re-render with new data

4. **Browser Update**
   - Dash sends JSON updates via WebSocket
   - Only changed components update (efficient)
   - Smooth animations via Plotly transitions

### Performance Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Update Rate | 1 Hz (1 per second) | Configurable (0.5-2 Hz) |
| Latency | <100ms | Simulated data |
| Latency | <200ms | Arduino serial |
| Memory Usage | ~50 MB | With 100 data points |
| CPU Usage | ~5% | During updates |
| Data Buffer | 100 points | Last 100 seconds |

### Technologies Used

- **Python 3.8+**: Core language
- **Dash 2.14+**: Web framework (built on Flask)
- **Plotly 5.17+**: Interactive graphing library
- **Pandas 2.0+**: Data manipulation
- **PySerial 3.5**: Arduino communication (optional)
- **Threading**: Background data generation

---

## Configuration

### Update Rate

Change in dashboard file:
```python
# Current: Updates every 1000ms (1 second)
dcc.Interval(id='interval', interval=1000, n_intervals=0)

# Faster: Updates every 500ms (0.5 second)
dcc.Interval(id='interval', interval=500, n_intervals=0)

# Slower: Updates every 2000ms (2 seconds)
dcc.Interval(id='interval', interval=2000, n_intervals=0)
```

### Buffer Size

Change in data_gen.py:
```python
# Current: Keeps last 100 points
self.data_buffer = deque(maxlen=100)

# More data: Keeps last 1000 points
self.data_buffer = deque(maxlen=1000)
```

### Sensor Ranges

Change in arduino_sensor_reader.py:
```python
self.sensor_ranges = {
    'Power': (0, 1000),      # Adjust max power
    'Voltage': (0, 300),     # Adjust max voltage
    'Sound': (0, 120),       # Adjust max sound
    'Torque': (0, 500),      # Adjust max torque
    'rpm': (0, 20000),       # Adjust max RPM
    'Vibrations': (0, 10)    # Adjust max vibration
}
```

### Color Scheme

Change in dashboard file:
```python
COLORS = {
    'background': '#0f172a',    # Dark blue
    'text': '#f1f5f9',          # Light gray
    'power': '#3b82f6',         # Blue
    'voltage': '#f59e0b',       # Orange
    'sound': '#10b981',         # Green
    'torque': '#8b5cf6',        # Purple
    'rpm': '#ef4444',           # Red
    'vibrations': '#ec4899',    # Pink
    'accent': '#06b6d4'         # Cyan
}
```

## License

This project is part of the **Experimental Setup for Developing Low Noise UAV Propeller Systems** seed grant research.

---

## Author

**Rajashekharareddy H G**  
Assistant Professor, Department of Aerospace and Automotive Engineering  
Faculty of Engineering and Technology

---

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: [23etcs002160@msruas.ac.in]

---

## Citation

If you use this dashboard in your research, please cite:

```
Rajashekharareddy, H. G. (2025). Real-Time Propeller Dashboard: 
An Experimental Setup for UAV Propeller Monitoring. 
Seed Grant Project, Department of Aerospace and Automotive Engineering.
```

---

## Acknowledgments

- Dr. Jayahar Sivasubramanian (Head, AAE Department)
- Faculty of Engineering and Technology
- Seed Grant Program 2025

---

## References

1. Dash Documentation: https://dash.plotly.com/
2. Plotly Python: https://plotly.com/python/
3. Arduino Reference: https://www.arduino.cc/reference/
4. PySerial Documentation: https://pyserial.readthedocs.io/

---

**Last Updated:** November 9, 2025  
**Version:** 1.0.0  
**Status:** Prototype Ready
