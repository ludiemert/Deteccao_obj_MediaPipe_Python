import cv2
import mediapipe as mp
import math

# Abrir o vídeo
video = cv2.VideoCapture('jumping_jack.mp4')

# Variáveis para detecção dos pontos do corpo usando a lib mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5)

# Variável que vai desenhar as linhas no vídeo
mp_drawing = mp.solutions.drawing_utils

# Contador do polichinelo
contador = 0
last_state = None

# Loop e variáveis
while True:
    success, img = video.read()
    # Verifica se o vídeo foi lido com sucesso
    if not success:
        break

    # Redimensionar a imagem para 640x360
    img = cv2.resize(img, (640, 360))
    # Convertendo a imagem para RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Processar a imagem para detectar os pontos
    results = pose.process(img_rgb)
    # Verifica se há pontos detectados
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Extrair as coordenadas dos pés e das mãos
        h, w, _ = img.shape
        foot_left_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].y * h)
        foot_left_x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].x * w)
        foot_right_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].y * h)
        foot_right_x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].x * w)
        hand_left_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y * h)
        hand_left_x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].x * w)
        hand_right_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].y * h)
        hand_right_x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].x * w)

        # Medir a distância dos pontos
        dist_hand = math.hypot(hand_left_x - hand_right_x, hand_left_y - hand_right_y)
        dist_foot = math.hypot(foot_left_x - foot_right_x, foot_left_y - foot_right_y)

        # Exibir as distâncias
        print(f'Distância das mãos: {dist_hand:.2f} | Distância dos pés: {dist_foot:.2f}')

        # Lógica de contagem de polichinelo ajustada
        if dist_hand <= 150 and dist_foot >= 80:
            if last_state != "jumped":
                contador += 1
                last_state = "jumped"
                print(f'Polichinelo contado: {contador}')
        elif dist_hand > 150 and dist_foot < 80:
            last_state = "not_jumped"

    # Exibir o contador na tela
    h, w, _ = img.shape
    cv2.rectangle(img, (w - 220, 20), (w - 20, 100), (255, 0, 0), -1)  # Ajuste as coordenadas para o lado direito
    cv2.putText(img, f'QTD: {contador}', (w - 200, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    # Exibir o resultado
    cv2.imshow('Resultado', img)

    # Delay de 40 milissegundos
    if cv2.waitKey(40) & 0xFF == ord('q'):  # Pressione 'q' para sair
        break

# Liberar o vídeo e fechar todas as janelas
video.release()
cv2.destroyAllWindows()
