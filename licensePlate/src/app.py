from os import walk
import cv2, mysql.connector, pytesseract
# from licensePlate.src.lib.filters import pytesseract
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np

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

# def apply_filter(plate):
#     gray = get_grayscale(plate)
#     thresh = thresholding(gray)
#     return thresh

def scan_plate(image):
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'
    custom_config = r'-c tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyz/ --psm 6'
    plate_number = (pytesseract.image_to_string(image, config=custom_config))
    return plate_number[:-2]

def validate_plate(plate_number, authorized_plate):
    if plate_number in authorized_plate:
        return 'AUTHORIZED'
    else:
        return 'NOT AUTHORIZED'

# def main():
#     authorized_plate = get_authorized_plates()

#     cap = cv2.VideoCapture(0)

#     if not cap.isOpened():
#         print("Erro: Não foi possível abrir a câmera.")
#         return []
    
#     authorized_data = []

#     while True:
#         # Captura um frame da câmera
#         ret, frame = cap.read()
#         if not ret:
#             print("Erro: Não foi possível capturar o frame.")
#             break

#         # Aplica o filtro no frame capturado
#         filtered_frame = apply_filter(frame)

#         # Tenta ler a placa do frame
#         plate_number = scan_plate(filtered_frame)

#         # Verifica se a placa está autorizada
#         status = validate_plate(plate_number, authorized_plate)
        
#         if status == 'AUTHORIZED':
#             current_time = datetime.now()
#             authorized_data.append({
#                 'placa': plate_number,
#                 'data': current_time.strftime('%Y-%m-%d'),
#                 'hora': current_time.strftime('%H:%M:%S')
#             })
#             # print(f"Placa autorizada detectada: {plate_number} às {current_time}")

#         # Sai do loop se a tecla 'q' for pressionada
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # Libera a câmera e fecha as janelas
#     cap.release()
#     cv2.destroyAllWindows()

#     # plates = []
#     # plates_filter_applied = []
#     # plates_numbers = []
#     # data = []
#     # authorized_data = []
#     # _, _, filenames = next(walk('../images/'))

#     # # Append the files name to list data
#     # for i in range(len(filenames)):
#     #     data.append([])
#     #     data[i].append(filenames[i])

#     # # Make an append to list plates
#     # for i in images:
#     #     plates.append(cv2.imread(i))

#     # # Calls the function apply_filter() passing the plate image
#     # for i in range(len(plates)):
#     #     plates_filter_applied.append(apply_filter(plates[i]))

#     # # Calls the function scan_plate() passing the plate image with filter applied
#     # for i in range(len(plates_filter_applied)):
#     #     plates_numbers.append(scan_plate(plates_filter_applied[i]))
#     #     data[i].append(plates_numbers[i])

#     # # Calls the function validate_plate() passing the plate number
#     # for i in range(len(plates_numbers)):
#     #     data[i].append(validate_plate(plates_numbers[i], authorized_plate))
#     #     if data[i][2] == 'AUTHORIZED':
#     #         current_time = datetime.now()
#     #         authorized_data.append({
#     #             'placa': plates_numbers[i],
#     #             'data': current_time.strftime('%Y-%m-%d'),  # Formato: AAAA-MM-DD
#     #             'hora': current_time.strftime('%H:%M:%S')   # Formato: HH:MM:SS
#     #         })
#     # format_output(data)
#     cv2.imshow(cap)
#     return authorized_data


class LicensePlateThread(QThread):
    plate_detected_signal = pyqtSignal(dict)  # Sinal para emitir dados da placa detectada

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
            print("Thread LicensePlateThread em execução")
            # Inicializa a câmera
            cap = cv2.VideoCapture(0)

            if not cap.isOpened():
                print("Erro: Não foi possível abrir a câmera.")
                return

            # Obtém a lista de placas autorizadas
            authorized_plate = get_authorized_plates()

            while self.running:
                # Captura um frame da câmera
                ret, frame = cap.read()
                if not ret:
                    print("Erro: Não foi possível capturar o frame.")
                    break

                # Aplica o filtro no frame capturado
                # filtered_frame = apply_filter(frame)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                blur = cv2.medianBlur(gray, 5)
                _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                kernel = np.ones((5, 5), np.uint8)
                dilated = cv2.dilate(thresh, kernel, iterations=1)
                erode = cv2.erode(dilated, kernel, iterations=1)
                opened = cv2.morphologyEx(erode, cv2.MORPH_OPEN, kernel)
                filtered_frame = cv2.Canny(opened, 100, 200)

                # Tenta ler a placa do frame
                plate_number = scan_plate(filtered_frame)

                # Verifica se a placa está autorizada
                status = validate_plate(plate_number, authorized_plate)

                # Se autorizada, emite o sinal com os dados da placa
                if status == 'AUTHORIZED':
                    current_time = datetime.now()
                    plate_data = {
                        'placa': plate_number,
                        'data': current_time.strftime('%Y-%m-%d'),
                        'hora': current_time.strftime('%H:%M:%S')
                    }
                    self.plate_detected_signal.emit(plate_data)
                    # print(f"Placa autorizada detectada: {plate_number} às {current_time}")

                # Exibe o frame (para depuração, mas deve ser removido em produção com Qt)
                cv2.imshow('video', frame)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break