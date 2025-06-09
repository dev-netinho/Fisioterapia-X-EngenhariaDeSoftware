import cv2
import mediapipe as mp
import math
import threading
import time
import numpy as np
import pyautogui
import pygame

# --- Classe WebcamStream (sem alterações) ---
class WebcamStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
    def start(self):
        threading.Thread(target=self.update, args=()).start()
        return self
    def update(self):
        while not self.stopped:
            (self.grabbed, self.frame) = self.stream.read()
    def read(self):
        return self.frame
    def stop(self):
        self.stopped = True

# --- Configurações e Constantes (sem alterações) ---
TARGET_POSITIONS = [(0.5, 0.5), (0.8, 0.5), (0.2, 0.5), (0.5, 0.2), (0.5, 0.8)]
TARGET_RADIUS_NORMALIZED = 0.05
MAX_SCORE = 20
INDEX_FINGER_TIP = 8
SMOOTHING_FACTOR = 0.2

# --- Inicialização do Áudio ---
pygame.init()
pygame.mixer.init()
try:
    hit_sound = pygame.mixer.Sound("hit.wav")
    finish_sound = pygame.mixer.Sound("finish.wav")
    sound_enabled = True
except pygame.error:
    print("AVISO: Arquivos de som 'hit.wav' ou 'finish.wav' não encontrados. O programa rodará sem som.")
    sound_enabled = False

# --- Funções Auxiliares (sem alterações) ---
def save_report(final_score, total_time_val, avg_time, avg_efficiency):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"relatorio_fisiotrack_{timestamp}.csv"
    header = ['Metrica', 'Valor']
    data = [
        ['Pontuacao Final', f"{final_score}/{MAX_SCORE}"],
        ['Tempo Total (s)', f"{total_time_val:.2f}"],
        ['Tempo Medio por Alvo (s)', f"{avg_time:.2f}"],
        ['Eficiencia Media do Movimento (%)', f"{avg_efficiency:.1f}"]
    ]
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    print(f"Relatório salvo como: {filename}")

def reset_exercise():
    global state
    state = {
        "current_target_index": 0, "score": 0, "start_time": time.time(),
        "last_hit_time": time.time(), "feedback_text": "", "game_over": False,
        "total_time": 0, "smoothed_x": 0, "smoothed_y": 0,
        "path_distance": 0.0, "last_known_pos": None, "efficiency_scores": [],
        "start_of_path_pos": TARGET_POSITIONS[0]
    }

# --- INICIALIZAÇÃO PRINCIPAL ---
screen_width, screen_height = pyautogui.size()
vs = WebcamStream(src=0).start()
mp_hands = mp.solutions.hands
hand_detector = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils
state = {}
reset_exercise()

