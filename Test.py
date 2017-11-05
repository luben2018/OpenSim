import opensim as osim

generic_MM_Path = 'FullBodyModel\\Rajagopal2015.osim'                 # Path to the Generic Musculoskeletal Model

# Load the generic musculoskeletal model
osimModel = osim.Model(generic_MM_Path)
state = osimModel.initSystem()