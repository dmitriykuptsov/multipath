import argparse
import sys
from utils import ParamsParser
from utils import Packet, Path, Analyzer
from scheduler import SchedulerFactory
import numpy as np
from time import time

# Set the seed so that the parameters are the same for both BN and WRR simulators
np.random.seed(1)

parser = argparse.ArgumentParser(description='Multipath simulator')
parser.add_argument('--file',  help='Simulation parameters')
args = parser.parse_args()
if args.file == None:
    parser.print_help()
    sys.exit(0)

simulationParameters = ParamsParser(args.file)
for idx in range(0, simulationParameters.getNumberOfSimulations()):
    params = simulationParameters.getSimulationParams(idx)
    reorderDistance = []
    for roundIndex in range(0, params.getNumRounds()):
        scheduler = SchedulerFactory.getInstance(params);
        packets = [];
        s = time()
        for packetIndex in range(0, params.getNumPackets()):
            path = scheduler.getNextPath()
            delay = path.getDelay()
            packet = Packet(packetIndex, path.getLastTimestamp() + delay, path.pathIndex())
            path.setLastTimestamp(path.getLastTimestamp() + delay)
            packets.append(packet)
        
        analyzer = Analyzer(packets)
        avgReorderingDistance = analyzer.computeReorderingDistance()
        reorderDistance.append(avgReorderingDistance)
        e = time()
        #print((e-s))
    print(params.getNumPaths(), np.mean(reorderDistance), np.std(reorderDistance))
