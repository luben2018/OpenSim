import opensim as osim
import numpy as np

dir_path = 'D:\\Google Drive\\Share to the world\\GitHub\\OpenSim'                                                      # Change the path to the location of you openSim project

generic_MM_Path = dir_path + '\\FullBodyModel\\Rajagopal2015.osim'                 # Path to the Generic Musculoskeletal Model
XML_generic_ST_path = dir_path + '\\XML\\scaleTool.xml'                            # Path to the generic Scale Tool XML file
XML_markers_path = dir_path + '\\XML\\markers.xml'                                 # Path to the markers XML file
TRC_file = dir_path + '\\TRC\\pose.trc'                                            # Path to the .trc file that contain the marker data

XML_ST_file = dir_path + '\\XML\\scaleToolSubject.xml'                             # Path to the subject Scale Tool XML file that will be created
XML_SF_file = dir_path + '\\XML\\scaleFactorSubject.xml'                           # Path to the subject Scale Factor file that will be created
scaled_MM_path = dir_path + '\\FullBodyModel\\Subject.osim'                        # Path to the subject Musculoskeletal Model that will be created with the model scaler
scaled_MM_path2 = dir_path + '\\FullBodyModel\\SubjectMoved.osim'                  # Path to the subject Musculoskeletal Model that will be created with the marker placer
XML_markers_path_move = dir_path + '\\XML\\markersMoved.xml'                       # Path to the markers XML file created with the marker placer

# Create a list of Marker Pair Set for each body
markerList = np.array(['RSHO', 'LSHO', 'C7', 'STRN', 'RELB', 'RWRA', 'RWRB', 'LELB', 'LWRA', 'LWRB', 'RASI', 'LASI', 'RPSI',
              'LPSI', 'RTHI', 'RKNE', 'INRKNE', 'RTIB', 'RANK', 'RHEE', 'RTOE', 'RPINKY', 'LTHI', 'LKNE', 'INLKNE',
              'LTIB', 'LANK', 'LHEE', 'LTOE', 'LPINKY', 'T10', 'CLAV', 'LFIN', 'RFIN'])

markerPairList =  np.array([['RASI', 'LASI'],
                  ['RASI', 'RKNE'], ['RKNE', 'RANK'],
                  ['RASI', 'RKNE'], ['RTOE', 'RHEE'], ['RTOE', 'RHEE'], ['RTOE', 'RHEE'],
                  ['LASI', 'LKNE'], ['LKNE', 'LANK'],
                  ['LASI', 'LKNE'], ['LTOE', 'LHEE'], ['LTOE', 'LHEE'], ['LTOE', 'LHEE'],
                  ['RSHO', 'LSHO'], ['T10', 'CLAV'],
                  ['RELB', 'RSHO'], ['RELB', 'RWRB'], ['RELB', 'RWRA'], ['RFIN', 'RWRA'],
                  ['LELB', 'LSHO'], ['LELB', 'LWRB'], ['LELB', 'LWRA'], ['LFIN', 'LWRA']])

bodyNames =  np.array([['pelvis'],
             ['femur_r'], ['tibia_r'],
             ['patella_r'], ['talus_r'], ['calcn_r'], ['toes_r'],
             ['femur_l'], ['tibia_l'],
             ['patella_l'], ['talus_l'], ['calcn_l'], ['toes_l'],
             ['torso'], ['torso'],
             ['humerus_r'], ['ulna_r'], ['radius_r'], ['hand_r'],
             ['humerus_l'], ['ulna_l'], ['radius_l'], ['hand_l']])

nBody = bodyNames.shape[0]

# The first step is to create an XML file with all the information used to scale the model

# Load the generic musculoskeletal model
osimModel = osim.Model(generic_MM_Path)
state = osimModel.initSystem()

# Add a marker set to the model
markerSet = osim.MarkerSet(XML_markers_path)
osimModel.replaceMarkerSet(state, markerSet)
state = osimModel.initSystem()

# Get the marker data from a .trc file
markerData = osim.MarkerData(TRC_file)
initial_time = markerData.getStartFrameTime()
final_time = markerData.getLastFrameTime()
TimeArray = osim.ArrayDouble()                                                 # Time range
TimeArray.set(0,initial_time)
TimeArray.set(1,final_time) 

# Scale Tool
scaleTool = osim.ScaleTool(XML_generic_ST_path)
scaleTool.setName('Subject')                                                   # Name of the subject
scaleTool.setSubjectMass(70)                                                   # Mass of the subject
scaleTool.setSubjectHeight(-1)                                                 # Only for information (not used by scaling)
scaleTool.setSubjectAge(-1)                                                    # Only for information (not used by scaling)

# Generic Model Maker
scaleTool.getGenericModelMaker().setModelFileName('Rajagopal2015.osim')
scaleTool.getGenericModelMaker().setMarkerSetFileName(XML_markers_path)

# Model Scaler
scaleTool.getModelScaler().setApply(1)
scaleTool.getModelScaler().setScalingOrder(osim.ArrayStr('measurements', 1))
scaleTool.getModelScaler().setMarkerFileName(TRC_file)                          
scaleTool.getModelScaler().setTimeRange(TimeArray)
scaleTool.getModelScaler().setPreserveMassDist(1)
scaleTool.getModelScaler().setOutputModelFileName(scaled_MM_path)
scaleTool.getModelScaler().setOutputScaleFileName(XML_SF_file)

