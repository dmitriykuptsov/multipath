from utils import SimulationParams
from numpy.random import uniform
import math

class GenericScheduler():
    def __init__(self, simulationParams = None):
        pass
    def getNextPath(self):
        raise Exception("Not implemented")

class WeightedRoundRobinScheduler(GenericScheduler):
    def __init__(self, simulationParameters = None):
        self.params = simulationParameters
        self.counter = 0
        self.totalBandwidth = 0
        self.batchSize = 0
        self.paths = self.params.getPaths()
        for path in self.paths:
            self.totalBandwidth += path.bandwidth()

        self.cumulativeBatch = []
        i = 0
        for path in self.paths:
            if i == 0:
                self.cumulativeBatch.append(int(self.totalBandwidth / path.bandwidth()))
            else:
                self.cumulativeBatch.append(self.cumulativeBatch[i - 1] + \
                    math.ceil(self.totalBandwidth / path.bandwidth()))
            self.batchSize += int(self.totalBandwidth / path.bandwidth())
            i += 1

    def getNextPath(self):
        self.counter = self.counter % self.batchSize;
        nextPath = None
        for index in range(0, len(self.cumulativeBatch)):
            if self.counter < self.cumulativeBatch[index]:
                nextPath = self.paths[index]
                break;
        self.counter += 1
        return nextPath

class BernoulliScheduler(GenericScheduler):
    def __init__(self, simulationParameters = None):
        self.params = simulationParameters
        self.totalBandwidth = 0
        self.paths = self.params.getPaths()
        for path in self.paths:
            self.totalBandwidth += path.bandwidth()

        self.cumulativeProbs = []
        i = 0
        for path in self.paths:
            if i == 0:
                self.cumulativeProbs.append(path.bandwidth() / self.totalBandwidth)
            else:
                self.cumulativeProbs.append(self.cumulativeProbs[i - 1] + \
                    path.bandwidth() / self.totalBandwidth)
            i += 1

    def getNextPath(self):
        nextPath = None
        prob = uniform(0, 1)
        for index in range(0, len(self.paths)):
            if prob <= self.cumulativeProbs[index]:
                nextPath = self.paths[index]
                break;
        return nextPath

class SchedulerFactory():
    @staticmethod
    def getInstance(params):
        if params.getSchedulerType() == "wrr":
            return WeightedRoundRobinScheduler(params)
        if params.getSchedulerType() == "bn":
            return BernoulliScheduler(params)
        raise Exception("Unsupported scheduler type")
