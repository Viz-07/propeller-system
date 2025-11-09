**Real-Time Propeller Dashboard**

---

## Quick Start

```bash
# 1. Clone and navigate
git clone https://github.com/Viz-07/propeller-system.git
cd propeller-system

# 2. Create & activate venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run dashboard
python dashboard_enhanced.py

# 5. Open browser
http://127.0.0.1:8050

# 6. Stop (when done)
Ctrl+C
```

---

## Dashboard Features

| Feature | How to Use |
|---------|------------|
| **Live Metrics** | Top bar - updates every second |
| **6 Graphs** | Middle section - different types |
| **Download CSV** | Click button in header |
| **Compare** | Dropdowns → select X & Y axes |
| **Data Table** | Bottom - last 10 readings |

---

## Common Commands

### Virtual Environment
```bash
# Activate
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate        # Windows CMD
.\venv\Scripts\Activate.ps1 # Windows PS

# Deactivate
deactivate

# Delete (if needed)
rm -rf venv    # Linux/Mac
rmdir /s venv  # Windows
```

### Dependencies
```bash
# Install
pip install -r requirements.txt

# List installed
pip list

# Update
pip install --upgrade dash plotly pandas

# Freeze to file
pip freeze > requirements.txt
```

### Running Dashboard
```bash
# Different port
# Edit code: app.run(port=8051)

# Debug mode
# Edit code: app.run(debug=True)
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port in use | `lsof -ti:8050 \| xargs kill -9` |
| pandas build error | `pip install pandas>=2.0.3` |
| Can't activate venv | Check path, use full path |
| Browser can't connect | Check firewall, try localhost |
| Data not updating | Check terminal for errors, restart |

---

## Configuration

**Update Rate:**
```python
# In dashboard file, find:
dcc.Interval(interval=1000)  # ms
# Change to 500 for 0.5s, 2000 for 2s
```

**Buffer Size:**
```python
# In data_gen.py:
deque(maxlen=100)  # points
# Change 100 to keep more data
```

**Colors:**
```python
# In dashboard file:
COLORS = {
    'power': '#3b82f6',  # Change hex codes
    ...
}
```
---

## URLs

- Dashboard: http://127.0.0.1:8050
- Dash Docs: https://dash.plotly.com/
- Plotly Docs: https://plotly.com/python/
- Python Docs: https://docs.python.org/

**Version:** 1.0.0 | **Last Updated:** Nov 9, 2025
