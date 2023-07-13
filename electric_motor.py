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

    NOTE:
        - introduce units to the calculations to make the simulation more coherent with
            the real world
        - define a maximum power to scale the percentual power accordingly
        - get the thermodynamics sorted.
        - if the thermodynamics are sorted, the control can be examined to
            detect futher errors in the code.
    """
    def __init__(self,init_temperature: int, volume_reservoir: int) -> None:
        self.temperature = init_temperature
        self.volume_reservoir = volume_reservoir
        self.current_heat_in_system = 14300*volume_reservoir*(init_temperature)
        self.current_heat_balance = 0
        self.max_power = 200 # kW

    def step(self, thrust, fluidflow, fluid_temperature) -> None:
        """
        handles the fluid dynamics, maybe include motor heat loss depending on current heat
        inputs:
            thrust:             thrust value to estimate the heat generated in the motor
            fluidflow:          the amount of cooling fluid
            fluid_temperature:  the temperature of the fluid in K
        returns:
            self.temperature:   the current temperature in the heat reservoir
        """

        # assuming constant specific heat
        # assuming the excess mass will just be emitted out of the motor
        C_HYDR = 14300 #J/(kgK)
        efficiency = .98
        # heat motor due to thrust
        # TODO: introduce loss of @efficiency due to higher temperature (look up graph)
        current_power_output = self.max_power*thrust
        current_heat_produced = (1 - efficiency)*current_power_output

        # fluidflow in kg/s
        # fluid_temperature in K
        # self.temperature in K
        # cooling is C*m*(T_2-T_1) since c=c and m=m T_in_system > T_input
        current_heat_cooled = C_HYDR*fluidflow*(self.temperature-fluid_temperature)
        current_heat_balance = current_heat_produced-current_heat_cooled
        self.current_heat_balance = current_heat_balance
        self.current_heat_in_system += current_heat_balance
        self.temperature = self.current_heat_in_system/(self.volume_reservoir*C_HYDR)
        return self.temperature
