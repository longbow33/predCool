class PID():
    def __init__(self,kP = 1, kI = 0, kD = 0) -> None:
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.I = 0

    def step(self, target, actual):
        diff = actual-target
        self.I += diff
        to_return = (self.kP*diff)+(self.kI*self.I)
        return to_return