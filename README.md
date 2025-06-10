# 🖐️ Controle por Gestos com IA: Mouse Virtual e FisioTrack

Este repositório documenta a evolução de um projeto de visão computacional, desde um **Mouse Virtual** controlado por gestos até uma ferramenta de **Análise de Movimento e Gamificação para Fisioterapia**, o **FisioTrack**. O objetivo é demonstrar a aplicação prática da Inteligência Artificial, especificamente o rastreamento de mãos com MediaPipe, para criar soluções interativas e funcionais.

Este projeto é um exemplo prático da união entre a **Engenharia de Software** e a **Fisioterapia**, mostrando como a tecnologia pode ser usada para criar ferramentas de avaliação clínica, reabilitação e acompanhamento de pacientes.

---

## Índice

* [Tecnologias Utilizadas](#-tecnologias-utilizadas)
* [Como Configurar o Ambiente](#-como-configurar-o-ambiente)
* [Projeto 1: Mouse Virtual](#-projeto-1-mouse-virtual)
* [Projeto 2: FisioTrack - Reabilitação Gamificada](#-projeto-2-fisiotrack---reabilitação-gamificada)
* [Autor](#-autor)

---

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído utilizando as seguintes bibliotecas e tecnologias:

* **Python 3.11+**
* **OpenCV:** Para captura de vídeo, manipulação de imagem e desenho de elementos na tela.
* **MediaPipe:** Para o rastreamento de alta fidelidade dos pontos de referência da mão em tempo real.
* **NumPy:** Para cálculos numéricos e manipulação da estrutura das imagens.
* **PyAutoGUI:** Para interagir com o sistema operacional (descobrir a resolução da tela).
* **Pygame:** Para a implementação de feedback sonoro no FisioTrack.

---

## ⚙️ Como Configurar o Ambiente

Siga os passos abaixo para executar os projetos em sua máquina.

**1. Pré-requisitos:**
* Ter o [Python](https://www.python.org/downloads/) instalado.
* Ter o [Git](https://git-scm.com/downloads) instalado.
* Uma webcam conectada ao computador.

**2. Clone o Repositório:**
```sh
git clone [https://github.com/dev-netinho/Fisioterapia-X-EngenhariaDeSoftware]
cd Fisioterapia-X-EngenhariaDeSoftware
```

**3. Instale as Dependências:**
Recomenda-se criar um ambiente virtual. Depois, instale todas as bibliotecas necessárias com um único comando:
```sh
pip install opencv-python mediapipe numpy pyautogui pygame
```

**4. Arquivos de Áudio (Para o FisioTrack):**
Para que os sons do FisioTrack funcionem, coloque dois arquivos de áudio na pasta raiz do projeto com os seguintes nomes:
* `hit.wav` (som para acerto de alvo)
* `finish.wav` (som para conclusão do exercício)

---

## 🖱️ Projeto 1: Mouse Virtual

Esta foi a primeira versão do projeto, uma prova de conceito para controlar o cursor do mouse do sistema operacional através de gestos.

### Funcionalidades
* **Movimento do Cursor:** A ponta do dedo indicador controla a posição do mouse na tela.
* **Clique:** O gesto de pinça entre o polegar e o dedo indicador executa um clique.

### Como Executar
```sh
python "Mouse Virtual.py"
```

## 🩺 Projeto 2: FisioTrack - Reabilitação Gamificada

Esta é a versão final e mais avançada do projeto, transformada em uma ferramenta de software voltada para a Fisioterapia.

### Funcionalidades
* **Interface Imersiva:** O programa roda em tela cheia, usando o vídeo da câmera como fundo.
* **Exercício Gamificado:** O usuário deve mover a mão para tocar em alvos que aparecem na tela, treinando amplitude de movimento e coordenação.
* **Feedback em Tempo Real:**
    * **Visual:** O cursor do dedo é destacado, e os alvos são visíveis sobre o vídeo.
    * **Sonoro:** Efeitos sonoros para acerto de alvo e para o final do exercício, aumentando o engajamento.
* **Análise de Desempenho:** Ao final do exercício (atingindo a pontuação máxima), uma tela de resultados é exibida com métricas objetivas:
    * Pontuação Final
    * Tempo Total do Exercício
    * Tempo Médio por Alvo
    * **Eficiência Média do Movimento (%)**: Uma métrica avançada que mede a qualidade do controle motor do usuário.
* **Geração de Relatórios (CSV):** Todos os resultados da sessão são salvos automaticamente em um arquivo `.csv` (planilha), com data e hora no nome do arquivo. Isso permite o acompanhamento clínico do progresso do paciente ao longo do tempo.
* **Ciclo Completo:** O usuário pode reiniciar o exercício ou sair do programa após a conclusão.

### Como Executar
```sh
python fisiotrack.py
```


## 👤 Autor

* **José Neto**
* **GitHub:** [https://github.com/dev-netinho](https://github.com/dev-netinho)
* **LinkedIn:** `https://www.linkedin.com/in/jose-gc-neto/`