# from os import walk
# import cv2, mysql.connector, pytesseract
# # from licensePlate.src.lib.filters import pytesseract
# from datetime import datetime
# from PyQt5.QtCore import QThread, pyqtSignal
# import numpy as np

# def get_authorized_plates():
#     conn = mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='',
#         database='countcore'
#     )
#     cursor = conn.cursor()
#     cursor.execute("SELECT placa FROM tabelaplaca")
#     results = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return [row[0] for row in results]

# # def apply_filter(plate):
# #     gray = get_grayscale(plate)
# #     thresh = thresholding(gray)
# #     return thresh

# def scan_plate(image):
#     pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'
#     custom_config = r'-c tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyz/ --psm 6'
#     plate_number = (pytesseract.image_to_string(image, config=custom_config))
#     return plate_number[:-2]

# def validate_plate(plate_number, authorized_plate):
#     if plate_number in authorized_plate:
#         return 'AUTHORIZED'
#     else:
#         return 'NOT AUTHORIZED'

# # def main():
# #     authorized_plate = get_authorized_plates()

# #     cap = cv2.VideoCapture(0)

# #     if not cap.isOpened():
# #         print("Erro: Não foi possível abrir a câmera.")
# #         return []
    
# #     authorized_data = []

# #     while True:
# #         # Captura um frame da câmera
# #         ret, frame = cap.read()
# #         if not ret:
# #             print("Erro: Não foi possível capturar o frame.")
# #             break

# #         # Aplica o filtro no frame capturado
# #         filtered_frame = apply_filter(frame)

# #         # Tenta ler a placa do frame
# #         plate_number = scan_plate(filtered_frame)

# #         # Verifica se a placa está autorizada
# #         status = validate_plate(plate_number, authorized_plate)
        
# #         if status == 'AUTHORIZED':
# #             current_time = datetime.now()
# #             authorized_data.append({
# #                 'placa': plate_number,
# #                 'data': current_time.strftime('%Y-%m-%d'),
# #                 'hora': current_time.strftime('%H:%M:%S')
# #             })
# #             # print(f"Placa autorizada detectada: {plate_number} às {current_time}")

# #         # Sai do loop se a tecla 'q' for pressionada
# #         if cv2.waitKey(1) & 0xFF == ord('q'):
# #             break

# #     # Libera a câmera e fecha as janelas
# #     cap.release()
# #     cv2.destroyAllWindows()

# #     # plates = []
# #     # plates_filter_applied = []
# #     # plates_numbers = []
# #     # data = []
# #     # authorized_data = []
# #     # _, _, filenames = next(walk('../images/'))

# #     # # Append the files name to list data
# #     # for i in range(len(filenames)):
# #     #     data.append([])
# #     #     data[i].append(filenames[i])

# #     # # Make an append to list plates
# #     # for i in images:
# #     #     plates.append(cv2.imread(i))

# #     # # Calls the function apply_filter() passing the plate image
# #     # for i in range(len(plates)):
# #     #     plates_filter_applied.append(apply_filter(plates[i]))

# #     # # Calls the function scan_plate() passing the plate image with filter applied
# #     # for i in range(len(plates_filter_applied)):
# #     #     plates_numbers.append(scan_plate(plates_filter_applied[i]))
# #     #     data[i].append(plates_numbers[i])

# #     # # Calls the function validate_plate() passing the plate number
# #     # for i in range(len(plates_numbers)):
# #     #     data[i].append(validate_plate(plates_numbers[i], authorized_plate))
# #     #     if data[i][2] == 'AUTHORIZED':
# #     #         current_time = datetime.now()
# #     #         authorized_data.append({
# #     #             'placa': plates_numbers[i],
# #     #             'data': current_time.strftime('%Y-%m-%d'),  # Formato: AAAA-MM-DD
# #     #             'hora': current_time.strftime('%H:%M:%S')   # Formato: HH:MM:SS
# #     #         })
# #     # format_output(data)
# #     cv2.imshow(cap)
# #     return authorized_data


# class LicensePlateThread(QThread):
#     plate_detected_signal = pyqtSignal(dict)  # Sinal para emitir dados da placa detectada

#     def __init__(self):
#         super().__init__()
#         self.running = True

#     def run(self):
#             print("Thread LicensePlateThread em execução")
#             # Inicializa a câmera
#             cap = cv2.VideoCapture(0)