# --- LOOP PRINCIPAL DO PROGRAMA ---
while True:
    frame = vs.read()
    if frame is None:
        continue

    frame = cv2.flip(frame, 1)

    # Processamento da imagem (MediaPipe)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(frame_rgb)
    hands = output.multi_hand_landmarks

    # ALTERADO: O vídeo da câmera é redimensionado para ser o fundo
    canvas = cv2.resize(frame, (screen_width, screen_height))

    if not state["game_over"]:
        if hands:
            for hand_landmarks in hands:
                # Desenha os landmarks no canvas grande (após o resize)
                mp_drawing.draw_landmarks(canvas, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                index_tip = hand_landmarks.landmark[INDEX_FINGER_TIP]
                
                # Lógica de suavização, distância e pontuação (sem alterações)
                state["smoothed_x"] += (index_tip.x - state["smoothed_x"]) * SMOOTHING_FACTOR
                state["smoothed_y"] += (index_tip.y - state["smoothed_y"]) * SMOOTHING_FACTOR
                
                current_pos = (state["smoothed_x"], state["smoothed_y"])
                if state["last_known_pos"]:
                    delta_distance = math.hypot(current_pos[0] - state["last_known_pos"][0], current_pos[1] - state["last_known_pos"][1])
                    state["path_distance"] += delta_distance
                state["last_known_pos"] = current_pos
                
                current_target_pos = TARGET_POSITIONS[state["current_target_index"]]
                distance_to_target = math.hypot(state["smoothed_x"] - current_target_pos[0], state["smoothed_y"] - current_target_pos[1])
                
                if distance_to_target < TARGET_RADIUS_NORMALIZED:
                    if (time.time() - state["last_hit_time"]) > 0.5:
                        if sound_enabled: hit_sound.play()
                        
                        straight_dist = math.hypot(current_target_pos[0] - state["start_of_path_pos"][0], current_target_pos[1] - state["start_of_path_pos"][1])
                        if state["path_distance"] > 0:
                            efficiency = (straight_dist / state["path_distance"]) * 100
                            state["efficiency_scores"].append(efficiency)
                        
                        state["score"] += 1
                        state["current_target_index"] = (state["current_target_index"] + 1) % len(TARGET_POSITIONS)
                        state["last_hit_time"] = time.time()
                        state["path_distance"] = 0.0
                        state["start_of_path_pos"] = current_target_pos

                        if state["score"] >= MAX_SCORE:
                            state["game_over"] = True
                            state["total_time"] = time.time() - state["start_time"]
                            if sound_enabled: finish_sound.play()
                            
                            avg_efficiency = np.mean(state["efficiency_scores"]) if state["efficiency_scores"] else 100.0
                            avg_time = state["total_time"] / state["score"] if state["score"] > 0 else 0
                            save_report(state["score"], state["total_time"], avg_time, avg_efficiency)
        
        # --- Desenho dos Elementos do Jogo sobre o Canvas ---
        # Alvos e cursor agora são desenhados por cima do vídeo em tela cheia
        target_radius_pixels = int(TARGET_RADIUS_NORMALIZED * screen_width * 0.4)
        target_pos_pixels = (int(current_target_pos[0] * screen_width), int(current_target_pos[1] * screen_height))
        cv2.circle(canvas, target_pos_pixels, target_radius_pixels, (255, 100, 100), 5)
        cv2.circle(canvas, target_pos_pixels, target_radius_pixels - 10, (255, 200, 200), cv2.FILLED)

        if hands:
            cursor_pos_pixels = (int(state["smoothed_x"] * screen_width), int(state["smoothed_y"] * screen_height))
            cv2.circle(canvas, cursor_pos_pixels, 15, (0, 255, 0), cv2.FILLED)
    
    # Desenho do HUD sobre o canvas
    elapsed_time = int(time.time() - state["start_time"])
    cv2.rectangle(canvas, (20, 20), (370, 110), (20,20,20), -1)
    cv2.putText(canvas, f"Tempo: {elapsed_time}s", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(canvas, f"Pontuacao: {state['score']}/{MAX_SCORE}", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    if state["game_over"]:
        # Tela final (sem alterações na lógica)
        overlay = canvas.copy()
        cv2.rectangle(overlay, (0, 0), (screen_width, screen_height), (0,0,0), -1)
        canvas = cv2.addWeighted(overlay, 0.6, canvas, 0.4, 0)
        
        avg_time = state["total_time"] / state["score"] if state["score"] > 0 else 0
        avg_efficiency = np.mean(state["efficiency_scores"]) if state["efficiency_scores"] else 100.0
        
        cv2.putText(canvas, "Exercicio Concluido!", (screen_width//2 - 250, screen_height//2 - 120), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        cv2.putText(canvas, f"Pontuacao Final: {state['score']}/{MAX_SCORE}", (screen_width//2 - 220, screen_height//2 - 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        cv2.putText(canvas, f"Tempo Total: {state['total_time']:.2f} segundos", (screen_width//2 - 220, screen_height//2), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        cv2.putText(canvas, f"Tempo medio/alvo: {avg_time:.2f}s", (screen_width//2 - 220, screen_height//2 + 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        cv2.putText(canvas, f"Eficiencia media: {avg_efficiency:.1f}%", (screen_width//2 - 220, screen_height//2 + 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        cv2.putText(canvas, "Pressione 'r' para reiniciar ou 'q' para sair", (screen_width//2 - 320, screen_height - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.imshow('FisioTrack - Exercicio Interativo', canvas)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('r') and state["game_over"]:
        reset_exercise()

vs.stop()
cv2.destroyAllWindows()
pygame.quit()