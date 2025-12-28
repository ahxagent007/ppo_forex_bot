class RiskManager:
    def __init__(self, balance):
        self.start = balance

    def check(self, balance):
        if (balance - self.start) / self.start < -0.02:
            raise RuntimeError("KILL SWITCH")
