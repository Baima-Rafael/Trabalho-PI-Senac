import sys, mysql.connector
from licensePlate.src.app import LicensePlateThread
from contador_vagas.contadorVagas import ContadorVagasThread
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QFileDialog, QDialog, QHeaderView, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt

def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="countcore"
    )

def placa_db(placa, data, hora):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id_placa FROM tabelaplaca WHERE placa = %s", (placa,))
        result = cursor.fetchone()
        if result:
            id_placa = result[0]  # Obtém o id_placa
                # Insere o id_placa, data e hora na tabelahistorico
            cursor.execute(" INSERT INTO tabelahistorico (placa_id, data, hora) VALUES (%s, %s, %s) """, (id_placa, data, hora))
            conn.commit()
            #print(f"Placa {placa} registrada com id_placa {id_placa} na tabelahistorico.")
        else:
            print(f"Placa {placa} não encontrada na tabelaplaca.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao inserir na tabelahistorico: {e}")

class janelaInicial(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("paginaInicial.ui", self)
        self.pushButton.clicked.connect(self.Entrar)

    def Entrar(self):
        nome = self.lineEdit.text()
        senha = self.lineEdit_2.text()

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tabelaadm WHERE nome = %s AND senha = %s", (nome, senha))
        resultado = cursor.fetchone()
        conn.close
        if True:
            self.janela_adm = janelaADM()
            self.janela_adm.show()
            self.close()
        else:
            QtWidgets.QMensagemBox.warning(self,"Erro", "Usuário ou Senha errado")

class janelaADM(QMainWindow):
    status_vagas_signal = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        uic.loadUi("telaADM.ui", self)


        self.thread_contador = ContadorVagasThread()
        self.thread_contador.status_vagas_signal.connect(self.atualizar_estilos)
        self.thread_contador.start()

        print("Iniciando LicensePlateThread...")
        self.thread_license_plate = LicensePlateThread()
        self.thread_license_plate.plate_detected_signal.connect(self.on_plate_detected)
        self.thread_license_plate.start()

        action_registrar = QAction("Registrar", self)
        action_registrar.triggered.connect(self.funcao_registrar)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(action_registrar)

        self.actionInicio.triggered.connect(self.Inicio)
        self.actionPesquisar.triggered.connect(self.Pesquisa)
        self.actionHistorico.triggered.connect(self.Historico)
        self.actionPerfil.triggered.connect(self.Perfil)
    def Inicio(self):
        self.janela_adm = janelaADM()
        self.janela_adm.show()
        self.close()
    def Pesquisa(self):
        self.janela_pesquisa = janelaPesquisa()
        self.janela_pesquisa.show()
        self.close()
    def Historico(self):
        self.janela_historico = janelaHistorico()
        self.janela_historico.show()
        self.close()
    def Perfil(self):
        self.janela_perfil = janelaPerfil()
        self.janela_perfil.show()
        self.close()
    def atualizar_estilos(self, status_vagas):
        # print(status_vagas)
        for vaga, estado in status_vagas.items():
            frame = getattr(self, vaga, None)
            if frame:
                if estado == "ocupado":
                    frame.setStyleSheet("QFrame { background-color: #c34a4d; }")
                else:
                    frame.setStyleSheet("QFrame { background-color: #47c25c; }")
    # ------
    def funcao_registrar(self):
        self.janela_registro = janelaRegistro()
        self.janela_registro.show()
        self.close()
    def on_plate_detected(self, plate_data):
        # Quando uma placa é detectada, chama placa_db
        print("Está funcionando")
        placa_db(plate_data['placa'], plate_data['data'], plate_data['hora'])

class janelaPesquisa(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("PaginadePesquisa.ui", self)
        # ---------
        self.pushButton.clicked.connect(self.pesquisar)
        self.actionInicio.triggered.connect(self.Inicio)
        self.actionPesquisar.triggered.connect(self.Pesquisa)
        self.actionHistorico.triggered.connect(self.Historico)
        self.actionPerfil.triggered.connect(self.Perfil)
        action_registrar = QAction("Registrar", self)
        action_registrar.triggered.connect(self.funcao_registrar)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(action_registrar)

    

        self.setWindowTitle("Pesquisa")
        self.setGeometry(100, 100, 1275, 879)

    def pesquisar(self):
        nome = self.lineEdit.text()

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT u.id_usuario, u.nome, f.link_foto, p.placa FROM tabelausuario u LEFT JOIN tabelafoto f ON u.id_usuario = f.usuario_id LEFT JOIN tabelaplaca p ON u.id_usuario = p.usuario_id WHERE u.nome = %s;", (nome,))
        resultado = cursor.fetchall()
        self.listWidget.clear()
        for id_usuario, nome, link_foto, placa in resultado:
            item_text = f"ID: {id_usuario} | Nome: {nome} | Foto: {link_foto or 'Nenhuma'} | Placa: {placa or 'Nenhuma'}"
            self.listWidget.addItem(item_text)
        cursor.close()
        conn.close()


    def Inicio(self):
        self.janela_adm = janelaADM()
        self.janela_adm.show()
        self.close()
    def Pesquisa(self):
        self.janela_pesquisa = janelaPesquisa()
        self.janela_pesquisa.show()
        self.close()
    def Historico(self):
        self.janela_historico = janelaHistorico()
        self.janela_historico.show()
        self.close()
    def Perfil(self):
        self.janela_perfil = janelaPerfil()
        self.janela_perfil.show()
        self.close()
    # -----------
    def funcao_registrar(self):
        self.janela_registro = janelaRegistro()
        self.janela_registro.show()
        self.close()

class janelaHistorico(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("histórico.ui", self)
        # --------
        self.actionInicio.triggered.connect(self.Inicio)
        self.actionPesquisar.triggered.connect(self.Pesquisa)
        self.actionHistorico.triggered.connect(self.Historico)
        self.actionPerfil.triggered.connect(self.Perfil)
        action_registrar = QAction("Registrar", self)
        action_registrar.triggered.connect(self.funcao_registrar)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(action_registrar)

        self.setWindowTitle("Histórico")
        self.setGeometry(100, 100, 1318, 862)
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT placa_id, data, hora FROM tabelahistorico")
        resultado = cursor.fetchall()
        self.tableWidget.setRowCount(len(resultado))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Placa", "Data", "Hora",])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for row_idx, row_data in enumerate(resultado):
            for col_idx, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        cursor.close()
        conn.close()
    def Inicio(self):
        self.janela_adm = janelaADM()
        self.janela_adm.show()
        self.close()
    def Pesquisa(self):
        self.janela_pesquisa = janelaPesquisa()
        self.janela_pesquisa.show()
        self.close()
    def Historico(self):
        self.janela_historico = janelaHistorico()
        self.janela_historico.show()
        self.close()
    def Perfil(self):
        self.janela_perfil = janelaPerfil()
        self.janela_perfil.show()
        self.close()
    # -----------
    def funcao_registrar(self):
        self.janela_registro = janelaRegistro()
        self.janela_registro.show()
        self.close()

class janelaPerfil(QMainWindow): 
    def __init__(self):
        super().__init__()
        uic.loadUi("Perfil.ui", self)
        action_registrar = QAction("Registrar", self)
        action_registrar.triggered.connect(self.funcao_registrar)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(action_registrar)
        # ---------
        self.actionInicio.triggered.connect(self.Inicio)
        self.actionPesquisar.triggered.connect(self.Pesquisa)
        self.actionHistorico.triggered.connect(self.Historico)
        self.actionPerfil.triggered.connect(self.Perfil)
        self.pushButton.clicked.connect(self.pesquisar)
        self.pushButton_2.clicked.connect(self.editar)
        self.pushButton_3.clicked.connect(self.deletar)


        self.setWindowTitle("Perfil")
        self.setGeometry(100, 100, 1345, 882)

    def Inicio(self):
        self.janela_adm = janelaADM()
        self.janela_adm.show()
        self.close()
    def Pesquisa(self):
        self.janela_pesquisa = janelaPesquisa()
        self.janela_pesquisa.show()
        self.close()
    def Historico(self):
        self.janela_historico = janelaHistorico()
        self.janela_historico.show()
        self.close()
    def Perfil(self):
        self.janela_perfil = janelaPerfil()
        self.janela_perfil.show()
        self.close()
    # -----------
    def funcao_registrar(self):
        self.janela_registro = janelaRegistro()
        self.janela_registro.show()
        self.close()

    def pesquisar(self):
        try:
            pesquisa = self.lineEdit.text().strip()
            if pesquisa.isalpha():
                conn = conectar_db()
                cursor = conn.cursor()
                cursor.execute("SELECT u.id_usuario, u.nome, f.link_foto, p.placa FROM tabelausuario u LEFT JOIN tabelafoto f ON u.id_usuario = f.usuario_id LEFT JOIN tabelaplaca p ON u.id_usuario = p.usuario_id WHERE u.nome = %s;", (pesquisa,))
                resultado = cursor.fetchall()
                self.listWidget.clear()
                for id_usuario, nome, link_foto, placa in resultado:
                    item_text = f"ID: {id_usuario}\nNome: {nome}\nFoto: {link_foto or 'Nenhuma'}\nPlaca: {placa or 'Nenhuma'}"
                    self.listWidget.addItem(item_text)
                    if link_foto:
                        pixmap = QPixmap(link_foto)
                        self.label_2.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
                    else:
                        print("Sein tofo")
                cursor.close()
                conn.close()
            elif pesquisa.isdigit():
                pesquisa = int(self.lineEdit.text())
                conn = conectar_db()
                cursor = conn.cursor()
                cursor.execute("SELECT u.id_usuario, u.nome, f.link_foto, p.placa FROM tabelausuario u LEFT JOIN tabelafoto f ON u.id_usuario = f.usuario_id LEFT JOIN tabelaplaca p ON u.id_usuario = p.usuario_id WHERE u.id_usuario = %s;", (pesquisa,))
                resultado = cursor.fetchall()
                self.listWidget.clear()
                for id_usuario, nome, link_foto, placa in resultado:
                    item_text = f"ID: {id_usuario} | Nome: {nome} | Foto: {link_foto or 'Nenhuma'} | Placa: {placa or 'Nenhuma'}"
                    self.listWidget.addItem(item_text)
                    if link_foto:
                        pixmap = QPixmap(link_foto)
                        self.label_2.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
                    else:
                        print("Sein tofo")
                cursor.close()
                conn.close()
        except Exception as e:
            print(f"O erro que ocorreu é o: {e}")

    def editar(self):
        if not self.listWidget.currentItem():
            self.listWidget.addItem("Selecione um item para editar")
            return

        item_text = self.listWidget.currentItem().text()
        partes = item_text.split(" | ")
        id_usuario = int(partes[0].split(": ")[1])
        nome = partes[1].split(": ")[1]
        link_foto = partes[2].split(": ")[1] if partes[2].split(": ")[1] != "Nenhuma" else ""
        placa = partes[3].split(": ")[1] if partes[3].split(": ")[1] != "Nenhuma" else ""

        dialog = EditarUsuario(nome, placa, link_foto, self)
        if dialog.exec_():  # Se o usuário clicar em "Aplicar"
            novos_dados = dialog.get_dados()
            try:
                conn = conectar_db()
                cursor = conn.cursor()

            # Atualiza o nome na tabela tabelausuario
                cursor.execute("UPDATE tabelausuario SET nome = %s WHERE id_usuario = %s;", (novos_dados["nome"], id_usuario))

            # Atualiza a placa na tabela tabelaplaca (se existir um registro)
                if novos_dados["placa"]:
                    cursor.execute(
                        "UPDATE tabelaplaca SET placa = %s WHERE usuario_id = %s;",
                        (novos_dados["placa"], id_usuario)
                    )
                else:
                # Remove o registro da placa se o campo estiver vazio
                    cursor.execute("DELETE FROM tabelaplaca WHERE usuario_id = %s;", (id_usuario,))

            # Atualiza o link_foto na tabela tabelafoto (se existir um registro)
                if novos_dados["link_foto"]:
                    cursor.execute(
                        "UPDATE tabelafoto SET link_foto = %s WHERE usuario_id = %s;",
                        (novos_dados["link_foto"], id_usuario)
                    )
                else:
                # Remove o registro da foto se o campo estiver vazio
                    cursor.execute("DELETE FROM tabelafoto WHERE usuario_id = %s;", (id_usuario,))

                conn.commit()
                cursor.close()
                conn.close()

            # Atualiza o QListWidget
                item_text = f"ID: {id_usuario} | Nome: {novos_dados['nome']} | Foto: {novos_dados['link_foto'] or 'Nenhuma'} | Placa: {novos_dados['placa'] or 'Nenhuma'}"
                self.listWidget.currentItem().setText(item_text)

            # Atualiza o QLabel com a nova foto
                if novos_dados["link_foto"]:
                    pixmap = QPixmap(novos_dados["link_foto"])
                    self.label_2.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
                else:
                    self.label_2.setText("Nenhuma foto disponível")

            except Exception as e:
                print(f"Erro ao atualizar: {e}")
                self.listWidget.addItem("Erro ao atualizar os dados")      

    def deletar(self):
        if not self.listWidget.currentItem():
            self.listWidget.addItem("Selecione um item para deletar")
            return

    # Extrai o id_usuario do item selecionado
        item_text = self.listWidget.currentItem().text()
        partes = item_text.split(" | ")
        id_usuario = int(partes[0].split(": ")[1])

        try:
            conn = conectar_db()
            cursor = conn.cursor()

            # Deleta os registros associados nas tabelas tabelaplaca e tabelafoto
            cursor.execute("DELETE FROM tabelaplaca WHERE usuario_id = %s;", (id_usuario,))
            cursor.execute("DELETE FROM tabelafoto WHERE usuario_id = %s;", (id_usuario,))

            # Deleta o usuário da tabela tabelausuario
            cursor.execute("DELETE FROM tabelausuario WHERE id_usuario = %s;", (id_usuario,))

            cursor.execute("SELECT MAX(id_usuario) FROM tabelausuario;")
            maior_id = cursor.fetchone()[0]
            if maior_id is not None:
                proximo_id = maior_id + 1
            else:
                proximo_id = 1
            
            cursor.execute("ALTER TABLE tabelausuario AUTO_INCREMENT = %s;", (proximo_id,))
            conn.commit()
            cursor.close()
            conn.close()

          # Remove o item do QListWidget
            self.listWidget.takeItem(self.listWidget.currentRow())

        # Limpa o QLabel da foto
            self.label_2.setText("Nenhuma foto disponível")

        except Exception as e:
          print(f"Erro ao deletar: {e}")
          self.listWidget.addItem("Erro ao deletar o usuário")

class EditarUsuario(QDialog):
    def __init__(self, nome, placa, link_foto, parent=None):
        super().__init__(parent)
        uic.loadUi("QDialogEditar.ui", self)
        self.lineEdit.setText(nome)
        self.lineEdit_2.setText(placa if placa else "")
        self.lineEdit_3.setText(link_foto if link_foto else "")
        self.pushButton.clicked.connect(self.accept)
        self.pushButton_2.clicked.connect(self.reject)
    
    
    def get_dados(self):
        return {
        "nome": self.lineEdit.text(),
        "placa": self.lineEdit_2.text(),
        "link_foto": self.lineEdit_3.text()
        }
        
class janelaRegistro(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ADMResgistrar.ui", self)
        action_registrar = QAction("Registrar", self)
        action_registrar.triggered.connect(self.funcao_registrar)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(action_registrar)
        # ---------

        self.pushButton.clicked.connect(self.registrar)
        self.actionInicio.triggered.connect(self.Inicio)
        self.actionPesquisar.triggered.connect(self.Pesquisa)
        self.actionHistorico.triggered.connect(self.Historico)
        self.actionPerfil.triggered.connect(self.Perfil)

        self.setWindowTitle("Registro")
        self.setGeometry(100, 100, 1261, 841)
        self.image_path = None

        self.label_imagem = QLabel(self.frame)
        self.label_imagem.setGeometry(0, 0, self.frame.width(), self.frame.height())
        self.label_imagem.setScaledContents(True)
        self.label_imagem.mousePressEvent = self.carregar_imagem

    def carregar_imagem(self, event):
        # Abre um diálogo para selecionar a imagem
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem", "",
                                                  "Imagens (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            # Armazena o caminho da imagem
            self.image_path = file_name
            # Exibe a imagem no QLabel
            pixmap = QPixmap(file_name)
            self.label_imagem.setPixmap(pixmap)

    def Inicio(self):
        self.janela_adm = janelaADM()
        self.janela_adm.show()
        self.close()
    def Pesquisa(self):
        self.janela_pesquisa = janelaPesquisa()
        self.janela_pesquisa.show()
        self.close()
    def Historico(self):
        self.janela_historico = janelaHistorico()
        self.janela_historico.show()
        self.close()
    def Perfil(self):
        self.janela_perfil = janelaPerfil()
        self.janela_perfil.show()
        self.close()
    def registrar(self):
        nome = self.lineEdit.text()
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tabelausuario (nome) VALUES (%s)", (nome,))
        conn.commit()
        self.id_usuario = cursor.lastrowid
        cursor.close()
        conn.close()
        if not self.id_usuario:
            print("Erro: ID do usuário não foi gerado!")
            return
        self.registrar_placa()
        self.registrar_img()
        self.limpar_areas()
    def registrar_placa(self):
        placa = self.lineEdit_2.text()
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tabelaplaca (placa, usuario_id) VALUES (%s, %s)", (placa,self.id_usuario,))
        conn.commit()
        cursor.close()
        conn.close()
    def registrar_img(self):
        image_path = self.image_path if self.image_path else ""
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tabelafoto (link_foto, usuario_id) VALUES (%s, %s)", (image_path,self.id_usuario,))
        conn.commit()
        cursor.close()
        conn.close()
    def limpar_areas(self):
        self.lineEdit.clear()  # Limpa o campo do nome
        self.lineEdit_2.clear()  # Limpa o campo da placa
        self.image_path = None  # Remove a referência da imagem
        self.label_imagem.clear()  # Limpa a QLabel onde a imagem foi carregada
    # def Configuracoes(self):
    #     self.janela_perfil = janelaPerfil()
    #     self.janela_perfil.show()
    #     self.close()
    # -----------
    def funcao_registrar(self):
        self.janela_registro = janelaRegistro() 
        self.janela_registro.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = janelaInicial()
    janela.show()
    sys.exit(app.exec_())