class SCC:
    def __init__(self):
        # Inputs
        self.pv_power = 0                # Power from solar panels [W]
        self.light_power = 0             # Current power level of light [W]
        self.heatpump_power = 0          # Current power level of heat pump [W]
        self.battery_voltage = 0         # Battery voltage [V]
        self.battery_temperature = 0     # Battery temperature [°C]

        # Output (suggestion dict)
        self.suggestion = {}

        # Internal state
        self.can_discharge = True  # Initially allowed to discharge

    # Setters for external updates
    def set_PV(self, power_watts):
        self.pv_power = power_watts

    def set_LightLevel(self, power_watts):
        self.light_power = power_watts

    def set_HeatpumpLevel(self, power_watts):
        self.heatpump_power = power_watts

    def set_BatVoltage(self, voltage):
        self.battery_voltage = voltage
        self._update_discharge_status()

    def set_BatTemp(self, temperature):
        self.battery_temperature = temperature

    # Internal helper
    def _update_discharge_status(self):
        if self.battery_voltage < 47.0:
            self.can_discharge = False
        elif self.battery_voltage >= 51.0:
            self.can_discharge = True

    # Main logic
    def suggest(self):
        s = {}

        # Determine whether charging/discharging is allowed
        charge_allowed = 0 <= self.battery_temperature <= 45 and self.battery_voltage < 55.1
        discharge_allowed = -25 <= self.battery_temperature <= 65 and self.can_discharge and self.battery_voltage > 47.0

        # Charging logic
        if charge_allowed and self.pv_power > 0:
            # Max battery charging power: 3000 W or limited by PV
            s['BAT'] = min(3000, self.pv_power)
        else:
            s['BAT'] = 0

        # Light injector logic
        light_demand = abs(self.light_power)
        if discharge_allowed:
            if light_demand > 900:
                s['LightInjector1'] = True
                s['LightInjector2'] = True
                s['Light'] = 1800
            elif light_demand > 0:
                s['LightInjector1'] = True
                s['LightInjector2'] = False
                s['Light'] = 900
            else:
                s['LightInjector1'] = False
                s['LightInjector2'] = False
                s['Light'] = 0
        else:
            s['LightInjector1'] = False
            s['LightInjector2'] = False
            s['Light'] = 0

        # Heatpump injector logic
        heat_demand = abs(self.heatpump_power)
        if discharge_allowed and heat_demand > 0:
            s['HPInjector'] = True
            s['HP'] = min(400, heat_demand)
        else:
            s['HPInjector'] = False
            s['HP'] = 0

        # Battery heater logic
        s['BATHEAT'] = self.battery_temperature < 0  # Turn on heater if too cold

        self.suggestion = s
        return s