#             if not cap.isOpened():
#                 print("Erro: Não foi possível abrir a câmera.")
#                 return

#             # Obtém a lista de placas autorizadas
#             authorized_plate = get_authorized_plates()

#             while self.running:
#                 # Captura um frame da câmera
#                 ret, frame = cap.read()
#                 if not ret:
#                     print("Erro: Não foi possível capturar o frame.")
#                     break

#                 # Aplica o filtro no frame capturado
#                 # filtered_frame = apply_filter(frame)
#                 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#                 blur = cv2.medianBlur(gray, 5)
#                 _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#                 kernel = np.ones((5, 5), np.uint8)
#                 dilated = cv2.dilate(thresh, kernel, iterations=1)
#                 erode = cv2.erode(dilated, kernel, iterations=1)
#                 opened = cv2.morphologyEx(erode, cv2.MORPH_OPEN, kernel)
#                 filtered_frame = cv2.Canny(opened, 100, 200)

#                 # Tenta ler a placa do frame
#                 plate_number = scan_plate(filtered_frame)

#                 # Verifica se a placa está autorizada
#                 status = validate_plate(plate_number, authorized_plate)

#                 # Se autorizada, emite o sinal com os dados da placa
#                 if status == 'AUTHORIZED':
#                     current_time = datetime.now()
#                     plate_data = {
#                         'placa': plate_number,
#                         'data': current_time.strftime('%Y-%m-%d'),
#                         'hora': current_time.strftime('%H:%M:%S')
#                     }
#                     self.plate_detected_signal.emit(plate_data)
#                     # print(f"Placa autorizada detectada: {plate_number} às {current_time}")

#                 # Exibe o frame (para depuração, mas deve ser removido em produção com Qt)
#                 cv2.imshow('video', frame)
#                 if cv2.waitKey(10) & 0xFF == ord('q'):
#                     break

# ---------------------------------------------------------------------------------------------------------- #

import cv2, os
import mysql.connector
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
import easyocr
import re

# Função para obter placas autorizadas do banco de dados
def get_authorized_plates():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='countcore'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT placa FROM tabelaplaca")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row[0] for row in results]

# Função para pré-processamento da imagem
def preprocess_image(image):
    try:
        # Converte para escala de cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Aplica CLAHE para melhorar o contraste
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        # Aplica desfoque leve para reduzir ruído
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        # Binarização adaptativa
        thresh = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )
        # Operações morfológicas
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        eroded = cv2.erode(dilated, kernel, iterations=1)
        return eroded
    except Exception as e:
        print(f"Erro no pré-processamento: {e}")
        return None
    

# Função para detectar a região da placa
def detect_plate_region(image):
    if image is None:
        return None
    try:
        # Encontra contornos
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            # Calcula a área e a proporção
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            # Parâmetros mais flexíveis
            if 300 < area < 20000 and 1.5 < aspect_ratio < 6:
                return (x, y, w, h)
        return None
    except Exception as e:
        print(f"Erro na detecção da placa: {e}")
        return None
    
