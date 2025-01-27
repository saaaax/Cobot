from fairino import Robot
import time

# Establish a connection with the robot controller and return a robot object if the connection is successful
robot = Robot.RPC('192.168.58.2')

type = 1 # data type, 1-joint position
name = 'track' # track name
period = 4 # sampling period, 2ms or 4ms or 8ms
di = 0 # di input configuration
do = 0 # do output configuration

ret = robot.SetTPDParam(name, period, di_choose=di) #configure TPD parameters
print("Configuration TPD parameter error code", ret)

robot.Mode(1) # robot cut to manual mode
time.sleep(1)
robot.DragTeachSwitch(1) # robot cuts to drag teach mode

Pose_1 = robot.GetActualJointPosDegree()
print("Get current tool position", Pose_1)
time.sleep(1)

ret = robot.SetTPDStart(name, period, do_choose=do) # start logging the demonstration trajectory
print("Starting to record the demonstration track error code", ret)
time.sleep(15)

ret = robot.SetWebTPDStop() # stop logging the demonstration trajectory
print("Stopped recording of the demonstration track error code", ret)
robot.DragTeachSwitch(0) # robot cuts to non-drag teach mode

#------------------------------------------------------------------------

blend = 1 # whether to smooth, 1-smooth, 0-not smooth
ovl = 100.0 #speed scaling

# ret = robot.MoveJ(Pose_1[1],0,0) #move to start point
# print("Movement to start point error code",ret)
# time.sleep(5)

ret = robot.LoadTPD(name) # track preloading
print("track preload error code",ret)

ret = robot.MoveJ(Pose_1[1],0,0) #move to start point
print("Movement to start point error code",ret)
time.sleep(5)

ret = robot.MoveTPD(name, blend, ovl) # trajectory replication
print("Trajectory reproduction error code",ret)