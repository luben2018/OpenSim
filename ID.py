import opensim as osim
import numpy as np
import os

# # Inverse Dynamics(ID) with python

# DataBase
dir_path = 'C:\\Users\\SeriouslyJapan\\Desktop\\OpenSim-master\\'

scaled_MM_Moved_path = dir_path + 'FullBodyModel\\SubjectMoved.osim'                                                   # Path to the subject Musculoskeletal Model that will be created

XML_generic_ID_path = dir_path + 'XML\\ID.xml'                                                                         # Path to the generic ID XML file
XML_generic_External_Load_ID_path = dir_path + 'XML\\External_Load_ID.xml'                                             # Path to the generic external load ID XML file

MOT_files = np.array([dir_path + 'MOT\\Walk_Mkrs.mot', dir_path + 'MOT\\Walk_Mkrs2.mot', dir_path + 'MOT\\Walk_Mkrs3.mot'])                  # Path to the .mot files that contain the marker data
PFF_MOT_files = np.array([dir_path + 'PFF_MOT\\walk1.mot', dir_path + 'PFF_MOT\\walk2.mot', dir_path + 'PFF_MOT\\walk3.mot'])                # Path to the .mot files that contain the marker data

# Musculoskeletal model
osimModel = osim.Model(scaled_MM_Moved_path)
state = osimModel.initSystem()

i = 0
MOT_file = MOT_files[i]
PFF_MOT_file = PFF_MOT_files[i]

path, filename = os.path.split(MOT_file)
filename, ext = os.path.splitext(filename)

STO_file = filename + '.sto'                                      # Path to the output .MOT file that will be created and contain the IK results
XML_ID_file = dir_path + 'XML\\' + filename + '_ID.xml'                                  # Path to the ID XML file that will be created
XML_External_Load_ID_file = dir_path + 'XML\\' + filename + '_External_Load_ID.xml'      # Path to the External Load ID XML file that will be created

# Mot Data
motData = osim.Storage(MOT_file)
initial_time = motData.getFirstTime()
final_time = motData.getLastTime()

# ID tool
####################################################





####################################################

# External Load File
externalLoads = osim.ExternalLoads(osimModel, XML_generic_External_Load_ID_path)
externalLoads.setName(filename)
externalLoads.setDataFileName(PFF_MOT_file)                                         # Set the PFF MOT filename
externalLoads.setLowpassCutoffFrequencyForLoadKinematics(4)

# External Force
####################################################





####################################################

# Set the external load file in the ID tool
idTool.setExternalLoadsFileName(XML_External_Load_ID_file)

# Create a subject specific ID xml and print it
idTool.printToXML(XML_ID_file)

idTool.run() # Run ID
print('STO files : ' + dir_path + STO_file + ' created')