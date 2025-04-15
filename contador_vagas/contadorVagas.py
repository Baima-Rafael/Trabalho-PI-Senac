import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

# Dicionário com coordenadas das vagas (nome: [x, y, w, h])
# Para adicionar as próprias vagas, utilize o "seletorVaga.py", ele irá retornar um txt chamado roi
vagas = {
    "vagas1" : [108,236,90,34],
    "vagas2" : [224,232,128,36],
    "vagas3" : [221,298,107,42],
    "vagas4" : [92,304,118,45]
}


class ContadorVagasThread(QThread):
    # Thread para monitoramento do status das vagas de estacionamento.
    status_vagas_signal = pyqtSignal(dict)
    

    def run(self):
        # Executa o loop de captura e análise de vagas.
        video = cv2.VideoCapture(1)

        while True:
            check,img = video.read()
            if not check:
                print("Erro com o video")
                break
            imgCinza = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            imgTh = cv2.adaptiveThreshold(imgCinza,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
            imgBlur = cv2.medianBlur(imgTh,5)
            kernel = np.ones((3,3),np.int8)
            imgDil = cv2.dilate(imgBlur,kernel)

            status_vagas = {}
            for nome, (x,y,w,h) in vagas.items():
                recorte = imgDil[y:y+h,x:x+w]
                qtPxBranco = cv2.countNonZero(recorte)

                if qtPxBranco > 150:
                    status_vagas[nome] = "ocupado"
                else:
                    status_vagas[nome] = "livre"

            self.status_vagas_signal.emit(status_vagas)

            cv2.imshow('video',img)
            cv2.waitKey(10)