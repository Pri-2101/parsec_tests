from gem5.components.boards.simple_board import SimpleBoard
from gem5.coherence_protocol import CoherenceProtocol

from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import PrivateL1PrivateL2CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import *
from gem5.simulate.simulator import Simulator
from gem5.resources.workload import CustomWorkload

import m5
from m5.objects import *

# Change this path according to your installation | (basically adding the "gem5/configs" to the path)
#                                                 v
m5.util.addToPath("gem5/configs/")
from common.FileSystemConfig import config_filesystem


from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)

cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="32kB",
    l1d_assoc=8,
    l1i_size="32kB",
    l1i_assoc=8,
    l2_size="256kB",
    l2_assoc=16,
    num_l2_banks=2
)

memory = SingleChannelDDR3_1600("16GiB")

# AtomicSimpleCPU
#processor = SimpleProcessor(isa=ISA.X86,cpu_type=CPUTypes.ATOMIC, num_cores=1)
# TimingSimpleCPU
#processor = SimpleProcessor(isa=ISA.X86,cpu_type=CPUTypes.TIMING, num_cores=1)
# O3CPU
processor = SimpleProcessor(isa=ISA.X86,cpu_type=CPUTypes.O3, num_cores=2)

# flag for fuzzing the TSC
#processor.cores[0].core.isa[0].fuzz_TSC = True

# flag for delaying control-speculative loads
#processor.cores[0].core.delayCtrlSpecLoad= False
# flag for delaying tainted load
#processor.cores[0].core.delayTaintedLoad= False

#processor.cores[0].core.max_insts_any_thread=250000000

# Add them to the board
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
    )

# Compilation code ->  g++ false_sharing.cpp -o false_sharing.g++ -pthread
# Add the above binary file's path down here |
#                                            v
#MEANT FOR NATIVE MACHINE
#non-triggering
#binary = CustomResource("/home/pritheshwar/Desktop/parsec_tests/false_sharing_tests/bin/native_false_sharing_non_triggering.g++");
#triggering
#binary = CustomResource("/home/pritheshwar/Desktop/parsec_tests/false_sharing_tests/bin/native_false_sharing_triggering.g++");

#MEANT FOR GEM5
#non-triggering
#binary = CustomResource("/home/pritheshwar/Desktop/parsec_tests/false_sharing_tests/bin/gem5_false_sharing_non_triggering.g++");
#triggering
binary = CustomResource("/home/pritheshwar/Desktop/parsec_tests/false_sharing_tests/bin/gem5_false_sharing_triggering.g++");

board.set_se_binary_workload(binary)

#board.set_se_binary_workload(
#    binary = CustomResource("../spec2006/gcc/gcc_base.x86_64_sse"),
#    arguments = ["../spec2006/gcc/input/scilab.i", "-o scilab.o"],
#    )

simulator = Simulator(board=board)

print ("Beginning simulation!")
simulator.run()

