# Solar Charger Controller (SCC):
This project simulates a Solar Charger Controller (SCC) that provides smart control suggestions for managing power distribution between solar panels, batteries, lighting systems, and a heat pump, based on various environmental and system parameters.

# Project Structure
├── scc.py                   # Main SCC logic
├── test_basic_senario.py   # Basic functional test
├── test_scc_blackbox.py    # Black-box testing
├── test_scc_whitebox.py    # White-box testing
└── README.md               # Project overview

# Features
- Intelligent charging based on PV power, battery voltage, and temperature
- Light and heat pump control logic with injector states
- Battery heater activation logic when temperature falls below 0°C
- Modular and testable design using Python classes

# 🧪 Testing
# 1. Basic Scenario
  python test_basic_senario.py
# 2. Black-box Tests
  python -m unittest test_scc_blackbox.py
# 3. White-box Tests

# 📌 Requirements
Python 3.x

# 🧠 How It Works
The core controller logic is implemented in SCC.suggest(), which evaluates inputs like:
- PV Power
Light demand
Heat pump demand
Battery voltage and temperature
And then outputs a dictionary with control suggestions like:
BAT – battery charge amount
LightInjector1, LightInjector2 – light injection states
HPInjector – heat pump activation
BATHEAT – battery heater status

