import opensim as osim

dir_path = 'D:\Google Drive\Share to the world\GitHub\OpenSim_Python'

generic_MM_Path = dir_path + '\\FullBodyModel\\Rajagopal2015.osim'                 # Path to the Generic Musculoskeletal Model

# Load the generic musculoskeletal model
osimModel = osim.Model(generic_MM_Path)
state = osimModel.initSystem()

