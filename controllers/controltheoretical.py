from .controller import Controller

MAX_SCALE_OUT_TIMES = 3
MIN_CORES = 0.001
MAX_CORES = 10.0

class CTControllerScaleX(Controller):
    def __init__(self, period, init_cores, BC=0.5, DC=0.95, st=0.5, min=MIN_CORES, max=MAX_CORES):
        super().__init__(period, init_cores, st=st)
        self.BC = BC
        self.DC = DC
        self.cores = init_cores  # new Inacio
        self.min = min
        self.max = max

    def reset(self):
        super().reset()
        self.xc_prec = 0

    def control(self, t):
        # getTotalRT() for Neptune and getRT for dependences
        rt = self.monitoring.getTotalRT()
        self.rt = rt
        e = 1 / self.setpoint - 1 / rt
        # print('STControllerTheory-', self.setpoint)
        self.e = e
        xc = float(self.xc_prec + self.BC * e)
        oldcores = self.cores
        self.cores = min(self.max, min(max(max(self.min, oldcores/MAX_SCALE_OUT_TIMES), xc + self.DC * e), oldcores*MAX_SCALE_OUT_TIMES))
        # print('st/Cores/RT=', self.setpoint, '/', self.cores, '/', rt)
        if t < 50:
            self.cores = self.init_cores
            print(self.cores)
        else:
            print(t)
        self.xc_prec = float(self.cores - self.BC * e)
    

    def __str__(self):
        return super().__str__() + " BC: %.2f DC: %.2f " % (self.BC, self.DC)
