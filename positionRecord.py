from fairino import Robot
import time
#Grabar la posicion en joint
class PositionRecorder:
    """
    Graba las posiciónes del robot por un tiempo determinado y las guarda en un archivo .txt
    
    Args:
        robot_ip(String): ip para concectar al robot. Debe ser '192.168.58.2'
        duration_seconds(Float): Duración de la grabación en segundos.
        
    Returns:
        None
    """
    def __init__(self, robot_ip , duration_seconds):
        self.robot = Robot.RPC(robot_ip) #Conectar con el cobot
        self.positions = []  # Lista para almacenar las posiciones
        self.duration_seconds = duration_seconds  # Tiempo total de grabación

    def record_positions(self):
        # Cambiar al robot a modo aprendizaje
        print("Cambiando el robot a modo aprendizaje...")
        self.robot.Mode(1)  # Modo manual
        time.sleep(1)

        self.robot.DragTeachSwitch(1)  # Modo aprendizaje (drag teach)
        print("Robot en modo aprendizaje. Iniciando grabación de posiciones...")
        start_time = time.time()

        while (time.time() - start_time) < self.duration_seconds:
            # Obtener posición actual del robot en joint
            position = self.robot.GetActualJointPosDegree()
            self.positions.append(position[1])

            # Esperar 50 ms
            time.sleep(0.05)
        self.robot.DragTeachSwitch(0) # Salimos de modo aprendizaje

    def save_to_file(self, filename):
        # Guardar las posiciones en un archivo
        with open(filename, 'w') as f:
            for pos in self.positions:
                f.write(f"{pos}\n")
        print(f"Posiciones guardadas en {filename}")

if __name__ == '__main__':
    # IP del robot y duración de la grabación en segundos
    robot_ip = '192.168.58.2'
    duration_seconds = 15  # Cambia este valor según sea necesario

    #Corremos el codigo
    recorder = PositionRecorder(robot_ip, duration_seconds)
    print("Iniciando grabación de posiciones...")
    recorder.record_positions()
    print("Grabación completada.")

    # Guardar las posiciones en un archivo de texto
    recorder.save_to_file('presboton.txt')