# Função para escanear a placa usando EasyOCR
def scan_plate(image, reader, debug_dir="debug_plates"):
    try:
        # Pré-processamento
        processed = preprocess_image(image)
        if processed is None:
            return "", None

        # Detecta a região da placa
        plate_region = detect_plate_region(processed)
        if plate_region is None:
            return "", None

        x, y, w, h = plate_region
        # Recorta a região da placa
        plate_image = image[y:y+h, x:x+w]
        # Converte para escala de cinza para EasyOCR
        plate_image_gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)

        # Salva a imagem recortada para depuração
        if not os.path.exists(debug_dir):
            os.makedirs(debug_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        debug_path = os.path.join(debug_dir, f"plate_{timestamp}.png")
        cv2.imwrite(debug_path, plate_image_gray)

        # Usa EasyOCR para ler o texto
        results = reader.readtext(plate_image_gray, allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        # Extrai o texto e filtra
        plate_number = ""
        for (bbox, text, prob) in results:
            if prob > 0.1:  # Limiar de confiança reduzido para depuração
                text = text.replace(" ", "").upper().strip()
                plate_number += text
                print(f"Texto detectado (prob={prob:.2f}): {text}")

        # Valida o formato da placa
        if is_valid_plate(plate_number):
            return plate_number, (x, y, w, h)
        else:
            print(f"Placa inválida detectada: {plate_number}")
            return "", (x, y, w, h)
    except Exception as e:
        print(f"Erro ao escanear a placa: {e}")
        return "", None

# Função para validar o formato da placa
def is_valid_plate(plate_number):
    # Padrão brasileiro antigo: LLLNNNN (3 letras + 4 números)
    # Padrão Mercosul: LLLNLNN (3 letras + 1 número + 1 letra + 2 números)
    pattern = r'^[A-Z]{7}$|^[A-Z]{3}[0-9][A-Z][0-9]{2}$' #[0-9]{4} ficava colada no [A-Z]{7}
    return bool(re.match(pattern, plate_number))

# Função para validar se a placa está autorizada
def validate_plate(plate_number, authorized_plate):
    if plate_number in authorized_plate:
        print(plate_number)
        return 'AUTHORIZED'
    return 'NOT AUTHORIZED'

# Classe para a thread de leitura de placas
class LicensePlateThread(QThread):
    plate_detected_signal = pyqtSignal(dict)  # Sinal para emitir dados da placa detectada

    def __init__(self):
        super().__init__()
        self.running = True
        # Inicializa o EasyOCR (inglês para números e letras)
        self.reader = easyocr.Reader(['en'], gpu=False)  # Use gpu=True se tiver GPU

    def run(self):
        # Inicializa a câmera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Erro: Não foi possível abrir a câmera.")
            return

        # Obtém a lista de placas autorizadas
        authorized_plate = get_authorized_plates()
        if not authorized_plate:
            print("Aviso: Nenhuma placa autorizada no banco de dados.")

        while self.running:
            try:
                ret, frame = cap.read()
                if not ret:
                    print("Erro: Não foi possível capturar o frame.")
                    break

                # Escaneia a placa
                plate_number, plate_region = scan_plate(frame, self.reader)
                if plate_number:
                    status = validate_plate(plate_number, authorized_plate)
                    if status == 'AUTHORIZED':
                        current_time = datetime.now()
                        plate_data = {
                            'placa': plate_number,
                            'data': current_time.strftime('%Y-%m-%d'),
                            'hora': current_time.strftime('%H:%M:%S')
                        }
                        self.plate_detected_signal.emit(plate_data)
                        print(f"Placa autorizada detectada: {plate_number} às {current_time}")

                # Desenha a região da placa no frame
                if plate_region:
                    x, y, w, h = plate_region
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, plate_number if plate_number else "N/A", 
                               (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            except Exception as e:
                print(f"Erro no loop de captura: {e}")

        # Libera a câmera
        try:
            cap.release()
        except Exception as e:
            print(f"Erro ao liberar a câmera: {e}")

    # def run(self):
    #     # Inicializa a câmera
    #     cap = cv2.VideoCapture(0)
        

    #     if not cap.isOpened():
    #         print("Erro: Não foi possível abrir a câmera.")
    #         return

    #     # Obtém a lista de placas autorizadas
    #     authorized_plate = get_authorized_plates()

    #     while self.running:
    #         # Captura um frame da câmera
    #         ret, frame = cap.read()
    #         if not ret:
    #             print("Erro: Não foi possível capturar o frame.")
    #             break

    #         # Tenta ler a placa do frame
    #         plate_number = scan_plate(frame, self.reader)

    #         # Verifica se a placa está autorizada
    #         status = validate_plate(plate_number, authorized_plate)

    #         # Se autorizada, emite o sinal com os dados da placa
    #         if status == 'AUTHORIZED' and plate_number:
    #             current_time = datetime.now()
    #             plate_data = {
    #                 'placa': plate_number,
    #                 'data': current_time.strftime('%Y-%m-%d'),
    #                 'hora': current_time.strftime('%H:%M:%S')
    #             }
    #             self.plate_detected_signal.emit(plate_data)
    #             print(f"Placa autorizada detectada: {plate_number} às {current_time}")

    #         # Exibe o frame (para depuração)
    #         cv2.imshow('autenticação', frame)
    #         if cv2.waitKey(10) & 0xFF == ord('q'):
    #             break

    #     # Libera a câmera e fecha as janelas
    #     cap.release()
    #     cv2.destroyAllWindows()