"""
this module should offer all capabilities of the simulated electric motor.
"""

class Motor():
    """
    simulation of the heat in an electric motor being cooled by a fluid cooling
    medium.
    inputs:
        init_temperature:   the inital temperature of the motor
        volume_reservoire:  the volume of the fluid being in the motor
    returns:
        Motor
    """
    def __init__(self,init_temperature: int, volume_reservoir: int) -> None:
        self.temperature = init_temperature
        self.volume_reservoir = volume_reservoir

    def step(self, thrust, fluidflow, fluidtemperature) -> None:
        """
        handles the fluid dynamics, maybe include motor heat loss depending on current heat
        inputs:
            thrust:             thrust value to estimate the heat generated in the motor
            fluidflow:          the fluid flow of the cooling medium
            fluidtemperature:   the temperature of the cooling medium
        returns:
            nothing, just adjusts the motor values
        """
        # assuming constant specific heat
        # assuming the excess mass will just be emitted out of the motor
