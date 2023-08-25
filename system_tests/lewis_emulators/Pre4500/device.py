from collections import OrderedDict
from .states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedPre4500(StateMachineDevice):

    """
    Simulated PRE4500 temperature sensor.
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """
        self.connected = True
        self.delay_time = None

        self._spare_temperature = 0
        self._chopper_body = 0
        self._cooling_water = 0
        self._chopper_pit = 0
        
        self.error = "0"

    def _get_state_handlers(self):
        """
        Returns: states and their names
        """
        return {
            DefaultState.NAME: DefaultState()
        }

    def _get_initial_state(self):
        """
        Returns: the name of the initial state
        """
        return DefaultState.NAME

    def _get_transition_handlers(self):
        """
        Returns: the state transitions
        """
        return OrderedDict()
    
    def _delay(self):
        """
        Simulate a delay.
        """
        if self.delay_time is not None:
            sleep(self.delay_time)


    @property
    def spare_temperature(self):
        """
        Get current temperature of the device.

        Returns: the current temperature in K.
        """
        self._delay()
        return self._spare_temperature

    @spare_temperature.setter
    def spare_temperature(self, temp):
        """
        Set the current temperature of the device.

        Args:
            temp: the current temperature of the device in K.

        """
        self._spare_temperature = int(temp)

    @property
    def chopper_body(self):
        """
        Get current temperature of the device.

        Returns: the current temperature in K.
        """
        self._delay()
        return self._chopper_body

    @chopper_body.setter
    def chopper_body(self, temp):
        """
        Set the current temperature of the device.

        Args:
            temp: the current temperature of the device in K.

        """
        self._chopper_body =  int(temp)

    @property
    def cooling_water(self):
        """
        Get current temperature of the device.

        Returns: the current temperature in K.
        """
        self._delay()
        return self._cooling_water

    @cooling_water.setter
    def cooling_water(self, temp):
        """
        Set the current temperature of the device.

        Args:
            temp: the current temperature of the device in K.

        """
        self._cooling_water =  int(temp)

    @property
    def chopper_pit(self):
        """
        Get current temperature of the device.

        Returns: the current temperature in K.
        """
        self._delay()
        return self._chopper_pit

    @chopper_pit.setter
    def chopper_pit(self, temp):
        """
        Set the current temperature of the device.

        Args:
            temp: the current temperature of the device in K.

        """
        self._chopper_pit =  int(temp)

