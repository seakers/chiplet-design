import numpy as np
import os
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

# Problem definition based on the following, from submodules/HISIM/HISIM-IMC/run.py mode 1

    # crossbar_size=[1024] 
    # N_tile=[64,81,100]
    # N_pe=[36]
    # N_tier=[3]   
    # f_core=[1]
    # f_noc=[1]
    # place_method=[5]
    # route_method=[2]
    # router_times_scale=[1]
    # percent_router=[1]
    # tsv_pitch=[2,3,4,5,10,20] # um
    # W2d=[32]
    # ai_model=['densenet121']
    # chip_arch=["M3D"]
    # N_stack=[1]

# Parameter           Setter Function           Parameter Options
# --chip_architect    set_chip_architecture     Chip Architecture options are 2D chip (M2D), 3D chip (M3D), 2.5D chip (H2_5D), and 3.5D (M3_5D).
# --xbar_size         set_xbar_size             RRAM crossbar sizes are 64, 128, 256, 512, and 1024
# --N_tile            set_N_tile                Number of tiles per tier, with options 4, 9, 16, 25, 36, and 49.
# --N_pe              set_num_pe                Number of processing elements (PEs) per tile, with options 4, 9, 16, 25, and 36.
# --N_crossbar        set_N_crossbar            Number of crossbars per PE, with options 4, 9, and 16.
# --quant_weight      set_quant_weight          Precision of quantized weights of the AI model.
# --quant_act         set_quant_act             Precision of quantized activations of the AI model.
# --freq_computing    set_freq_computing        Clock frequency of the compute core in GHz.
# --fclk_noc          set_fclk_noc              Clock frequency of the network communication unit in GHz.
# --tsvPitch          set_tsv_pitch             3D TSV (Through-Silicon Via) pitch in micrometers (µm).
# --N_tier            set_N_tier                Number of tiers in the chip for 3D architecture.
# --volt              set_volt                  Operating voltage in volts
# --placement_method  set_placement             Placement method options:
#                                               1: Tier/Chiplet Edge to Tier/Chiplet Edge connection
#                                               5: Tile-to-Tile 3D connection
# --routing_method    set_router                Routing method options:
#                                               1: Local routing—uses only nearby routers and TSVs.
#                                               2: Global routing—data will attempt to use all available routers to reach the next tier.
# --percent_router    set_percent_router        Percentage of routers used for 3D communication when data is routed from one tier to the next.
# --W2d               set_W2d                   2D NoC (Network on Chip) bandwidth.
# --router_times_scale  set_router_times_scale  Scaling factor for time components of the router: trc, tva, tsa, tst, tl, tenq.
# --ai_model          set_ai_model              AI models, including vit, gcn, resnet50, resnet110, vgg16, and densenet121.
# --thermal           set_thermal               Set to True to run a thermal simulation; set to False otherwise.
# --N_stack,          set_N_stack               Number of 3D stacks in a 3.5D design or number of chiplets in a 2.5D design.

# Outputs are chosen by my best guess at what two outputs would be useful to optimize for
# since I only want two for now I am going with total system latency and power


class MyProblem(ElementwiseProblem):

    def __init__(self):
        super().__init__(n_var=13,
                         n_obj=2,
                         n_constr=0,
                         xl=np.array([1024, 64, 36, 3, 1, 1, 5, 2, 1, 1, 2, 32, 1]),
                         xu=np.array([1024, 100, 36, 3, 1, 1, 5, 2, 1, 1, 20, 32, 1]))

    def _evaluate(self, x, out, *args, **kwargs):
        crossbar_size, N_stack, N_tile, N_tier, N_pe, f_core, f_noc, place_method, route_method, percent_router, tsv_pitch, W2d, router_times_scale = x
        ai_model = 'densenet121'
        chip_arch = 'M3D'

        os.system('python submodules/HISIM/HISIM-IMC/analy_model.py --xbar_size %d \
            --N_stack %d\
            --N_tile %d \
            --N_tier %d \
            --N_pe %d \
            --freq_computing %f \
            --fclk_noc %f \
            --placement_method %d \
            --routing_method %d\
            --percent_router %f\
            --tsvPitch %f \
            --chip_architect %s\
            --W2d %d\
            --router_times_scale %d\
            --ai_model %s ' %(int(crossbar_size), int(N_stack), int(N_tile),int(N_tier),int(N_pe),float(f_core),float(f_noc),float(place_method),float(route_method),float(percent_router),float(tsv_pitch), str(chip_arch), int(W2d),int(router_times_scale), str(ai_model)))
        
        # Read the output from the file
        with open('Results/PPA.csv', 'r') as file:
            data = file.readlines()
            last_line = data[-1].strip().split(',')
            # power = float(last_line[11])/float(last_line[10])*pow(10,-3) # watts I think
            # print("Power: ", power)
            area = float(last_line[13]) # mm^2
            networkLatency = float(last_line[18]) # ns
            print("Area: ", area)
            print("Network Latency: ", networkLatency)
            out["F"] = [area, networkLatency]
            print("Output Numbers: ", out["F"])

problem = MyProblem()

algorithm = NSGA2(pop_size=10)

res = minimize(problem,
               algorithm,
               ("n_gen", 5),
               verbose=True)

plot = Scatter()
plot.add(res.F, color="red")
plot.save("Results/output.png")