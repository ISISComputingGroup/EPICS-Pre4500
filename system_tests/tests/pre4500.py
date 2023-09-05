import unittest

from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir, IOCRegister
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc, skip_if_recsim


DEVICE_PREFIX = "PRE4500_01"


IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("PRE4500"),
        "macros": {},
        "emulator": "Pre4500",
    },
]


TEST_MODES = [TestModes.DEVSIM]

TEMP_PROBE = ["SPARE:TEMP", "CHOPPER:BODY:TEMP", "COOLING:WATER:TEMP","CHOPPER:PIT:TEMP"]
TEMP_PROBE_EMULATOR = ["spare_temperature", "chopper_body", "cooling_water", "chopper_pit"]

class Pre4500Tests(unittest.TestCase):
    """
    Tests for the Pre4500 IOC.
    """
    def setUp(self):
        self._setup_lewis_and_channel_access()
        self._reset_device_state()

    def _setup_lewis_and_channel_access(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc("Pre4500", DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX)
        self._reset_device_state()

    def _reset_device_state(self):
        self._lewis.backdoor_set_on_device('connected', True)
        intial_temp = 0.0
        self._set_current_temperature(intial_temp, TEMP_PROBE, TEMP_PROBE_EMULATOR)

    def _set_current_temperature(self, temperature, TEMP_PROBE, TEMP_PROBE_EMULATOR):
        for probe_position in range(len(TEMP_PROBE)):
                self._lewis.backdoor_set_on_device(TEMP_PROBE_EMULATOR[probe_position], temperature)
                self.ca.assert_that_pv_is_number(TEMP_PROBE[probe_position], temperature/10)  #these temperatures are then divide by 10 to see if they match

    @skip_if_recsim("Lewis backdoor not available in recsim")
    def test_GIVEN_temperature_set_on_device_WHEN_reading_temperature_THEN_temperature_readback_matches(self): 
        expected_temperature = [100, 200, 300, 400] #these temperatures are scaled by 10 as the input for the emulator has to be a integer, and are multipled by 0.1 within the IOC
        for probe_position in range(len(TEMP_PROBE)):
            self._set_current_temperature(expected_temperature[probe_position], TEMP_PROBE, TEMP_PROBE_EMULATOR)
            self.ca.assert_that_pv_is(TEMP_PROBE[probe_position], expected_temperature[probe_position]/10.0) #these temperatures are then divide by 10 to see if they match
        
