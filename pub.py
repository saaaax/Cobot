#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32MultiArray

def publicar_lista():
    # Inicializa el nodo
    rospy.init_node('error_pose', anonymous=True)
    # Crea un publicador en el tópico '/lista_posiciones'
    pub = rospy.Publisher('/error_pose', Float32MultiArray, queue_size=10)
    # Define la frecuencia de publicación
    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        # Crea un mensaje Float32MultiArray
        mensaje = Float32MultiArray()
        # Asigna la lista al atributo 'data' del mensaje
        mensaje.data = [0, 0, 0]

        # Publica el mensaje en el tópico
        pub.publish(mensaje)
        # Espera hasta la siguiente iteración
        rate.sleep()

if __name__ == '__main__':
    try:
        publicar_lista()
    except rospy.ROSInterruptException:
        pass
