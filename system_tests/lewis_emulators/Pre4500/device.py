from collections import OrderedDict

from lewis.devices import StateMachineDevice

from .states import DefaultState


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

        self._chan1 = 0
        self._chan2 = 0
        self._chan3 = 0
        self._chan4 = 0

        self.error = "0"

    def _get_state_handlers(self):
        """
        Returns: states and their names
        """
        return {DefaultState.NAME: DefaultState()}

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
    def chan1(self):
        """
        Get current temperature of the device.

        Returns: the current temperature in K.
        """
        self._delay()
        return self._chan1

    @chan1.setter
    def chan1(self, temp):
        """
        Set the current temperature of the device.

        Args:
            temp: the current temperature of the device in K.

        """
        self._chan1 = int(temp)

    @property
    def chan2(self):
        """
        Get current temperature of the device.

        Returns: the current temperature in K.
        """
        self._delay()
        return self._chan2

    @chan2.setter
    def chan2(self, temp):
        """
        Set the current temperature of the device.

        Args:
            temp: the current temperature of the device in K.

        """
        self._chan2 = int(temp)

    @property
    def chan3(self):
        """
        Get current temperature of the device.

        Returns: the current temperature in K.
        """
        self._delay()
        return self._chan3

    @chan3.setter
    def chan3(self, temp):
        """
        Set the current temperature of the device.

        Args:
            temp: the current temperature of the device in K.

        """
        self._chan3 = int(temp)

    @property
    def chan4(self):
        """
        Get current temperature of the device.

        Returns: the current temperature in K.
        """
        self._delay()
        return self._chan4

    @chan4.setter
    def chan4(self, temp):
        """
        Set the current temperature of the device.

        Args:
            temp: the current temperature of the device in K.

        """
        self._chan4 = int(temp)
