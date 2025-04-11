import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

vagas = {
    "vagas1" : [108,236,90,34],
    "vagas2" : [224,232,128,36],
    "vagas3" : [221,298,107,42],
    "vagas4" : [92,304,118,45]
}
# C:/Users/57434946/OneDrive - SENAC PA - EDU/Área de Trabalho/Trabalho-Senac-main/contador_vagas/video.mp4
class ContadorVagasThread(QThread):
    status_vagas_signal = pyqtSignal(dict)
    

    def run(self):
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

            # qtVagasAbertas = 0
            # vagas_ocupadas = []
            status_vagas = {}
            for nome, (x,y,w,h) in vagas.items():
                recorte = imgDil[y:y+h,x:x+w]
                qtPxBranco = cv2.countNonZero(recorte)
                # cv2.putText(img,str(qtPxBranco),(x,y+h-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)

                if qtPxBranco > 150:
                    # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    # vagas_ocupadas.append(nome)
                    status_vagas[nome] = "ocupado"
                else:
                    # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    # qtVagasAbertas +=1
                    status_vagas[nome] = "livre"

            # cv2.rectangle(img,(90,0),(415,60),(255,0,0),-1)
            # cv2.putText(img,f'LIVRE: {qtVagasAbertas}/8',(95,45),cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),5)

            # if vagas_ocupadas:
            #     ocupadas_texto = ", ".join(vagas_ocupadas)
            #     cv2.putText(img, f'Ocupadas: {ocupadas_texto}', (95, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            self.status_vagas_signal.emit(status_vagas)

            cv2.imshow('video',img)
            # cv2.imshow('video TH', imgDil)
            cv2.waitKey(10)