from numpy.random import exponential
from numpy.random import uniform
from numpy.random import pareto

class GenericDelay():

    def __init__(self, *args):
        pass

    def generate(self):
        return 0;

    def mean(self):
        return 0

class ExponentialDelay(GenericDelay):

    def __init__(self, args):
        self.lambda_ = uniform(args[0], args[1]);
        self.scale = 1.0/self.lambda_

    def generate(self):
        return exponential(self.scale)

    def mean(self):
        return self.scale
    
class UniformDelay(GenericDelay):

    def __init__(self, args):
        self.a = uniform(args[0], args[1]);
        self.b = uniform(args[2], args[3]);

    def generate(self):
        return uniform(self.a, self.b)

    def mean(self):
        return (self.a + self.b)/2

class ParetoDelay(GenericDelay):
    def __init__(self, args):
        self.a = uniform(args[0], args[1])
        self.m = uniform(args[2], args[3])

    def generate(self):
        return (np.random.pareto(self.a, 1) + 1) * self.m

    def mean(self):
        if self.a <= 1:
            return inf
        return self.a * self.m / (self.a - 1)

class DelayFactory():
    @staticmethod
    def get(distribution, args):
        if distribution == "pareto":
            return ParetoDelay(args)
        if distribution == "uniform":
            return UniformDelay(args)
        if distribution == "exponential":
            return ExponentialDelay(args)
        raise Exception("Not supported distribution")