# The scale factor information concern the pair of marker that will be used
# to scale each body in your model to make it more specific to your subject.
# The scale factor are computed with the distance the virtual markers and between your experimental markers

# Create a Marker Pair Set fo each body
measurementTemp = osim.Measurement()
bodyScaleTemp = osim.BodyScale()
markerPairTemp = osim.MarkerPair()

for i in range(0, nBody):

    # Create a Marker Pair Set
    markerPair = markerPairTemp.clone()
    markerPair.setMarkerName(0, markerPairList[i][0])
    markerPair.setMarkerName(1, markerPairList[i][1])

    # Create a Body Scale Set
    bodyScale = bodyScaleTemp.clone()
    bodyScale.setName(bodyNames[i][0]) # Name of the body
    bodyScale.setAxisNames(osim.ArrayStr('X Y Z', 1))
    
    # Create a measurement
    measurement = measurementTemp.clone()
    measurement.setApply(1)
    measurement.getBodyScaleSet().adoptAndAppend(bodyScale)
    measurement.getMarkerPairSet().adoptAndAppend(markerPair)
    measurement.setName(bodyNames[i][0]) # Whatever name you want(Usually I set the same name as the body)
    
    # Add the measurement to the Model Scaler
    scaleTool.getModelScaler().addMeasurement(measurement)

# Create the subject Scale Tool XML file
scaleTool.printToXML(XML_ST_file)
print('XML files : ' +  XML_ST_file + ' created')

# Launch the scale tool again with the new XML file and then scale the
# generic musculoskeletal model
scaleTool = osim.ScaleTool(XML_ST_file)

# Scale the model
scaleTool.getModelScaler().processModel(state,osimModel)
print('Scaled Musculoskeletal : ' + scaled_MM_path + ' created')

# In this part, we will use the previous XML file created and update it
# with the MarkerPlacer tool to Adjust the position of the marker on the
# scaled musculoskeletal model

# Load the scaled musculoskeletal model
osimModel = osim.Model(scaled_MM_path)
state = osimModel.initSystem()

# Add a marker set to the model
markerSet = osim.MarkerSet(XML_markers_path)
osimModel.replaceMarkerSet(state, markerSet)
state = osimModel.initSystem()

# Launch the scale tool
scaleTool = osim.ScaleTool(XML_ST_file)

# Get the marker data from a.trc file
markerData = osim.MarkerData(TRC_file)
initial_time = markerData.getStartFrameTime()
final_time = markerData.getLastFrameTime()
TimeArray = osim.ArrayDouble() # Time range
TimeArray.set(0, initial_time)
TimeArray.set(1, final_time)

# The static pose weights will be used to adjust the markers position in 
# the model from a static pose. The weights of the markers depend of the
# confidence you have on its position.In this example, all marker weight
# are fixed to one.

scaleTool.getMarkerPlacer().setApply(1) # Ajustement placement de marqueurs(true or false)
scaleTool.getMarkerPlacer().setStaticPoseFileName(TRC_file) # trc files for adjustements(usually the same as static)
scaleTool.getMarkerPlacer().setTimeRange(TimeArray) # Time range
scaleTool.getMarkerPlacer().setOutputModelFileName(scaled_MM_path2)
scaleTool.getMarkerPlacer().setOutputMarkerFileName(XML_markers_path_move)
scaleTool.getMarkerPlacer().setMaxMarkerMovement(-1.0)

measurementTemp = osim.Measurement()
ikMarkerTaskTemp = osim.IKMarkerTask()

for i in range(0, markerList.shape[0]):

    ikMarkerTask = ikMarkerTaskTemp.clone()

    ikMarkerTask.setName(markerList[i]) # Name of the markers
    ikMarkerTask.setApply(1)
    ikMarkerTask.setWeight(1)

    scaleTool.getMarkerPlacer().getIKTaskSet().adoptAndAppend(ikMarkerTask)

# Create the subject Scale Tool XML file
scaleTool.printToXML(XML_ST_file)
print('XML files : ' + XML_ST_file + ' created')

# Launch the ScaleTool again
scaleTool = osim.ScaleTool(XML_ST_file)
scaleTool.getMarkerPlacer().processModel(state, osimModel)
print('Adjusted markers on the musculoskeletal done')
print('Adjusted markers XML file: ' +  XML_markers_path_move + ' created')

# Display the Scale Factor after the scaling process
osimModel = osim.Model(scaled_MM_path2)
state = osimModel.initSystem()

nBody = osimModel.getBodySet().getSize() # Number of Body

bodyNames = []
scaleFactors = []
# Display scale factors
for i in range(0, nBody):

    ScaleFactor = osim.Vec3(0, 0, 0)
    osimModel.getBodySet().get(i).getScaleFactors(ScaleFactor)
    bodyNames.append(osimModel.getBodySet().get(i).getName())
    scaleFactors.append([ScaleFactor.get(0), ScaleFactor.get(1), ScaleFactor.get(2)])

    if (any(i == t for t in [0, 1, 7, 13, 14, 16, 18, 20, 22])):
        tab = '\t\t'
    else:
        tab = '\t'

    print('Scale factors of ' +  str(bodyNames[i]) + tab + ' - X: ' +  "{:.3f}".format(scaleFactors[i][0])) + '\t\t - Y: ' + "{:.3f}".format(scaleFactors[i][1]) + '\t\t - Z: ' + "{:.3f}".format(scaleFactors[i][2])