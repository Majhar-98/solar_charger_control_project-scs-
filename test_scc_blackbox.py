import unittest
import sys, os
sys.path.append(os.path.abspath("."))

from scc import SCC

class TestSCCBlackBox(unittest.TestCase):
    def setUp(self):
        self.scc = SCC()

    # Expected to PASS
    def test_valid_charge(self):
        self.scc.set_PV(1500)
        self.scc.set_BatVoltage(50)
        self.scc.set_BatTemp(25)
        self.assertGreater(self.scc.suggest()['BAT'], 0)

    def test_charge_blocked_temp_high(self):
        self.scc.set_PV(1500)
        self.scc.set_BatTemp(50)
        self.scc.set_BatVoltage(50)
        self.assertEqual(self.scc.suggest()['BAT'], 0)

    def test_charge_blocked_voltage_high(self):
        self.scc.set_PV(1500)
        self.scc.set_BatTemp(25)
        self.scc.set_BatVoltage(56)
        self.assertEqual(self.scc.suggest()['BAT'], 0)

    def test_light_both_on(self):
        self.scc.set_LightLevel(1500)
        self.scc.set_BatVoltage(52)
        self.scc.set_BatTemp(25)
        output = self.scc.suggest()
        self.assertTrue(output['LightInjector1'])
        self.assertTrue(output['LightInjector2'])

    def test_hp_limited(self):
        self.scc.set_HeatpumpLevel(500)
        self.scc.set_BatVoltage(52)
        self.scc.set_BatTemp(25)
        self.assertEqual(self.scc.suggest()['HP'], 400)

    def test_heater_on_below_zero(self):
        self.scc.set_BatTemp(-2)
        self.assertTrue(self.scc.suggest()['BATHEAT'])

    # Expected to FAIL
    def test_charge_fails_wrong_temp(self):
        self.scc.set_PV(1500)
        self.scc.set_BatTemp(45)
        self.scc.set_BatVoltage(50)
        self.assertEqual(self.scc.suggest()['BAT'], 0)  # should pass, but actually charges

    def test_light_fail_when_voltage_low(self):
        self.scc.set_LightLevel(1200)
        self.scc.set_BatVoltage(45)  # < 47V
        self.scc.set_BatTemp(25)
        self.assertTrue(self.scc.suggest()['LightInjector1'])  # should fail

    def test_hp_off_should_fail(self):
        self.scc.set_HeatpumpLevel(200)
        self.scc.set_BatVoltage(46)  # discharge not allowed
        self.scc.set_BatTemp(25)
        self.assertNotEqual(self.scc.suggest()['HP'], 0)  # fails

    def test_heater_off_expected_fail(self):
        self.scc.set_BatTemp(5)
        self.assertTrue(self.scc.suggest()['BATHEAT'])  # should be False

    def test_light_level_zero_should_fail(self):
        self.scc.set_LightLevel(0)
        self.scc.set_BatVoltage(52)
        self.scc.set_BatTemp(25)
        self.assertGreater(self.scc.suggest()['Light'], 0)

    def test_hp_limited_fail(self):
        self.scc.set_HeatpumpLevel(300)
        self.scc.set_BatVoltage(46)
        self.scc.set_BatTemp(25)
        self.assertEqual(self.scc.suggest()['HP'], 300)  # Should be 0

    def test_invalid_charge_check(self):
        self.scc.set_PV(0)
        self.scc.set_BatVoltage(52)
        self.scc.set_BatTemp(25)
        self.assertGreater(self.scc.suggest()['BAT'], 0)  # should fail

    def test_light_on_wrong_temp(self):
        self.scc.set_LightLevel(1200)
        self.scc.set_BatVoltage(52)
        self.scc.set_BatTemp(70)  # discharge blocked
        self.assertGreater(self.scc.suggest()['Light'], 0)

    def test_discharge_below_47_still_allowed(self):
        self.scc.set_BatVoltage(46)
        self.scc.set_LightLevel(1200)
        self.scc.set_BatTemp(25)
        self.assertTrue(self.scc.suggest()['LightInjector1'])

    def test_temp_above_limit_still_charge(self):
        self.scc.set_BatTemp(46)
        self.scc.set_BatVoltage(50)
        self.scc.set_PV(1000)
        self.assertGreater(self.scc.suggest()['BAT'], 0)

    def test_valid_charge_but_fails(self):
        self.scc.set_BatTemp(25)
        self.scc.set_BatVoltage(50)
        self.scc.set_PV(1500)
        self.assertEqual(self.scc.suggest()['BAT'], 0)

    def test_light_injection_should_be_two(self):
        self.scc.set_LightLevel(1200)
        self.scc.set_BatVoltage(52)
        self.scc.set_BatTemp(25)
        self.assertFalse(self.scc.suggest()['LightInjector2'])

    def test_no_light_expected_fail(self):
        self.scc.set_LightLevel(0)
        self.scc.set_BatVoltage(52)
        self.scc.set_BatTemp(25)
        self.assertTrue(self.scc.suggest()['LightInjector1'])

if __name__ == "__main__":
    unittest.main()
