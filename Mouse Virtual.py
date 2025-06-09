import cv2
import mediapipe as mp
import pyautogui
import math
import threading
import time

# --- Classe para Leitura da Câmera em uma Thread Separada ---
class WebcamStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        # Inicia a thread para ler os frames do stream de vídeo
        threading.Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # Loop infinito até que a thread seja parada
        while not self.stopped:
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # Retorna o frame mais recente
        return self.frame

    def stop(self):
        self.stopped = True

# --- CONSTANTES E CONFIGURAÇÕES ---
INDEX_FINGER_TIP = 8
THUMB_TIP = 4
CLICK_DISTANCE_THRESHOLD = 0.04
SMOOTHING_FACTOR = 0.2

# --- INICIALIZAÇÃO ---
screen_width, screen_height = pyautogui.size()
smoothed_x, smoothed_y = 0, 0
current_x, current_y = 0, 0

# Inicia a captura de vídeo com threading
vs = WebcamStream(src=0).start()

mp_hands = mp.solutions.hands
hand_detector = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# --- LOOP PRINCIPAL ---
while True:
    # Pega o frame mais recente da thread
    frame = vs.read()
    if frame is None:
        continue

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(frame_rgb)
    hands = output.multi_hand_landmarks
    frame_height, frame_width, _ = frame.shape

    if hands:
        for hand_landmarks in hands:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            index_tip = hand_landmarks.landmark[INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[THUMB_TIP]
            
            target_x = index_tip.x * screen_width
            target_y = index_tip.y * screen_height

            current_x = smoothed_x + (target_x - smoothed_x) * SMOOTHING_FACTOR
            current_y = smoothed_y + (target_y - smoothed_y) * SMOOTHING_FACTOR
            pyautogui.moveTo(current_x, current_y)
            smoothed_x, smoothed_y = current_x, current_y

            pinch_distance = math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)
            
            index_pixel_pos = (int(index_tip.x * frame_width), int(index_tip.y * frame_height))
            thumb_pixel_pos = (int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height))

            line_color = (255, 0, 0)
            if pinch_distance < CLICK_DISTANCE_THRESHOLD:
                line_color = (0, 255, 0)
                pyautogui.click()
                time.sleep(0.2) # Usamos time.sleep aqui, já que o waitKey não é mais para delay

            cv2.line(frame, index_pixel_pos, thumb_pixel_pos, line_color, 3)
            cv2.circle(frame, index_pixel_pos, 10, line_color, cv2.FILLED)
            cv2.circle(frame, thumb_pixel_pos, 10, line_color, cv2.FILLED)

    cv2.imshow('Mouse Virtual Otimizado', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- FINALIZAÇÃO ---
vs.stop()
cv2.destroyAllWindows()