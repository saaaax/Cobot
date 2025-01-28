from fairino import Robot

# Establish a connection with the robot controller and return a robot object if the connection is successful
robot = Robot.RPC('192.168.58.2')
#Posición deseada y error conocido
#ret, pos_tcp =robot.GetActualTCPPose()
#error=[120, 0, 0]

def corregir(pos,error,TCP=False):
    """
    Reajustar la posición si existe error
    
    Args:
        pos (list[float]): Lista de 6 valores que representan la posición del cobot, puede ser en joint
            ([j1,j2,j3,j4,j5,j6]) o TCP ([x,y,z,rx,ry,rz])
        error (list[float]): Lista de 3 valores que representan los errores en las 
            coordenadas espaciales (x, y, z) en mm.
        TCP (bool, optional): Indica si la posición se entrega en TCP (True) o joint(False).
            Por defecto es False.

    Returns:
        Posición ajustada en joint.
    """
    if TCP == True:
        new_position= pos #extraemos la posicion
        #Ajustamos el error
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