from fairino import Robot
import time
import rospy
from std_msgs.msg import Float32MultiArray

class Correccion:
    def __init__(self):
        # Suscribirse al tema '/error_pose'
        self.sub = rospy.Subscriber("/error_pose", Float32MultiArray, self.callback)

    def callback(self,msg):
        # Leer las posiciones de las juntas
        error = msg.data 
        rospy.loginfo(error)

        # Desuscribirse para que el callback solo se ejecute una vez
        #self.sub.unregister()

        robot = Robot.RPC('192.168.58.2')

        blend = 1 # whether to smooth, 1-smooth, 0-not smooth
        ovl = 20.0 #speed scaling
        ret = robot.LoadTPD('track') # track preloading

        pos_tcp =robot.GetActualTCPPose()
        new_position= pos_tcp[1]
        #Posicion sin error
        for i in range(0,3): new_position[i]=new_position[i] + error[i]

        #Cambiar a posicion joint
        ret, pos_j = robot.GetInverseKin(0,new_position,config=-1)
        print("Nueva posición en Joint", pos_j)

        #Movemos a posicion sin error
        tool = 0 #Tool coordinate system number
        user = 0 #Workpiece coordinate system number
        ret = robot.MoveJ(pos_j, tool, user, vel=20)
        print('corrigiendo')
        time.sleep(5)
        print('trackeando')
        ret = robot.MoveTPD('track', blend, ovl) # trajectory replication
        print("Trajectory reproduction error code",ret)

if __name__ == '__main__':
    rospy.init_node('error_pose', anonymous=True)
    pose_reader = Correccion()
    # Mantener el nodo vivo
    rospy.spin()