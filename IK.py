import opensim as osim
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

# DataBase
scaled_MM_Moved_path = 'FullBodyModel\\SubjectMoved.osim'  # Path to the subject Musculoskeletal Model that will be created

TRC_files = np.array(['TRC\\Walk_Mkrs.trc', 'TRC\\Walk_Mkrs2.trc', 'TRC\\Walk_Mkrs3.trc'])
print(TRC_files)
print(TRC_files[0])
print(TRC_files[1])
print(TRC_files[2])

XML_generic_IK_path = 'XML\IK.xml' # Path to the generic IK XML file

markerList = np.array(['RSHO', 'LSHO', 'C7', 'STRN', 'RELB', 'RWRA',
                       'RWRB', 'LELB', 'LWRA', 'LWRB', 'RASI', 'LASI', 'RPSI',
                       'LPSI', 'RTHI', 'RKNE', 'INRKNE', 'RTIB', 'RANK',
                       'RHEE', 'RTOE', 'RPINKY', 'LTHI', 'LKNE', 'INLKNE',
                       'LTIB', 'LANK', 'LHEE', 'LTOE', 'LPINKY', 'T10', 'CLAV', 'LFIN', 'RFIN'])

markerWeight = np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
print(markerWeight)

# Launch the musculoskeletal model
##################################
osimModel = osim.Model(scaled_MM_Moved_path)
state = osimModel.initSystem()
##################################

i = 0
TRC_file = TRC_files[i]

path, filename = os.path.split(TRC_file)
filename, ext = os.path.splitext(filename)

MOT_file = 'MOT\\' + filename + '.mot'                                # Path to the output .MOT file that will be created and contain the IK results
XML_IK_file = 'XML\\' + filename + '_IK.xml'                          # Path to the IK XML file that will be created

# Marker Data
##################################
markerData = osim.MarkerData(TRC_file)
initial_time = markerData.getStartFrameTime()
final_time = markerData.getLastFrameTime()
##################################

# Set the IK tool
##################################
ikTool = osim.InverseKinematicsTool(XML_generic_IK_path)
ikTool.setModel(osimModel)
ikTool.setName(filename + ext)
ikTool.setMarkerDataFileName(TRC_file)
ikTool.setStartTime(initial_time)
ikTool.setEndTime(final_time)
ikTool.setOutputMotionFileName(MOT_file)
##################################

# For loop demo
for j in range(0, 10):
    print(j)

# Set the ikTool with the MarkerTask
for j in range(0, markerList.shape[0]):
    ikMarkerTask = osim.IKMarkerTask()
    ikMarkerTask.setName(markerList[j])
    ikMarkerTask.setApply(1)
    ikMarkerTask.setWeight(markerWeight[j])
    ikTool.getIKTaskSet().adoptAndAppend(ikMarkerTask)

# Create the IK XML file
ikTool.printToXML(XML_IK_file)
ikTool.run()