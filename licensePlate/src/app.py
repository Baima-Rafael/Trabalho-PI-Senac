import cv2, os, mysql.connector, easyocr, re, time, glob
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np

image_count = 0

# Função para obter placas autorizadas do banco de dados
def get_authorized_plates():
    # Recupera placas autorizadas do banco de dados.

    # Returns:
    #     list: Lista de placas autorizadas (strings).

    # Raises:
    #     mysql.connector.Error: Se a conexão com o banco falhar.

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
    # Pré-processa a imagem para melhorar a detecção de placas.

    # Args:
    #     image (np.ndarray): Imagem em formato BGR.

    # Returns:
    #     np.ndarray: Imagem pré-processada (binarizada) ou None em caso de erro.
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
    # Detecta a região da placa na imagem binarizada.

    # Args:
    #     image (np.ndarray): Imagem binarizada.

    # Returns:
    #     tuple: Coordenadas (x, y, w, h) da região da placa ou None se não encontrada.
    
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
    # Escaneia a placa na imagem usando EasyOCR.

    # Args:
    #     image (np.ndarray): Imagem em formato BGR.
    #     reader (easyocr.Reader): Instância do EasyOCR.
    #     debug_dir (str): Diretório para salvar imagens de depuração.

    # Returns:
    #     tuple: (plate_number, plate_region), onde plate_number é a placa detectada (str)
    #            e plate_region é a região (x, y, w, h) ou None.

    # Notes:
    #     Após 10 imagens, a pasta debug_dir é limpa para economizar espaço.
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
        image_count += 1

        if image_count >= 10:
            try:
                # Remove todas as imagens na pasta debug_plates
                for file in glob.glob(os.path.join(debug_dir, "*.png")):
                    os.remove(file)
                print(f"Pasta {debug_dir} limpa.")
                # Reseta o contador
                image_count = 0
            except Exception as e:
                print(f"Erro ao limpar pasta {debug_dir}: {e}")
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
    # Valida o formato da placa (padrão Mercosul).

    # Args:
    #     plate_number (str): Texto da placa detectada.

    # Returns:
    #     bool: True se a placa for válida, False caso contrário.

    # Padrão brasileiro antigo: LLLNNNN (3 letras + 4 números)
    # Padrão Mercosul: LLLNLNN (3 letras + 1 número + 1 letra + 2 números)
    pattern = r'^[A-Z]{7}$|^[A-Z]{3}[0-9][A-Z][0-9]{2}$' #[0-9]{4} ficava colada no [A-Z]{7}
    return bool(re.match(pattern, plate_number))

# Função para validar se a placa está autorizada
def validate_plate(plate_number, authorized_plate):
    # Verifica se a placa está autorizada.

    # Args:
    #     plate_number (str): Placa detectada.
    #     authorized_plate (list): Lista de placas autorizadas.

    # Returns:
    #     str: 'AUTHORIZED' se autorizada, 'NOT AUTHORIZED' caso contrário.
    if plate_number in authorized_plate:
        print(plate_number)
        return 'AUTHORIZED'
    return 'NOT AUTHORIZED'

# Classe para a thread de leitura de placas
class LicensePlateThread(QThread):
    # Thread para leitura contínua de placas via câmera.
    plate_detected_signal = pyqtSignal(dict)  # Sinal para emitir dados da placa detectada

    def __init__(self):
        super().__init__()
        self.running = True
        # Inicializa o EasyOCR (inglês para números e letras)
        self.reader = easyocr.Reader(['en'], gpu=False)  # Inicializa EasyOCR / # Use gpu=True se tiver GPU

    def run(self):
        # Executa o loop de captura e processamento de placas.
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
                time.sleep(2)
            except Exception as e:
                print(f"Erro no loop de captura: {e}")

        # Libera a câmera
        try:
            cap.release()
        except Exception as e:
            print(f"Erro ao liberar a câmera: {e}")