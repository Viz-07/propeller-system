# Complete Setup Guide

This guide provides detailed step-by-step instructions to set up and run the Real-Time Propeller Dashboard from scratch.

---

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Software Installation](#software-installation)
3. [Project Setup](#project-setup)
4. [First Run](#first-run)
5. [Verification](#verification)
6. [Next Steps](#next-steps)

---

## 1. System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 20.04+)
- **RAM**: 4 GB
- **Storage**: 500 MB free space
- **Python**: 3.8 or higher

### Recommended
- **OS**: Windows 11 or macOS 13+
- **RAM**: 8 GB
- **Storage**: 1 GB free space
- **Python**: 3.10 or 3.11

---

## 2. Software Installation

### Step 2.1: Install Python

#### Windows:
1. Go to https://www.python.org/downloads/
2. Download Python 3.11+ installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```powershell
   python --version
   # Should show: Python 3.11.x
   ```

#### macOS:
```bash
# Using Homebrew
brew install python@3.11

# Verify
python3 --version
```

#### Linux (Ubuntu/Debian):
```bash
# Update package list
sudo apt update

# Install Python
sudo apt install python3.11 python3.11-venv python3-pip

# Verify
python3 --version
```

---

### Step 2.2: Install Git

#### Windows:
1. Go to https://git-scm.com/download/win
2. Download and install
3. Use default settings
4. Verify:
   ```powershell
   git --version
   ```

#### macOS:
```bash
# Using Homebrew
brew install git

# Verify
git --version
```

#### Linux:
```bash
sudo apt install git

# Verify
git --version
```

---

### Step 2.3: Install VS Code (Recommended)

1. Go to https://code.visualstudio.com/
2. Download for your OS
3. Install with default settings
4. Launch VS Code

**Recommended Extensions:**
- Python (Microsoft)
- Pylance (Microsoft)
- GitLens

---

## 3. Project Setup

### Step 3.1: Open Terminal in VS Code

1. Launch VS Code
2. Press `` Ctrl + ` `` (backtick) or go to **View > Terminal**
3. Terminal opens at bottom of VS Code

---

### Step 3.2: Navigate to Workspace

```bash
# Create a workspace folder (if needed)
# Windows:
cd C:\Users\YourUsername\Documents
mkdir PropellerProject
cd PropellerProject

# macOS/Linux:
cd ~/Documents
mkdir PropellerProject
cd PropellerProject
```

---

### Step 3.3: Clone Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/propeller-dashboard.git

# Navigate into project
cd propeller-dashboard

# Verify files
ls  # macOS/Linux
dir # Windows

# Should see:
# dashboard_clean.py
# data_gen.py
# requirements.txt
# README.md
# etc.
```

**No Git Repository?** If you have files manually:
```bash
# Create project folder
mkdir propeller-dashboard
cd propeller-dashboard

# Copy your files here:
# - dashboard_clean.py
# - data_gen.py
# - requirements.txt
```

---

### Step 3.4: Create Virtual Environment

**Why?** Isolates project dependencies from system Python.

#### Windows (PowerShell):
```powershell
# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activate again
.\venv\Scripts\Activate.ps1

# Success! You should see (venv) in prompt:
# (venv) PS C:\Users\...\propeller-dashboard>
```

#### Windows (Command Prompt):
```cmd
# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate.bat

# Success! You should see (venv) in prompt:
# (venv) C:\Users\...\propeller-dashboard>
```

#### macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Success! You should see (venv) in prompt:
# (venv) user@computer:~/propeller-dashboard$
```

---

### Step 3.5: Upgrade pip

```bash
# Upgrade pip to latest version
python -m pip install --upgrade pip

# Verify
pip --version
# Should show: pip 24.x or higher
```

---

### Step 3.6: Install Dependencies

#### Method 1: Individual Packages (Recommended)
```bash
# Install core packages
pip install dash plotly pandas

# Expected output:
# Collecting dash...
# Collecting plotly...
# Collecting pandas...
# Installing collected packages: ...
# Successfully installed dash-2.x plotly-5.x pandas-2.x
```

#### Method 2: From requirements.txt
```bash
# Install from requirements file
pip install -r requirements.txt

# Same result as Method 1
```

#### Method 3: With Arduino Support
```bash
# If using Arduino
pip install dash plotly pandas pyserial
```

---

### Step 3.7: Verify Installation

```bash
# Check installed packages
pip list

# Should see:
# Package    Version
# ---------- -------
# dash       2.14.1 (or higher)
# plotly     5.17.0 (or higher)
# pandas     2.0.3 (or higher)
# ... (and dependencies)
```

Test imports:
```bash
python -c "import dash, plotly, pandas; print('All packages installed!')"

# Should print:
# All packages installed!
```

---

## 4. First Run

### Step 4.1: Start Dashboard

```bash
# Make sure you're in project directory with venv activated
# You should see (venv) in prompt

# Run dashboard
python dashboard_clean.py

# Expected output:
# Data streaming started!
# Dashboard starting...
# Open: http://127.0.0.1:8050
# Terminal logging suppressed (clean output)
```
**Dashboard is now running!** 
---

### Step 4.2: Access Dashboard

1. **Open your web browser** (Chrome, Firefox, Edge, Safari)

2. **Go to:**
   ```
   http://127.0.0.1:8050
   ```
   or
   ```
   http://localhost:8050
   ```

3. **You should see:**
   - Real-Time Propeller Dashboard (title)
   - LIVE indicator
   - Download CSV button
   - 6 metric cards (Power, Voltage, Sound, etc.)
   - 6 different graphs
   - Custom Comparison section
   - Data table at bottom

---

### Step 4.3: Interact with Dashboard

**Try these features:**

1. **Watch Live Updates**
   - Metric cards update every second
   - Graphs animate smoothly
   - Notice the data flowing

2. **Download CSV**
   - Click "Download CSV" button
   - File downloads: `propeller_data_2025-11-09_11-30-45.csv`
   - Open in Excel/Calc to view data

3. **Custom Comparison**
   - Scroll to "Custom Comparison"
   - Click X-axis dropdown → Select "Power"
   - Click Y-axis dropdown → Select "Voltage"
   - See scatter plot showing correlation

4. **View Data Table**
   - Scroll to bottom
   - See "Latest Data (Last 10 Readings)"
   - Table shows recent values

---

### Step 4.4: Stop Dashboard

When you're done:

1. **Go to terminal** (VS Code terminal where dashboard is running)

2. **Press:**
   ```
   Ctrl + C
   ```

3. **Expected output:**
   ```
   ^C
   KeyboardInterrupt
   (dashboard stops cleanly)
   ```

4. **Dashboard and data generator stop**

---

## 5. Verification Checklist

Use this to verify everything is working:

### Python Setup
- [ ] Python 3.8+ installed
- [ ] `python --version` works
- [ ] pip works

### Project Setup
- [ ] Repository cloned (or files copied)
- [ ] In project directory
- [ ] Files present (dashboard_clean.py, data_gen.py, etc.)

### Virtual Environment
- [ ] Virtual environment created
- [ ] Virtual environment activated (see `(venv)` in prompt)
- [ ] pip upgraded

### Dependencies
- [ ] dash installed
- [ ] plotly installed
- [ ] pandas installed
- [ ] `pip list` shows packages
- [ ] Test import works

### Dashboard
- [ ] `python dashboard_clean.py` runs without errors
- [ ] Terminal shows startup messages
- [ ] Browser can access http://127.0.0.1:8050
- [ ] Dashboard loads and displays data
- [ ] Graphs update every second
- [ ] CSV download works
- [ ] Comparison graph works
- [ ] Data table shows

---

## 6. Next Steps

### Testing and Development

1. **Experiment with Features**
   - Try different parameter comparisons
   - Download multiple CSV files
   - Let dashboard run for 5 minutes
   - Observe data trends

2. **Customize Dashboard**
   - Change colors in `dashboard_clean.py`
   - Adjust update rate (interval)
   - Modify graph types
   - Add new metrics

3. **Prepare for Arduino**
   - Review `arduino_sensor_reader.py`
   - Check `arduino_propeller_sensor.ino`
   - Plan sensor connections
   - Test Arduino separately

### Arduino Integration (Optional)

When ready for real sensors:

1. **Hardware Setup**
   - Wire sensors to Arduino
   - Upload `arduino_propeller_sensor.ino`
   - Test serial output

2. **Software Setup**
   - Install PySerial: `pip install pyserial`
   - Run: `python dashboard_arduino.py`
   - Dashboard auto-detects Arduino

3. **Calibration**
   - Adjust sensor ranges
   - Apply calibration coefficients
   - Validate measurements

---

## Common Issues

### Issue: "python: command not found"

**Solution:**
```bash
# Try python3 instead
python3 --version

# Or add alias (Linux/Mac)
alias python=python3
```

### Issue: "venv\Scripts\activate not found"

**Solution:**
```powershell
# Windows PowerShell: Use full path
.\venv\Scripts\Activate.ps1

# Windows CMD:
venv\Scripts\activate.bat

# Linux/Mac:
source venv/bin/activate
```

### Issue: Port 8050 already in use

**Solution:**
```bash
# Find and kill process using port 8050
# Windows:
netstat -ano | findstr :8050
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8050 | xargs kill -9
```

### Issue: Browser shows "Unable to connect"

**Check:**
1. Is dashboard running in terminal?
2. Did you see "Dashboard starting" message?
3. Try http://localhost:8050 instead
4. Check Windows Firewall
5. Try different port: Change `port=8050` to `port=8051` in code

---

## Getting Help

If you encounter issues:

1. **Check README.md** - Comprehensive documentation
2. **Review error messages** - Most errors are self-explanatory
3. **Search online** - Copy error message to Google
4. **Open an issue** - GitHub Issues (if using repo)
5. **Contact author** - Email for project-specific questions

---

## Success!

If you completed all steps:
- Project is set up correctly
- Dashboard runs smoothly
- All features work
- Ready for customization or Arduino integration

**Congratulations!** You're ready to use the Real-Time Propeller Dashboard! 🚀

---

**Last Updated:** November 9, 2025  
**Version:** 1.0.0
