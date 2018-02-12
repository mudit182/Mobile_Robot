class PID:
    def __init__(self, Kp, Ki, Kd):
        self.E = 0
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def getRateOfChange(self, error, timeElapsed):
        if not timeElapsed == 0:
            self.e = error
            self.E += self.e * timeElapsed
            self.de = self.e / timeElapsed
            return (self.Kp * self.e) + (self.Ki * self.E) + (self.Kd * self.de)
        else:
            return 0

    def reset(self):
        self.E = 0
