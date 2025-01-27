from fairino import Robot

# Establish a connection with the robot controller and return a robot object if the connection is successful
robot = Robot.RPC('192.168.58.2')
#Posición deseada y error conocido
#ret, pos_tcp =robot.GetActualTCPPose()
#error=[120, 0, 0]

def corregir(pos,error,TCP=False):
    if TCP == True:
        new_position= pos
        #Posicion sin error
        for i in range(0,3): new_position[i]=pos[i] + error[i]

        #Cambiar a posicion joint
        ret, pos_j = robot.GetInverseKin(0,new_position,config=-1)
        #print("Nueva posición en Joint", pos_j)
        return pos_j
    else:
        new_position= robot.GetForwardKin(pos)[1]
        #Posicion sin error
        for i in range(0,3): new_position[i]=new_position[i] + error[i]
        
        #Cambiar a posicion joint
        ret, pos_j = robot.GetInverseKin(0,new_position,config=-1)
        #print("Nueva posición en Joint", pos_j)
        return pos_j      

#corregir(pos_tcp, error)