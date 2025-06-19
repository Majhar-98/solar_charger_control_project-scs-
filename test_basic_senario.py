from scc import SCC

def test_basic_scenario():
    scc = SCC()

    # Set inputs (simulate a sunny day with active usage)
    scc.set_PV(1800)               # Solar power available
    scc.set_LightLevel(1000)       # Lights using power
    scc.set_HeatpumpLevel(300)     # Heat pump is on
    scc.set_BatVoltage(52.5)       # Mid battery level
    scc.set_BatTemp(20)            # Normal temperature

    # Get control suggestion
    suggestion = scc.suggest()

    print("SCC Suggestion:")
    for k, v in suggestion.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    test_basic_scenario()
