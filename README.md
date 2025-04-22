# {Nome do Projeto}

Esse sistema visa solucionar problemas com autenticação de placas e gerenciamento de vagas de estacionamento, assim, reduzindo o tempo que leva para estacionar

# Guia de Instalação

### Requisitos Mínimos do Sistema
- Processador: Intel Core i3 ou equivalente
- Memória RAM: 8 GB
- Espaço disponível: 256 GB SSD ou 500 GB HD
- Câmera: Webcam ou câmera USB compatível com OpenCV (resolução mínima 720p).
- Sistema Operacional: Windows 10/11, Ubuntu 20.04/22.04, ou macOS

### Software
- Python: Versão 3.8 ou superior.
- MySQL: Versão 8.0 ou superior.

### Bibliotecas utilizadas
- sys
- mysql.connector-python==8.0.33
- datetime
- opencv-python==4.8.0
- numpy==1.24.3
- easyocr==1.7.1
- re
- time
- os
- glob
- PyQt5==5.15.9
  - uic
  - QtWidgets
  - QtCore
  - QtGui

# Configuração do Ambiente

## 1. Instalação do Python
Baixe e instale o Python 3.8+ em python.org.
Certifique-se de adicionar o Python ao PATH durante a instalação.

## 2. Instalação do MySQL
Baixe e instale o MySQL Server (ou server de sua preferência) em [mysql.com](https://dev.mysql.com/downloads/installer/).
Durante a instalação, configure:<br>
Usuário: root (ou configure e atualize no código)<br>
Senha: Deixe em branco (ou configure e atualize no código).
Após a instalação do MySQL Server (ou server de sua preferência), importe o arquivo .sql

## 3. Configuração das Variáveis de Ambiente 
- MySQL: 
   - Certifique-se de que o host, usuário, senha e nome do banco de dados no código correspondem 
     à configuração do MySQL:
    ```
mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Atualize se necessário
        database="countcore"
       )
     ```

- Câmeras:<br>
    - Verifique os índices das câmeras no OpenCV:<br>
     LicensePlateThread usa cv2.VideoCapture(0) (câmera principal).<br>
     ContadorVagasThread usa cv2.VideoCapture(1) (câmera secundária).<br>
     Ajuste os índices se necessário (teste com cv2.VideoCapture(n)).

## 4. Configuração dos Arquivos de Interface <br>
Certifique-se de que os arquivos .ui (interface gráfica) estão no mesmo diretório do script principal (main.py):
paginaInicial.ui<br>
telaADM.ui<br>
PaginadePesquisa.ui<br>
histórico.ui<br>
Perfil.ui<br>
ADMResgistrar.ui<br>
QDialogEditar.ui<br>
Esses arquivos devem ser gerados com o Qt Designer e carregados via uic.loadUi.

## 5. Teste do Sistema
- Execute o script principal:<br>
``` 
python main.py 
```

- Verifique:<br>
A janela inicial (janelaInicial) deve abrir.<br>
Conexão com o banco de dados deve funcionar.<br>
Câmeras devem capturar vídeo (se configuradas corretamente).<br>
As threads LicensePlateThread e ContadorVagasThread devem processar placas e vagas.

## 6. Solução de Problemas
- Erro de conexão com MySQL:
   - Verifique se o servidor MySQL está rodando (mysqladmin -u root -p status).
   - Confirme as credenciais no código.
- Câmera não detectada:
  - Teste os índices da câmera com um script simples:
```
import cv2
cap = cv2.VideoCapture(0)  # Ou 1, 2, etc.
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        cv2.imshow("Teste", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
```
- Erro de dependências:
  - Reinstale as bibliotecas com versões específicas:
```
pip install --force-reinstall mysql-connector-python==8.0.33 PyQt5==5.15.9 opencv-python==4.8.0 easyocr==1.7.1 numpy==1.24.3
```

## 7. Observações
- EasyOCR
  - Na primeira execução, o EasyOCR baixará modelos automaticamente (necessita de internet).
  - Para melhor desempenho, habilite GPU se disponível (gpu=True em easyocr.Reader).
- Vagas:
  - Ajuste as coordenadas em vagas no arquivo contador_vagas.py conforme a câmera:
```
vagas = {
    "vagas1": [108, 236, 90, 34],
    "vagas2": [224, 232, 128, 36],
    "vagas3": [221, 298, 107, 42],
    "vagas4": [92, 304, 118, 45]
}
```
- Diretório de Depuração:
  - Imagens processadas são salvas em debug_plates/ para análise (verifique se há espaço no disco). OBSERVAÇÃO: Após 10 imagens, todas as imagens são deletas

# Documentação do Código
## Funções e Módulos
### Módulo: main.py
  - Propósito: Implementa a interface gráfica (usando PyQt5) e a lógica de interação com o banco de dados MySQL para autenticação, registro, pesquisa e histórico de placas.
  - Funções:
    - conectar_db()
      - **Propósito**: Estabelece conexão com o banco de dados MySQL.
      - **Parâmetros**: Nenhum.
      - **Retorno**: mysql.connector.connection.MySQLConnection (objeto de conexão).
      - **Exceções**.
        - mysql.connector.Error: Falha na conexão (credenciais inválidas, servidor offline).
      - **Notas**: Usado por várias classes para acessar o banco.
    - placa_db(placa, data, hora)
      - **Propósito**: Insere registros de placas detectadas na tabela tabelahistorico.
      - **Parâmetros:
        - placa (str): Número da placa.
        - data (str): Data no formato 'YYYY-MM-DD'.
        - hora (str): Hora no formato 'HH:MM:SS'.
      - **Retorno**: Nenhum.
      - **Exceções**:
        - mysql.connector.Error: Erros de consulta ou inserção.
      - **Notas**: Verifica se a placa existe em tabelaplaca antes de inserir.
  - Classes:
    - janelaInicial(QMainWindow)
      - **Propósito**: Janela de login para administradores.
      - **Métodos Principais**:
        - Entrar(): Valida credenciais e abre janelaADM se corretas.
      - **Sinais**: Nenhum.
      - **Notas**: Carrega paginaInicial.ui.
    - janelaADM(QMainWindow)
      - **Propósito**: Interface principal para monitoramento de vagas e placas.
      - **Métodos Principais**:
        - atualizar_estilos(status_vagas): Atualiza cores das vagas (vermelho para ocupada, verde 
          para livre).
        - on_plate_detected(plate_data): Registra placas detectadas no banco.
        - funcao_registrar(), Inicio(), Pesquisa(), Historico(), Perfil(): Navegação entre 
          janelas.
      - **Sinais**:
        - status_vagas_signal: Recebe status das vagas.
      - **Notas**: Inicializa threads LicensePlateThread e ContadorVagasThread.
    - janelaPesquisa, janelaHistorico, janelaPerfil, janelaRegistro, EditarUsuario:
      - **Propósito**: Interfaces para pesquisa de placas, visualização de histórico, gerenciamento de 
        perfis e registro de usuários.
      - **Métodos Principais**:
        - Métodos de navegação (Inicio, Pesquisa, etc.).
        - Funcionalidades específicas (ex.: pesquisar em janelaPesquisa, registrar em 
          janelaRegistro).
      - **Notas**: Cada uma carrega um arquivo .ui correspondente.
### Módulo: license_plate.py
  - Propósito: Implementa o reconhecimento de placas usando OpenCV e EasyOCR, com validação de autorização e armazenamento de imagens de depuração.
  - Funções:
    - get_authorized_plates()
      - **Propósito**: Recupera placas autorizadas do banco.
      - **Parâmetro**: Nenhum.
      - **Retorno**: list de strings (placas).
      - **Exceções**:
        - mysql.connector.Error: Falha na conexão ou consulta.
      - **Notas**: Usado para validar placas detectadas.
    - preprocess_image(image)
      - **Propósito**: Aplica filtros (escala de cinza, CLAHE, binarização) para melhorar detecção.
      - **Parâmetro**: image (np.ndarray): Imagem BGR.
      - **Retorno**: np.ndarray (imagem binarizada) ou None.
      - **Exceções**:
        - cv2.error: Erros de processamento de imagem.
      - **Notas**: Essencial para destacar a placa.
    - detect_plate_region(image)
      - **Propósito**: Identifica a região da placa com base em contornos.
      - **Parâmetro**: image (np.ndarray): Imagem binarizada.
      - **Retorno**: tuple (x, y, w, h) ou None.
      - **Exceções**:
        - cv2.error: Erros na detecção de contornos.
      - **Notas**: Usa filtros de área e proporção.
    - scan_plate(image, reader, debug_dir)
      - **Propósito**: Extrai o texto da placa usando EasyOCR e salva imagens de depuração.
      - **Parâmetros**:
         - image (np.ndarray): Imagem BGR.
         - reader (easyocr.Reader): Instância do EasyOCR.
         - debug_dir (str): Pasta para imagens de depuração.
      - **Retorno**: tuple (plate_number: str, plate_region: tuple).
      - **Exceções**:
        - cv2.error: Erros de processamento.
        - OSError: Falhas ao salvar imagens.
      - **Notas**: Limpa debug_dir após 10 imagens.
    - is_valid_plate(plate_number)
      - **Propósito**: Valida o formato da placa (Mercosul).
      - **Parâmetros**: plate_number (str): Texto da placa.
      - **Retorno**: bool.
      - **Exceção**: Nenhuma.
      - **Notas**: Usa regex para padrão LLLNLNN.
    - validate_plate(plate_number, authorized_plate)
      - **Propósito**: Verifica se a placa está na lista de autorizadas.
      - **Parâmetros**: 
        - plate_number (str): Placa detectada
        - authorized_plate (list): Lista de placas autorizadas.
      - **Retorno**: str ('AUTHORIZED' ou 'NOT AUTHORIZED').
      - **Exceção**: Nenhuma.
  - Classes:
    - LicensePlateThread(QThread)
      - **Propósito**: Executa leitura contínua de placas em uma thread separada.
      - **Método Principal**: run(): Loop de captura, processamento e emissão de sinais.
      - **Sinal**: plate_detected_signal: Emite dicionário com dados da placa (placa, data, hora).
      - **Notas**: Usa cv2.VideoCapture(0) para câmera principal.
### Módulo: contador_vagas.py
  - Propósito: Monitora vagas de estacionamento usando análise de imagem para detectar ocupação.
  - Classes:
    - ContadorVagasThread(QThread)
      - **Propósito**: Analisa vídeo para determinar o status das vagas.
      - **Método Principal**: run(): Loop de captura, processamento e emissão de status.
      - **Sinal**: status_vagas_signal: Emite dicionário com status das vagas (nome: 'ocupado' ou 'livre').
      - **Notas**:
        - Usa cv2.VideoCapture(1) para câmera secundária.
        - Depende do dicionário vagas com coordenadas fixas.
  - Variáveis:
      - Propósito: Define regiões das vagas com coordenadas [x, y, w, h].
      - Formato: Dicionário {nome: [x, y, w, h]}.
      - Notas: Requer ajuste utilizando o código seletorVaga.py
## Convenções de Código
### Regras de Nomenclatura
- Funções:
  - Usar snake_case (ex.: conectar_db, preprocess_image).
  - Nomes descritivos que indicam ação ou propósito (ex.: scan_plate, validate_plate).
- Classes:
  - Usar CamelCase (ex.: janelaInicial, LicensePlateThread).
  - Prefixos como janela para interfaces gráficas, indicando contexto.
- Variáveis:
  - Usar snake_case para variáveis locais e globais (ex.: image_count, plate_number).
  - Evitar abreviações ambíguas; preferir nomes claros (ex.: status_vagas em vez de sv).
- Constantes:
  - Usar UPPER_SNAKE_CASE (ex.: nenhuma constante definida explicitamente no código atual).
- Sinais Qt:
  - Usar snake_case com sufixo _signal (ex.: plate_detected_signal, status_vagas_signal).

---

# Guia de Uso do Sistema

O sistema é uma aplicação desktop com interface gráfica (GUI) desenvolvida com PyQt5, que integra reconhecimento de placas de veículos, monitoramento de vagas de estacionamento e gerenciamento de usuários, com armazenamento de dados em um banco de dados MySQL (`countcore`). Abaixo, você encontrará instruções detalhadas sobre como interagir com o sistema e exemplos práticos de uso.

## Como Utilizar o Sistema

O sistema é operado por meio de uma interface gráfica, executada a partir do arquivo `main.py`. Ele não possui uma API ou interface de linha de comando (CLI).

### 1. Executando o Sistema

Para iniciar o sistema, execute o arquivo `main.py` no terminal ou em um ambiente Python:

```bash
python main.py
```

Isso abrirá a janela inicial de login (`janelaInicial`), onde você deve inserir credenciais de administrador (nome e senha) para acessar o sistema.

### 2. Fluxo de Uso

O sistema é composto por várias janelas, cada uma com funcionalidades específicas. Aqui está o fluxo geral de uso:

1. **Tela de Login (`janelaInicial`)**:
   - Insira o nome de usuário e a senha de um administrador registrado no banco de dados (`tabelaadm`).
   - Clique em "Entrar" para acessar a tela principal (`janelaADM`).
   - Se as credenciais estiverem incorretas, uma mensagem de erro será exibida.

2. **Tela Principal (`janelaADM`)**:
   - Exibe o status das vagas de estacionamento (livre ou ocupado) em tempo real, atualizado pela thread `ContadorVagasThread`.
   - Mostra placas detectadas automaticamente pela thread de reconhecimento de placas (`LicensePlateThread`).
   - Oferece um menu com opções para navegar para outras telas: **Início**, **Pesquisar**, **Histórico**, **Perfil** e **Registrar**.

3. **Tela de Pesquisa (`janelaPesquisa`)**:
   - Permite pesquisar usuários por nome, exibindo informações como ID, nome, placa e foto associada.
   - Entrada: Nome do usuário no campo de texto.
   - Saída: Lista de resultados com ID, nome, foto e placa.

4. **Tela de Histórico (`janelaHistorico`)**:
   - Exibe o histórico de entradas de veículos, incluindo placa, data e hora.
   - Dados são carregados automaticamente da tabela `tabelahistorico`.

5. **Tela de Perfil (`janelaPerfil`)**:
   - Permite pesquisar, editar e deletar informações de usuários.
   - Suporta pesquisa por nome ou ID, edição de nome, placa e foto, e exclusão de registros.

6. **Tela de Registro (`janelaRegistro`)**:
   - Permite registrar novos usuários com nome, placa e foto.
   - Fotos são carregadas via diálogo de seleção de arquivo.

7. **Tela de Edição (`EditarUsuario`)**:
   - Um diálogo modal para editar informações de um usuário selecionado na tela de perfil.

## Exemplos Práticos

Abaixo estão exemplos práticos de uso do sistema, com entradas e saídas esperadas.

### Exemplo 1: Login no Sistema

**Contexto**: Um administrador deseja acessar o sistema.

**Entrada**:
- Na tela de login (`janelaInicial`):
  - Nome: `admin`
  - Senha: `12345`

**Ação**:
- Clique no botão "Entrar".

**Saída Esperada**:
- A tela de login fecha, e a tela principal (`janelaADM`) é exibida, mostrando o status das vagas e o menu de navegação.
- Se as credenciais estiverem incorretas, uma mensagem de erro aparece: `Usuário ou Senha errado`.

### Exemplo 2: Registrar um Novo Usuário

**Contexto**: Um administrador deseja registrar um novo usuário com uma placa e uma foto.

**Entrada**:
- Na tela de registro (`janelaRegistro`):
  - Nome: `João Silva`
  - Placa: `ABC1234`
  - Foto: Clique no frame, selecione `C:/imagens/joao.jpg`

**Ação**:
- Clique no botão "Registrar".

**Saída Esperada**:
- Os dados são salvos nas tabelas `tabelausuario`, `tabelaplaca` e `tabelafoto`.
- Os campos são limpos, e a imagem é removida do frame.
- No banco de dados:
  - `tabelausuario`: `(id_usuario: 1, nome: João Silva)`
  - `tabelaplaca`: `(placa: ABC1234, usuario_id: 1)`
  - `tabelafoto`: `(link_foto: C:/imagens/joao.jpg, usuario_id: 1)`

### Exemplo 3: Pesquisar um Usuário

**Contexto**: Um administrador deseja buscar informações de um usuário.

**Entrada**:
- Na tela de pesquisa (`janelaPesquisa`):
  - Nome: `João Silva`

**Ação**:
- Clique no botão "Pesquisar".

**Saída Esperada**:
- A lista (`listWidget`) exibe:
  ```
  ID: 1 | Nome: João Silva | Foto: C:/imagens/joao.jpg | Placa: ABC1234
  ```

### Exemplo 4: Editar Informações de um Usuário

**Contexto**: Um administrador deseja atualizar os dados de um usuário.

**Entrada**:
- Na tela de perfil (`janelaPerfil`):
  - Pesquisar: `João Silva`
  - Selecione o item na lista.
  - Clique no botão "Editar".
- No diálogo de edição (`EditarUsuario`):
  - Nome: `João Silva Jr.`
  - Placa: `XYZ5678`
  - Foto: `C:/imagens/joao_novo.jpg`

**Ação**:
- Clique em "Aplicar" no diálogo.

**Saída Esperada**:
- A lista é atualizada:
  ```
  ID: 1 | Nome: João Silva Jr. | Foto: C:/imagens/joao_novo.jpg | Placa: XYZ5678
  ```
- A imagem no `label_2` é atualizada para `joao_novo.jpg`.
- No banco de dados, as tabelas `tabelausuario`, `tabelaplaca` e `tabelafoto` refletem as alterações.

### Exemplo 5: Visualizar o Histórico

**Contexto**: Um administrador deseja ver o histórico de entradas de veículos.

**Entrada**:
- Navegue até a tela de histórico (`janelaHistorico`).

**Ação**:
- A tabela é carregada automaticamente.

**Saída Esperada**:
- A tabela (`tableWidget`) exibe:
  ```
  Placa: ABC1234 | Data: 2025-04-16 | Hora: 10:30:45
  Placa: XYZ5678 | Data: 2025-04-16 | Hora: 11:15:22
  ```

### Exemplo 6: Monitoramento de Vagas

**Contexto**: O sistema monitora as vagas em tempo real.

**Entrada**:
- Na tela principal (`janelaADM`), as vagas estão sendo monitoradas pela `ContadorVagasThread`.

**Ação**:
- Um veículo ocupa a vaga `vagas1`.

**Saída Esperada**:
- O frame correspondente a `vagas1` muda para vermelho (`background-color: #c34a4d`).
- Outras vagas livres permanecem verdes (`background-color: #47c25c`).
- No console, aparece:
  ```
  {'vagas1': 'ocupado', 'vagas2': 'livre', 'vagas3': 'livre', 'vagas4': 'livre'}
  ```

### Exemplo 7: Reconhecimento de Placa

**Contexto**: A webcam detecta uma placa de veículo.

**Entrada**:
- A thread `LicensePlateThread` captura uma imagem da webcam, e o OCR extrai a placa `ABC1234`.

**Ação**:
- A placa é validada contra `tabelaplaca`.

**Saída Esperada**:
- Se a placa está na tabela, ela é registrada em `tabelahistorico`:
  ```
  Placa ABC1234 registrada com id_placa 1 na tabelahistorico.
  ```
- No banco de dados:
  - `tabelahistorico`: `(placa_id: 1, data: 2025-04-16, hora: 12:00:00)`

## Notas Adicionais

- **Performance**: O reconhecimento de placas pode ser sensível à qualidade da imagem e iluminação. Ajuste os parâmetros de filtro em `license_plate.py` (e.g., CLAHE, binarização) para melhorar a precisão.
- **Erros Comuns**:
  - **Câmera não encontrada**: Verifique se a webcam está conectada e o índice está correto.
  - **Erro de conexão com o banco**: Verifique as credenciais e se o MySQL está rodando.

---

## 1. Manutenção do Sistema xxxx

A manutenção do sistema envolve monitoramento, correção de bugs e implementação de melhorias. Esta seção detalha como reportar problemas e sugerir aprimoramentos.

### 1.1. Como Reportar Bugs ou Sugerir Melhorias

Para garantir que problemas sejam resolvidos e melhorias sejam implementadas de forma organizada, utilize um repositório GitHub (ou outra plataforma de controle de versão, se aplicável) para gerenciar issues. Siga as instruções abaixo:

#### 1.1.1. Reportando Bugs

1. **Acesse o Repositório**:
   - Vá até o repositório do projeto no GitHub (ex.: `https://github.com/usuario/projeto-estacionamento`).
   - Navegue até a aba **Issues**.

2. **Criar uma Nova Issue**:
   - Clique em **New Issue**.
   - Use o template de bug (se disponível) ou crie uma issue com o título claro, como: `[BUG] Falha no reconhecimento de placa em baixa iluminação`.

3. **Descreva o Bug**:
   Inclua as seguintes informações:
   - **Descrição**: Explique o problema encontrado (ex.: "O sistema não reconhece placas em condições de pouca luz").
   - **Passos para Reproduzir**: Liste os passos exatos para replicar o bug (ex.: "1. Execute `

System: main.py`; 2. Use a webcam em um ambiente com iluminação inferior a 50 lux; 3. A placa não é detectada").
   - **Comportamento Esperado**: Descreva o que deveria acontecer (ex.: "A placa deveria ser reconhecida com precisão").
   - **Comportamento Observado**: Detalhe o que ocorre (ex.: "A thread `LicensePlateThread` retorna string vazia").
   - **Ambiente**:
     - Sistema operacional (ex.: Windows 11).
     - Versão do Python (ex.: 3.9).
     - Versões das bibliotecas (ex.: `opencv-python==4.8.0`).
     - Hardware (ex.: webcam Logitech C920).
   - **Logs ou Capturas de Tela**: Anexe logs de erro (ex.: saída do console) ou capturas de tela, se aplicável.

4. **Adicione Labels**:
   - Use labels como `bug`, `urgent` ou `needs-triage` para categorizar a issue.

5. **Envie a Issue**:
   - Clique em **Submit new issue**. A equipe de manutenção será notificada.

#### 1.1.2. Sugerindo Melhorias

1. **Acesse a Aba Issues**:
   - No repositório, vá para **Issues** e clique em **New Issue**.

2. **Crie uma Issue de Melhoria**:
   - Use um título descritivo, como: `[FEATURE] Adicionar suporte a múltiplas webcams`.
   - Escolha o template de feature (se disponível) ou escreva manualmente.

3. **Descreva a Melhoria**:
   Inclua:
   - **Objetivo**: Explique o propósito da melhoria (ex.: "Permitir o uso de várias webcams para monitoramento simultâneo").
   - **Benefícios**: Detalhe as vantagens (ex.: "Maior flexibilidade em estacionamentos maiores").
   - **Implementação Sugerida**: Proponha uma abordagem técnica (ex.: "Modificar `ContadorVagasThread` para suportar lista de índices de câmeras").
   - **Impacto**: Liste possíveis impactos no sistema (ex.: "Pode aumentar o uso de CPU").
   - **Exemplo de Uso**: Descreva como a funcionalidade seria usada (ex.: "O administrador seleciona webcams na interface").

4. **Adicione Labels**:
   - Use labels como `enhancement` ou `feature-request`.

5. **Envie a Issue**:
   - Submeta a issue para discussão com a equipe.

**Exemplo de Issue de Bug**:
```markdown
**Título**: [BUG] Erro ao conectar ao banco de dados MySQL

**Descrição**: A função `conectar_db()` falha ao tentar conectar ao MySQL quando o servidor está em uma porta não padrão.

**Passos para Reproduzir**:
1. Configure o MySQL para rodar na porta 3307.
2. Execute `main.py`.
3. Tente fazer login na tela inicial.

**Comportamento Esperado**: A conexão com o banco deve ser estabelecida.

**Comportamento Observado**: Erro: `mysql.connector.errors.InterfaceError: 2003: Can't connect to MySQL server`.

**Ambiente**:
- SO: Ubuntu 20.04
- Python: 3.8
- mysql-connector-python: 8.0.33
- MySQL: 8.0.28

**Logs**:
```
Erro ao inserir na tabelahistorico: 2003: Can't connect to MySQL server on 'localhost:3307'
```
```

**Exemplo de Issue de Melhoria**:
```markdown
**Título**: [FEATURE] Exportar histórico para CSV

**Objetivo**: Adicionar funcionalidade para exportar o histórico de entradas (`tabelahistorico`) em formato CSV.

**Benefícios**: Facilita a análise de dados por administradores em ferramentas externas como Excel.

**Implementação Sugerida**:
- Adicionar botão "Exportar CSV" na tela `janelaHistorico`.
- Usar biblioteca `pandas` para converter resultados da consulta SQL em CSV.
- Salvar arquivo em diretório escolhido pelo usuário via `QFileDialog`.

**Impacto**: Pequeno aumento no tamanho do código e dependência adicional (`pandas`).

**Exemplo de Uso**:
- Usuário clica em "Exportar CSV" na tela de histórico.
- Seleciona diretório e salva arquivo `historico_2025-04-16.csv`.
```

---

## 2. Instruções para Testes

Testes são essenciais para garantir a estabilidade do sistema após alterações. O sistema ainda não possui uma suíte de testes automatizada, but esta seção propõe a criação de testes usando a biblioteca `pytest`. A estrutura sugerida para testes inclui verificações de funcionalidades críticas, como conexão ao banco de dados, reconhecimento de placas e monitoramento de vagas.

### 2.1. Configuração do Ambiente de Testes

1. **Instale o `pytest`**:
   ```bash
   pip install pytest
   ```

2. **Crie uma Estrutura de Diretórios**:
   Organize os testes em um diretório chamado `tests/` na raiz do projeto:
   ```
   projeto-estacionamento/
   ├── main.py
   ├── license_plate.py
   ├── contador_vagas.py
   ├── tests/
   │   ├── test_db.py
   │   ├── test_plate_recognition.py
   │   └── test_vagas.py
   └── requirements.txt
   ```

3. **Configure o Banco de Testes**:
   - Crie um banco de dados de teste (`countcore_test`) com a mesma estrutura do banco principal (`countcore`).
   - Modifique a função `conectar_db()` para aceitar uma configuração de teste (ex.: variável de ambiente `TEST_MODE`):
     ```python
     import os
     def conectar_db():
         db_name = "countcore_test" if os.getenv("TEST_MODE") else "countcore"
         return mysql.connector.connect(
             host="localhost",
             user="root",
             password="",
             database=db_name
         )
     ```

4. **Dependências para Testes**:
   - Instale bibliotecas adicionais, se necessário:
     ```bash
     pip install pytest-mock opencv-python-headless
     ```

### 2.2. Exemplos de Testes

Crie arquivos de teste no diretório `tests/`. Abaixo estão exemplos de testes para cada módulo.

#### 2.2.1. Testes para Conexão ao Banco (`test_db.py`)

```python
import pytest
import mysql.connector
from main import conectar_db, placa_db

def test_conectar_db():
    conn = conectar_db()
    assert conn.is_connected(), "Falha ao conectar ao banco de dados"
    conn.close()

def test_placa_db_success(mocker):
    mocker.patch('main.conectar_db', return_value=mocker.Mock())
    mock_cursor = mocker.Mock()
    mock_cursor.fetchone.return_value = (1,)
    mocker.patch('mysql.connector.connect.cursor', return_value=mock_cursor)
    placa_db("ABC1234", "2025-04-16", "12:00:00")
    mock_cursor.execute.assert_called_with(
        "INSERT INTO tabelahistorico (placa_id, data, hora) VALUES (%s, %s, %s)",
        (1, "2025-04-16", "12:00:00")
    )

def test_placa_db_placa_inexistente(mocker, capsys):
    mocker.patch('main.conectar_db', return_value=mocker.Mock())
    mock_cursor = mocker.Mock()
    mock_cursor.fetchone.return_value = None
    mocker.patch('mysql.connector.connect.cursor', return_value=mock_cursor)
    placa_db("XYZ5678", "2025-04-16", "12:00:00")
    captured = capsys.readouterr()
    assert "Placa XYZ5678 não encontrada na tabelaplaca" in captured.out
```

#### 2.2.2. Testes para Reconhecimento de Placas (`test_plate_recognition.py`)

```python
import pytest
import cv2
from license_plate import get_authorized_plates, preprocess_image, validate_plate

def test_get_authorized_plates(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.fetchall.return_value = [("ABC1234",), ("XYZ5678",)]
    mock_conn.cursor.return_value = mock_cursor
    mocker.patch('mysql.connector.connect', return_value=mock_conn)
    plates = get_authorized_plates()
    assert plates == ["ABC1234", "XYZ5678"]

def test_preprocess_image():
    image = cv2.imread("tests/sample_plate.jpg")
    filtered = preprocess_image(image)
    assert filtered is not None, "Filtro não aplicado corretamente"
    assert len(filtered.shape) == 2, "Imagem não convertida para escala de cinza"

def test_validate_plate():
    authorized = ["ABC1234", "XYZ5678"]
    assert validate_plate("ABC1234", authorized) == "AUTHORIZED"
    assert validate_plate("DEF9012", authorized) == "NOT AUTHORIZED"
```

#### 2.2.3. Testes para Monitoramento de Vagas (`test_vagas.py`)

```python
import pytest
import cv2
import numpy as np
from contador_vagas import ContadorVagasThread

def test_vaga_ocupada(mocker):
    mock_video = mocker.Mock()
    mock_video.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
    mocker.patch('cv2.VideoCapture', return_value=mock_video)
    thread = ContadorVagasThread()
    thread.status_vagas_signal = mocker.Mock()
    thread.run()
    thread.status_vagas_signal.emit.assert_called()
```

### 2.3. Executando Testes

1. **Navegue até o diretório do projeto**:
   ```bash
   cd projeto-estacionamento
   ```

2. **Execute os testes**:
   ```bash
   pytest tests/ -v
   ```

3. **Interprete os Resultados**:
   - Testes aprovados aparecem com `[OK]`.
   - Testes falhos mostram detalhes do erro (ex.: `AssertionError`).
   - Use `pytest --cov` (com `pytest-cov` instalado) para verificar a cobertura de código:
     ```bash
     pip install pytest-cov
     pytest tests/ --cov=.
     ```

4. **Testes Manuais**:
   - Para funcionalidades visuais (ex.: interface PyQt5), execute o sistema manualmente:
     ```bash
     python main.py
     ```
   - Teste cenários como login, registro de usuário, pesquisa, edição e visualização do histórico.

---

## 3. Fluxo de Contribuição

O fluxo de contribuição segue práticas padrão de desenvolvimento colaborativo, utilizando Git e GitHub. Ele envolve a criação de branches, pull requests (PRs) e revisões.

### 3.1. Configuração Inicial

1. **Fork do Repositório**:
   - Acesse o repositório (ex.: `https://github.com/usuario/projeto-estacionamento`).
   - Clique em **Fork** para criar uma cópia no seu perfil GitHub.

2. **Clone o Repositório**:
   ```bash
   git clone https://github.com/seu-usuario/projeto-estacionamento.git
   cd projeto-estacionamento
   ```

3. **Configure o Upstream**:
   ```bash
   git remote add upstream https://github.com/usuario/projeto-estacionamento.git
   ```

4. **Instale Dependências**:
   ```bash
   pip install -r requirements.txt
   ```
   Crie um `requirements.txt` com:
   ```
   pyqt5==5.15.9
   mysql-connector-python==8.0.33
   opencv-python==4.8.0
   numpy==1.24.3
   easyocr==1.7.1
   ```

### 3.2. Criando uma Contribuição

1. **Crie uma Branch**:
   - Use um nome descritivo, como `fix/bug-conexao-db` ou `feature/export-csv`:
     ```bash
     git checkout -b feature/nova-funcionalidade
     ```

2. **Faça as Alterações**:
   - Edite os arquivos necessários (`main.py`, `license_plate.py`, `contador_vagas.py`, etc.).
   - Adicione testes no diretório `tests/` para cobrir as mudanças.
   - Siga boas práticas:
     - Mantenha o código legível (use PEP 8).
     - Adicione comentários explicativos.
     - Evite alterações desnecessárias.

3. **Teste Localmente**:
   - Execute o sistema:
     ```bash
     python main.py
     ```
   - Execute os testes:
     ```bash
     pytest tests/
     ```

4. **Commit das Alterações**:
   - Use mensagens de commit claras:
     ```bash
     git add .
     git commit -m "feat: adicionar exportação de histórico para CSV"
     ```

5. **Push para o Repositório**:
   ```bash
   git push origin feature/nova-funcionalidade
   ```

### 3.3. Criando um Pull Request

1. **Acesse o GitHub**:
   - Vá ao seu fork no GitHub.
   - Clique em **Compare & pull request** na branch recém-enviada.

2. **Preencha o Pull Request**:
   - **Título**: Ex.: "Adicionar exportação de histórico para CSV".
   - **Descrição**:
     - Explique o propósito da mudança.
     - Liste issues relacionadas (ex.: "Resolve #12").
     - Descreva testes realizados (ex.: "Adicionado teste em `test_db.py`").
     - Inclua capturas de tela, se aplicável (ex.: nova interface).
   - Exemplo:
     ```markdown
     **Descrição**: Adiciona funcionalidade para exportar histórico em CSV na tela `janelaHistorico`.

     **Mudanças**:
     - Novo botão "Exportar CSV" em `histórico.ui`.
     - Função `export_to_csv` em `janelaHistorico`.
     - Teste em `tests/test_db.py`.

     **Testes**:
     - Testado localmente com MySQL 8.0.
     - Todos os testes do `pytest` passaram.

     **Issue**: #12
     ```

3. **Adicione Reviewers**:
   - Selecione membros da equipe como revisores, se aplicável.

4. **Submeta o PR**:
   - Clique em **Create pull request**.

### 3.4. Revisão e Merge

1. **Revisão**:
   - Revisores analisarão o código, verificando:
     - Conformidade com requisitos.
     - Qualidade do código (legibilidade, PEP 8).
     - Cobertura de testes.
   - Comentários podem solicitar ajustes (ex.: "Adicione validação para entradas vazias").

2. **Ajustes**:
   - Faça as alterações solicitadas na mesma branch:
     ```bash
     git add .
     git commit -m "fix: adicionar validação para entradas vazias"
     git push origin feature/nova-funcionalidade
     ```
   - O PR será atualizado automaticamente.

3. **Merge**:
   - Após aprovação, o PR será merged na branch principal (`main`).
   - A branch de feature pode ser deletada:
     ```bash
     git push origin --delete feature/nova-funcionalidade
     ```

### 3.5. Mantendo o Fork Atualizado

1. **Sincronize com o Upstream**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   git push origin main
   ```

2. **Resolva Conflitos**:
   - Se houver conflitos, edite os arquivos afetados, adicione as mudanças e continue o merge:
     ```bash
     git add .
     git merge --continue
     ```

---

## 4. Boas Práticas para Contribuição

- **Commits Atômicos**: Faça commits pequenos e focados em uma única mudança.
- **Testes Obrigatórios**: Sempre inclua testes para novas funcionalidades ou correções.
- **Documentação**: Atualize a documentação (ex.: README, guias) se necessário.
- **Comunicação**: Comente nas issues e PRs para esclarecer dúvidas ou justificar decisões.
- **Respeite o Estilo**: Siga o estilo de código existente (ex.: PEP 8, nomes de variáveis consistentes).

---

## 5. Problemas Comuns e Soluções

- **Erro de Conexão ao Banco**:
  - Verifique se o MySQL está rodando e as credenciais em `conectar_db()` estão corretas.
  - Ajuste a porta, se necessário (ex.: `port=3307`).

- **Falha no Reconhecimento de Placas**:
  - Ajuste parâmetros de filtro em `license_plate.py` (ex.: CLAHE, binarização).
  - Teste com imagens de alta qualidade em `tests/sample_plate.jpg`.

- **Webcam Não Detectada**:
  - Confirme o índice da webcam em `license_plate.py` (`cv2.VideoCapture(0)`) e `contador_vagas.py` (`cv2.VideoCapture(1)`).
  - Teste com `cv2.VideoCapture(0)` para verificar disponibilidade.

- **Testes Falhando**:
  - Verifique se o banco de teste (`countcore_test`) está configurado.
  - Execute `pytest` com `-v` for details do erro.

# FAQ e Solução de Problemas do Sistema de Gerenciamento de Estacionamento

## 1. FAQ (Perguntas Frequentes)

As perguntas abaixo abordam dúvidas comuns sobre a configuração, uso e funcionalidades do sistema.

### 1.1. Como configurar o sistema pela primeira vez?
**Resposta**:  
Para configurar o sistema, siga estes passos:  
1. **Instale as dependências**:
   ```bash
   pip install pyqt5 mysql-connector-python opencv-python numpy pytesseract
   ```
2. **Instale o Tesseract OCR**:  
   - Baixe e instale o Tesseract (disponível em: [Tesseract OCR GitHub](https://github.com/tesseract-ocr/tesseract)).  
   - Configure o caminho do executável em `app.py`, se necessário.  
3. **Configure o banco de dados MySQL**:  
   - Crie o banco `countcore` e as tabelas necessárias:
     ```sql
     CREATE DATABASE countcore;
     USE countcore;
     CREATE TABLE tabelaadm (nome VARCHAR(50), senha VARCHAR(50));
     CREATE TABLE tabelausuario (id_usuario INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(100));
     CREATE TABLE tabelaplaca (placa VARCHAR(10), usuario_id INT, FOREIGN KEY (usuario_id) REFERENCES tabelausuario(id_usuario));
     CREATE TABLE tabelafoto (link_foto VARCHAR(255), usuario_id INT, FOREIGN KEY (usuario_id) REFERENCES tabelausuario(id_usuario));
     CREATE TABLE tabelahistorico (placa_id INT, data DATE, hora TIME, FOREIGN KEY (placa_id) REFERENCES tabelaplaca(id_placa));
     ```
4. **Verifique as webcams**:  
   - Conecte duas webcams (índice 0 para reconhecimento de placas em `app.py`, índice 1 para monitoramento de vagas em `contadorVagas.py`).  
5. **Execute o sistema**:
   ```bash
   python main.py
   ```

### 1.2. Como fazer login no sistema?
**Resposta**:  
- Na tela inicial (`janelaInicial`), insira o nome de usuário e senha registrados na tabela `tabelaadm` do banco `countcore`.  
- Exemplo:
  - Nome: `admin`
  - Senha: `12345`  
- Clique em **Entrar**. Se as credenciais estiverem incorretas, uma mensagem de erro será exibida.

### 1.3. Como registrar um novo usuário?
**Resposta**:  
1. Acesse a tela de registro pelo menu **Registrar** na interface principal (`janelaADM`).  
2. Na tela de registro (`janelaRegistro`):  
   - Insira o **nome** do usuário.  
   - Insira a **placa** do veículo (ex.: `ABC1234`).  
   - Clique na área de imagem para selecionar uma foto (formatos: `.png`, `.jpg`, `.jpeg`, `.bmp`).  
3. Clique em **Registrar**.  
Os dados serão salvos nas tabelas `tabelausuario`, `tabelaplaca` e `tabelafoto`.

### 1.4. O que acontece quando uma placa é reconhecida?
**Resposta**:  
- A thread `LicensePlateThread` em `app.py` captura vídeo da webcam (índice 0), aplica filtros (escala de cinza e limiarização) e usa Tesseract OCR para extrair o número da placa.  
- Se a placa estiver na tabela `tabelaplaca`, ela é considerada autorizada, e um registro é adicionado à `tabelahistorico` com a placa, data e hora.  
- Caso contrário, uma mensagem é exibida no console: `Placa {placa} não encontrada na tabelaplaca`.

### 1.5. Como o monitoramento de vagas funciona?
**Resposta**:  
- A thread `ContadorVagasThread` em `contadorVagas.py` usa uma webcam (índice 1) para monitorar quatro vagas predefinidas.  
- Cada vaga é analisada por meio de processamento de imagem (conversão para cinza, limiarização adaptativa, desfoque e dilatação).  
- Se a quantidade de pixels brancos em uma vaga exceder 150, ela é marcada como **ocupada** (vermelho na interface); caso contrário, é **livre** (verde).

### 1.6. Posso usar arquivos de vídeo em vez de webcams?
**Resposta**:  
- Sim, modifique o código em `app.py` e `contadorVagas.py` para usar arquivos de vídeo:  
  - Em `app.py`, altere `cv2.VideoCapture(0)` para `cv2.VideoCapture("caminho/para/video.mp4")`.  
  - Em `contadorVagas.py`, altere `cv2.VideoCapture(1)` para `cv2.VideoCapture("caminho/para/video.mp4")`.  
- Certifique-se de que o vídeo tenha resolução e iluminação adequadas.

### 1.7. Como visualizar o histórico de entradas?
**Resposta**:  
- Acesse a tela de histórico pelo menu **Histórico** na interface principal.  
- A tabela exibe os registros da `tabelahistorico`, incluindo `placa_id`, `data` e `hora`.  
- Para atualizar, recarregue a tela selecionando **Histórico** novamente.

### 1.8. Como editar ou excluir um usuário?
**Resposta**:  
- Acesse a tela de perfil pelo menu **Perfil**.  
- **Pesquisa**: Digite o nome ou ID do usuário e clique em **Pesquisar**.  
- **Edição**: Selecione o usuário, clique em **Editar**, modifique os campos (nome, placa, foto) e clique em **Aplicar**.  
- **Exclusão**: Selecione o usuário e clique em **Deletar**. Isso remove os registros associados nas tabelas `tabelausuario`, `tabelaplaca` e `tabelafoto`.

### 1.9. Como reportar um problema ou sugerir melhorias?
**Resposta**:  
- Crie uma issue no repositório do projeto no GitHub (se disponível, ex.: `https://github.com/usuario/projeto-estacionamento`).  
- Para bugs, inclua: descrição, passos para reproduzir, comportamento esperado, logs e ambiente.  
- Para melhorias, descreva o objetivo, benefícios e sugestões de implementação.  
- Veja a seção de [Manutenção e Contribuição](#) para mais detalhes.

---

## 2. Problemas Comuns e Suas Soluções

Abaixo estão os problemas mais frequentes encontrados ao usar o sistema, com suas respectivas soluções.

### 2.1. Erro: "Can't connect to MySQL server on 'localhost'"
**Descrição**: O sistema não consegue conectar ao banco de dados MySQL ao executar `main.py`.  
**Causa**: Servidor MySQL não está rodando, credenciais incorretas ou configuração inadequada.  
**Solução**:  
1. Verifique se o MySQL está ativo:
   ```bash
   sudo systemctl status mysql  # Linux
   net start mysql              # Windows
   ```
   Inicie o serviço, se necessário:
   ```bash
   sudo systemctl start mysql  # Linux
   net start mysql             # Windows
   ```
2. Confirme as credenciais em `conectar_db()` (`main.py` e `app.py`):
   - Host: `localhost`
   - Usuário: `root`
   - Senha: `""` (vazia, ou ajuste para sua senha)
   - Banco: `countcore`
3. Certifique-se de que o banco `countcore` existe:
   ```sql
   CREATE DATABASE countcore;
   ```
4. Teste a conexão manualmente:
   ```bash
   mysql -u root -p
   ```
5. Se o MySQL usa uma porta não padrão (ex.: 3307), modifique `conectar_db()`:
   ```python
   return mysql.connector.connect(
       host="localhost",
       user="root",
       password="",
       database="countcore",
       port=3307
   )
   ```

**Recurso Externo**: [MySQL Documentation - Connection Issues](https://dev.mysql.com/doc/refman/8.0/en/can-not-connect-to-server.html)

### 2.2. Erro: "No such file or directory: 'paginaInicial.ui'"
**Descrição**: O sistema falha ao carregar a interface gráfica com erro de arquivo `.ui` não encontrado.  
**Causa**: Arquivos `.ui` (ex.: `paginaInicial.ui`, `telaADM.ui`) não estão no diretório do projeto.  
**Solução**:  
1. Verifique se os arquivos `.ui` estão na mesma pasta que `main.py`. Estrutura esperada:
   ```
   projeto/
   ├── main.py
   ├── app.py
   ├── contadorVagas.py
   ├── paginaInicial.ui
   ├── telaADM.ui
   ├── PaginadePesquisa.ui
   ├── histórico.ui
   ├── Perfil.ui
   ├── ADMResgistrar.ui
   ├── QDialogEditar.ui
   └── lib/
       ├── filters.py
       └── format_output.py
   ```
2. Se os arquivos estiverem em outro diretório, atualize o caminho em `uic.loadUi()`:
   ```python
   uic.loadUi("caminho/para/paginaInicial.ui", self)
   ```
3. Caso os arquivos `.ui` estejam faltando, gere-os com o **Qt Designer**:
   - Instale o PyQt5 Designer:
     ```bash
     pip install pyqt5-tools
     ```
   - Crie ou edite interfaces com `designer.exe` (Windows) ou `designer` (Linux/macOS).
   - Salve os arquivos `.ui` no diretório correto.

**Recurso Externo**: [PyQt5 Documentation - Using Qt Designer](https://www.riverbankcomputing.com/static/Docs/PyQt5/designer.html)

### 2.3. Erro: "Erro: Não foi possível abrir a câmera"
**Descrição**: Mensagem no console indicando falha ao acessar a webcam em `app.py` ou `contadorVagas.py`.  
**Causa**: Webcam não conectada, índice incorreto ou drivers ausentes.  
**Solução**:  
1. Confirme que as webcams estão conectadas:
   - Índice 0 (`app.py`) para reconhecimento de placas.
   - Índice 1 (`contadorVagas.py`) para monitoramento de vagas.
2. Teste os índices das webcams:
   ```python
   import cv2
   cap = cv2.VideoCapture(0)  # Teste índice 0
   if cap.isOpened():
       print("Webcam 0 OK")
   else:
       print("Webcam 0 falhou")
   cap.release()
   ```
   Repita para índice 1. Se necessário, ajuste os índices em:
   - `app.py`: `cv2.VideoCapture(0)`
   - `contadorVagas.py`: `cv2.VideoCapture(1)`
3. Verifique os drivers da webcam:
   - Windows: Atualize drivers no Gerenciador de Dispositivos.
   - Linux: Instale `v4l2loopback` se necessário:
     ```bash
     sudo apt-get install v4l2loopback-dkms
     ```
4. Use um arquivo de vídeo para testes:
   ```python
   cap = cv2.VideoCapture("caminho/para/video.mp4")
   ```

**Recurso Externo**: [OpenCV Documentation - VideoCapture](https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html)

### 2.4. Problema: Placas não são reconhecidas corretamente
**Descrição**: A thread `LicensePlateThread` não detecta placas ou retorna strings incorretas.  
**Causa**: Iluminação inadequada, configuração do Tesseract OCR ou filtros mal ajustados.  
**Solução**:  
1. **Melhore a iluminação**:
   - Certifique-se de que a área da webcam tem iluminação uniforme (mínimo 100 lux).  
   - Evite sombras ou reflexos na placa.  
2. **Verifique o Tesseract OCR**:
   - Confirme que o Tesseract está instalado e configurado:
     ```bash
     tesseract --version
     ```
   - Ajuste o caminho em `app.py`, se necessário:
     ```python
     pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Windows
     ```
3. **Ajuste os filtros**:
   - Em `app.py`, modifique `apply_filter()` para melhorar o contraste:
     ```python
     def apply_filter(plate):
         gray = get_grayscale(plate)
         thresh = thresholding(gray)
         thresh = cv2.GaussianBlur(thresh, (5, 5), 0)  # Adicione desfoque
         return thresh
     ```
4. **Teste com imagens estáticas**:
   - Substitua a captura de vídeo por uma imagem de teste:
     ```python
     frame = cv2.imread("tests/placa_teste.jpg")
     ```
   - Analise o resultado de `scan_plate(frame)` no console.

**Recurso Externo**: [Tesseract OCR Documentation](https://tesseract-ocr.github.io/docs/)

### 2.5. Problema: Monitoramento de vagas marca vagas incorretamente
**Descrição**: Vagas são exibidas como ocupadas ou livres de forma errada na interface (`janelaADM`).  
**Causa**: Limiar de pixels brancos mal configurado ou coordenadas das vagas incorretas.  
**Solução**:  
1. **Ajuste o limiar de pixels**:
   - Em `contadorVagas.py`, modifique o valor em `qtPxBranco > 150`:
     ```python
     if qtPxBranco > 200:  # Aumente ou diminua conforme necessário
         status_vagas[nome] = "ocupado"
     else:
         status_vagas[nome] = "livre"
     ```
   - Teste valores entre 100 e 300, dependendo da iluminação e resolução.  
2. **Verifique as coordenadas das vagas**:
   - Em `contadorVagas.py`, ajuste as coordenadas em `vagas`:
     ```python
     vagas = {
         "vagas1": [108, 236, 90, 34],
         "vagas2": [224, 232, 128, 36],
         "vagas3": [221, 298, 107, 42],
         "vagas4": [92, 304, 118, 45]
     }
     ```
   - Use um script para visualizar as regiões:
     ```python
     import cv2
     cap = cv2.VideoCapture(1)
     ret, img = cap.read()
     for nome, (x, y, w, h) in vagas.items():
         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
     cv2.imshow("Vagas", img)
     cv2.waitKey(0)
     cap.release()
     cv2.destroyAllWindows()
     ```
3. **Melhore a iluminação**:
   - Certifique-se de que o estacionamento está bem iluminado para evitar falsos positivos.

**Recurso Externo**: [OpenCV Image Processing Tutorial](https://docs.opencv.org/4.x/d9/df8/tutorial_py_image_processing.html)

### 2.6. Erro: "Usuário ou Senha errado" mesmo com credenciais corretas
**Descrição**: A tela de login exibe erro, apesar de usar credenciais válidas.  
**Causa**: Bug na lógica de autenticação ou dados ausentes na tabela `tabelaadm`.  
**Solução**:  
1. **Verifique a lógica de login**:
   - Em `janelaInicial.Entrar`, a condição `if True` ignora o resultado da consulta SQL:
     ```python
     resultado = cursor.fetchone()
     conn.close()
     if resultado:  # Corrija para verificar o resultado
         self.janela_adm = janelaADM()
         self.janela_adm.show()
         self.close()
     else:
         QtWidgets.QMessageBox.warning(self, "Erro", "Usuário ou Senha errado")
     ```
2. **Confira os dados no banco**:
   - Acesse o MySQL e verifique a tabela `tabelaadm`:
     ```sql
     SELECT * FROM tabelaadm;
     ```
   - Insira credenciais de teste, se necessário:
     ```sql
     INSERT INTO tabelaadm (nome, senha) VALUES ('admin', '12345');
     ```
3. **Teste a consulta manualmente**:
   - Execute no MySQL:
     ```sql
     SELECT * FROM tabelaadm WHERE nome = 'admin' AND senha = '12345';
     ```

**Recurso Externo**: [PyQt5 QMessageBox Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtWidgets/qmessagebox.html)

### 2.7. Problema: Interface gráfica não responde ou trava
**Descrição**: A aplicação fica lenta ou não responde ao navegar entre telas.  
**Causa**: Threads (`LicensePlateThread`, `ContadorVagasThread`) consomem muitos recursos ou erro na gestão de janelas.  
**Solução**:  
1. **Reduza a carga das threads**:
   - Em `app.py`, aumente o intervalo de captura:
     ```python
     cv2.waitKey(100)  # De 1ms para 100ms
     ```
   - Em `contadorVagas.py`, ajuste o intervalo:
     ```python
     cv2.waitKey(50)  # De 10ms para 50ms
     ```
2. **Evite múltiplas instâncias de janelas**:
   - Nos métodos de navegação (ex.: `Inicio`, `Pesquisa`), modifique para reutilizar janelas:
     ```python
     def Inicio(self):
         if not hasattr(self, 'janela_adm') or not self.janela_adm.isVisible():
             self.janela_adm = janelaADM()
         self.janela_adm.show()
         self.hide()  # Esconde em vez de fechar
     ```
3. **Monitore o uso de recursos**:
   - Use o Gerenciador de Tarefas (Windows) ou `htop` (Linux) para verificar CPU e memória.  
   - Reduza a resolução das webcams, se necessário:
     ```python
     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
     ```

**Recurso Externo**: [PyQt5 Threading Guide](https://www.pythonguis.com/faq/pyqt5-threading/)

### 2.8. Erro: "Erro ao inserir na tabelahistorico"
**Descrição**: Mensagem no console indicando falha ao registrar uma placa em `placa_db`.  
**Causa**: Placa não existe na tabela `tabelaplaca` ou erro na estrutura do banco.  
**Solução**:  
1. **Verifique a placa**:
   - Confirme se a placa detectada está na tabela `tabelaplaca`:
     ```sql
     SELECT * FROM tabelaplaca WHERE placa = 'ABC1234';
     ```
   - Adicione a placa, se necessário:
     ```sql
     INSERT INTO tabelaplaca (placa, usuario_id) VALUES ('ABC1234', 1);
     ```
2. **Cheque a estrutura do banco**:
   - Verifique se `tabelahistorico` tem as colunas corretas:
     ```sql
     DESCRIBE tabelahistorico;
     ```
   - Recrie a tabela, se necessário (veja FAQ 1.1).  
3. **Depure a função**:
   - Adicione logs detalhados em `placa_db`:
     ```python
     print(f"Tentando inserir: placa={placa}, data={data}, hora={hora}")
     ```

**Recurso Externo**: [MySQL Connector/Python Documentation](https://dev.mysql.com/doc/connector-python/en/)

## 3. Links para Recursos Externos

- **PyQt5 Documentation**: [https://www.riverbankcomputing.com/static/Docs/PyQt5/](https://www.riverbankcomputing.com/static/Docs/PyQt5/)  
  Guia oficial para desenvolvimento de interfaces gráficas com PyQt5.  
- **OpenCV Documentation**: [https://docs.opencv.org/4.x/](https://docs.opencv.org/4.x/)  
  Referência para processamento de imagens e captura de vídeo.  
- **Tesseract OCR Documentation**: [https://tesseract-ocr.github.io/docs/](https://tesseract-ocr.github.io/docs/)  
  Instruções para configuração e uso do Tesseract para reconhecimento de texto.  
- **MySQL Documentation**: [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)  
  Documentação oficial para configuração e gerenciamento do MySQL.  
- **Python Official Documentation**: [https://docs.python.org/3/](https://docs.python.org/3/)  
  Referência para Python, incluindo gerenciamento de dependências e boas práticas.  
- **Stack Overflow**: [https://stackoverflow.com/](https://stackoverflow.com/)  
  Comunidade para suporte técnico em Python, PyQt5, OpenCV e MySQL.

[Repositório Github]([https://github.com/Baima-Rafael/Trabalho-Senac-Provavelmente-Final/tree/main](https://github.com/Baima-Rafael/Trabalho-PI-Senac))
