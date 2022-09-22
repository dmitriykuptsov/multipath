from delays import GenericDelay
from delays import DelayFactory

class Analyzer():
    def __init__(self, packets):
        self.packets = packets
        self.sequence = self.__sort__()
    def __sort__(self):
        output = []
        ts = []
        for idx1 in range(0, len(self.packets)):
            for idx2 in range(0, len(self.packets)):
                if self.packets[idx1].arrivalTimestamp < self.packets[idx2].arrivalTimestamp:
                    tmp = self.packets[idx1]
                    self.packets[idx1] = self.packets[idx2]
                    self.packets[idx2] = tmp
        for idx in range(0, len(self.packets)):
            output.append(self.packets[idx].sequence)
            ts.append(self.packets[idx].arrivalTimestamp)
        return output
    
    def computeReorderingDistance(self):
        cumulative = 0
        for i in range(0, len(self.sequence) - 2):
            maxrm = 0
            for j in range(i + 1, len(self.sequence)):
                if self.sequence[i] > self.sequence[j]:
                    rm = j - i
                    if rm > maxrm:
                        maxrm = rm
            cumulative += maxrm
        return cumulative / len(self.sequence)

    def getSequence(self):
        return self.sequence

class Path():
    def __init__(self, index, distribution, args):
        self.index = index;
        self.distribution = distribution;
        self.delay = DelayFactory.get(distribution, args)
        self.lastTimestamp = 0
    def pathIndex(self):
        return self.index;
    def bandwidth(self):
        return 1.0/self.delay.mean()
    def delayMean(self):
        return self.delay.mean()
    def getDelay(self):
        return self.delay.generate()
    def getLastTimestamp(self):
        return self.lastTimestamp
    def setLastTimestamp(self, ts):
        self.lastTimestamp = ts

class Packet():
    def __init__(self, sequence, arrivalTimestamp, pathIndex):
        self.sequence = sequence
        self.arrivalTimestamp = arrivalTimestamp
        self.pathIndex = pathIndex
    
class SimulationParams():
    def __init__(self, numRounds = 1000, numPackets = 1000, numPaths = 2, scheduler = "wrr", distribution = "exponential", distributionParams = [0.3, 0.3]):
        self.numRounds = numRounds
        self.numPackets = numPackets
        self.numPaths = numPaths
        self.distribution = distribution
        self.distributionParams = distributionParams
        self.scheduler = scheduler
        self.paths = [];
    def getNumPackets(self):
        return self.numPackets
    def getNumRounds(self):
        return self.numRounds
    def getNumPaths(self):
        return self.numPaths
    def getDistribution(self):
        return self.distributionParams
    def getSchedulerType(self):
        return self.scheduler
    def getPaths(self):
        if len(self.paths) > 0:
            return self.paths
        for i in range(0, self.numPaths):
            self.paths.append(Path(i, self.distribution, self.distributionParams))
        return self.paths

class ParamsParser():
    def __init__(self, file):
        self.maxSimulations = 0
        self.simulations = [];

        with open(file) as fd:
            lines = fd.readlines();
            c = 0
            numPaths = 2
            numRounds = 1000
            numPackets = 1000
            distribution = "exponential"
            schedulerType = "wrr"
            args = []
            for line in lines:
                if c % 2 == 0:
                    p = line.split(" ")
                    numPaths = int(p[0])
                    numRounds = int(p[1])
                    numPackets = int(p[2])
                else:
                    p = line.split(" ")
                    distribution = p[0]
                    schedulerType = p[1]
                    for i in range(2, len(p)):
                        args.append(float(p[i]))
                c += 1
                if c % 2 == 1:
                    self.simulations.append(SimulationParams(numRounds, numPackets, numPaths, schedulerType, distribution, args))
    def getNumberOfSimulations(self):
        return len(self.simulations)
    def getSimulationParams(self, index):
        return self.simulations[index]