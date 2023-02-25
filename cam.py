import cv2
import math
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Inicializar la captura de video
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Configurar la detección de landmarks de la cara
with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
) as face_mesh:

    # Variables para almacenar la posición anterior del punto medio de la frente
    prev_forehead_x, prev_forehead_y = None, None

    # Variable para almacenar el total de píxeles que se han movido hacia arriba
    total_pixels_up = 0

    while True:
        ret, frame = cap.read()

        if ret == False:
            break
        frame = cv2.flip(frame, 1)

        # Convierte la imagen a RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Realiza la detección de los puntos de referencia de la cara
        results = face_mesh.process(image)

        if results.multi_face_landmarks:
            # Encuentra las coordenadas del landmark de la nariz
            nose_landmark = results.multi_face_landmarks[0].landmark[1]
            nose_x, nose_y = int(
                nose_landmark.x * image.shape[1]), int(nose_landmark.y * image.shape[0])

            # Encuentra las coordenadas del landmark del mentón
            chin_landmark = results.multi_face_landmarks[0].landmark[152]
            chin_x, chin_y = int(
                chin_landmark.x * image.shape[1]), int(chin_landmark.y * image.shape[0])

            # Encuentra las coordenadas del landmark del punto medio de la frente
            forehead_landmark = results.multi_face_landmarks[0].landmark[10]
            forehead_x, forehead_y = int(
                forehead_landmark.x * image.shape[1]), int(forehead_landmark.y * image.shape[0])

            # Dibuja círculos en los landmarks de la nariz, mentón y frente
            cv2.circle(image, (nose_x, nose_y), 5, (0, 0, 255), -1)
            cv2.circle(image, (chin_x, chin_y), 5, (0, 255, 0), -1)
            cv2.circle(image, (forehead_x, forehead_y), 5, (255, 0, 0), -1)

            # Si esta es la primera vez que se detecta el punto medio de la frente,
            # simplemente almacene su posición actual y continúe
            if prev_forehead_x is None and prev_forehead_y is None:
                prev_forehead_x, prev_forehead_y = forehead_x, forehead_y
                continue
                # Calcula la distancia entre la posición actual del punto medio de la frente
            # y su posición anterior
            dist_forehead = math.sqrt(
                (forehead_x - prev_forehead_x)**2 + (forehead_y - prev_forehead_y)**2)

            # Si la distancia es mayor a un cierto umbral,
            # significa que la cabeza se ha movido hacia arriba
            if dist_forehead > 10:
                # Calcula la cantidad de píxeles que se han movido hacia arriba
                pixels_up = forehead_y - prev_forehead_y

                # Incrementa el contador total de píxeles hacia arriba
                total_pixels_up += pixels_up

                # Imprime el total de píxeles hacia arriba
                print("Total pixels up:", total_pixels_up)

                # Actualiza la posición anterior del punto medio de la frente
                prev_forehead_x, prev_forehead_y = forehead_x, forehead_y

        # Dibuja los puntos de referencia de la cara y la línea que los conecta
        mp_drawing.draw_landmarks(
            image,
            results.multi_face_landmarks[0],
            mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=mp_drawing.DrawingSpec(
                color=(0, 255, 0), thickness=1, circle_radius=1),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=1))

        # Convierte la imagen de nuevo a BGR y la muestra en pantalla
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imshow("Face mesh", image)

        # Si se presiona la tecla 'q', se termina el programa
        if cv2.waitKey(1) == ord("q"):
            break


cap.release()
cv2.destroyAllWindows()
