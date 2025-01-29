import os

if __name__ == "__main__":
    crossbar_size = 1024 
    N_tile = 100
    N_pe = 9
    N_tier = 3   
    f_core = 1
    f_noc = 1
    place_method = 5
    route_method = 2
    router_times_scale = 1
    percent_router = 1
    tsv_pitch = 5
    W2d = 32
    chip_arch = "M3D"
    ai_model = "vit"
    N_stack = 1
    thermal_flag = True

    os.system(f"cd ./submodules/HISIM/HISIM-IMC && python analy_model.py {"--thermal" if thermal_flag else ""} --xbar_size {int(crossbar_size)}\
        --N_stack {int(N_stack)}\
        --N_tile {int(N_tile)}\
        --N_tier {int(N_tier)}\
        --N_pe {int(N_pe)}\
        --freq_computing {float(f_core)}\
        --fclk_noc {float(f_noc)}\
        --placement_method {int(place_method)}\
        --routing_method {int(route_method)}\
        --percent_router {float(percent_router)}\
        --tsvPitch {float(tsv_pitch)}\
        --chip_architect {str(chip_arch)}\
        --W2d {int(W2d)}\
        --router_times_scale {int(router_times_scale)}\
        --ai_model {str(ai_model)}")