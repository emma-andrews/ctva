# Configuration File
# Change values appropriately
# For relative pathing, please use relative to this file and main.py
# (config.py and main.py must be in the same directory)

#########
# Files #
#########
verilog_source = "verilog_samples/reduction.v"

#############
# Registers #
#############
state_reg = "state"
init_state = "WAIT"
end_state = "DONEOUT"

###################
# Operation Costs #
###################
# Values in number of clock cycles
# Note: this config.py uses arbitrary clock cycles but ratioed between operations correctly.
# In most hardware, certain operations have the same computation time as others, where indicated
add_cost = 10
sub_cost = add_cost
mult_cost = 20 + add_cost # cost of multiplication = cost of true multiplication + cost of addition
div_cost = 50 # Pure division operation, if able to shift instead of divide use shift_cost
shift_cost = 10
mod_cost = div_cost + add_cost
exp_cost = mult_cost * mult_cost
bitand_cost = 5 # Bitwise operations, not logical. Logical do not take a clock cycle to process
bitor_cost = 5
bitxor_cost = 5
bitnot_cost = 5

####################
# Graphing Options #
####################
# Note: you will need to have an X-server display configured and running 
# for the graph options to work.
# Please see matplotlib documentation for further reference.
display_graph = False
save_graph = False