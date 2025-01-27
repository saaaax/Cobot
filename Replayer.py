from fairino import Robot
import time

class SplineReplayer:
    def __init__(self, robot_ip, position_file, downsample_factor=5):
        self.robot = Robot.RPC(robot_ip)
        self.position_file = position_file
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
                self.positions.append(position)
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
    downsample_factor = 2  # Tomar 1 de cada 5 posiciones para reducir puntos

    replayer = SplineReplayer(robot_ip, position_file, downsample_factor)
    replayer.load_positions()
    replayer.downsample_positions()
    replayer.replay_spline_movements()
