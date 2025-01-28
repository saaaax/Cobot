from fairino import Robot
import error
#definir el error en x,y,z en mm
e=[10,0,0]

class SplineReplayer:
    """
    Reproduce las posiciones de un archivo .txt con la función Spline del cobot
    
    Args:
        robot_ip(String): ip para concectar al robot. Debe ser '192.168.58.2'
        position_file(String): nombre del archivo donde están las posiciones
        downsample_factor(int): Factor para reducir las posiciones
        
    Returns:
        None
    """
    def __init__(self, robot_ip, position_file, downsample_factor):
        self.robot = Robot.RPC(robot_ip) #Conectarse con el robot
        self.position_file = position_file #Archivo con el recorrido
        self.downsample_factor = downsample_factor  # Factor para reducir puntos
        self.tool = 0  # Sistema de coordenadas de la herramienta
        self.user = 0  # Sistema de coordenadas del usuario

    def load_positions(self):
        # Cargar las posiciones desde el archivo .txt
        self.positions = []
        with open(self.position_file, 'r') as f:
            for line in f:
                # Convertir cada línea a una lista de floats y redondear a 3 decimales
                position = [round(float(x), 3) for x in line.strip().strip("[]").split(',')]
                pos_error= error.corregir(position,e) # Arreglar el error 
                pos=  [round(num, 3) for num in pos_error]# Redondear nuevamente
                self.positions.append(pos)
        print(f"Se cargaron {len(self.positions)} posiciones del archivo {self.position_file}.")

    def downsample_positions(self):
        # Reducir la cantidad de puntos mediante submuestreo
        self.positions = self.positions[::self.downsample_factor]
        print(f"Se redujo la cantidad de puntos a {len(self.positions)} después del submuestreo.")

    def replay_spline_movements(self):
        # Reproducir movimientos con spline
        print("Iniciando movimientos spline...")

        # Iniciar movimiento spline
        ret = self.robot.SplineStart()
        print("Spline motion started: error code", ret)

        # Enviar los puntos de trayectoria uno por uno
        for idx, joint_position in enumerate(self.positions):
            ret = self.robot.SplinePTP(joint_position, self.tool, self.user, vel=20)
            print(f" - Spline PTP motion {idx + 1}/{len(self.positions)}: error code", ret)

        # Finalizar movimiento spline
        ret = self.robot.SplineEnd()
        print("Spline motion ended: error code", ret)
        print("Reproducción completada.")

if __name__ == '__main__':
    # Configurar IP del robot y archivo de posiciones
    robot_ip = '192.168.58.2'
    position_file = 'presboton.txt'  # Archivo generado previamente

    # Configuración del factor de submuestreo
    downsample_factor = 2  # Tomar 1 de cada n posiciones para reducir puntos

    # Corremos el código
    replayer = SplineReplayer(robot_ip, position_file, downsample_factor)
    replayer.load_positions()
    replayer.downsample_positions()
    replayer.replay_spline_movements()