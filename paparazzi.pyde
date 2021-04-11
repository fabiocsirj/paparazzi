from util import ponto
from drone import Drone
from oito import Oito

# Variáveis Globais
d1 = None
p8 = None

def setup():                        # Inicializa variáveis globais, frequencia e tamanho da tela
    global d1, p8
    frameRate(30)
    size(1200, 800)
    d1 = Drone()
    p8 = Oito(width/2, height/2, 200)
    d1.set_mission(p8)

def draw():
    background(255)   # Fundo branco
    p8.paint()        # Desenha 8 de Paparazzi
    d1.execute()      # Executa missao
    print('Velocidade:', d1.velo.mag())
    print('---')

def mouseClicked():
    global p8
    p8 = Oito(mouseX, mouseY, 150)
    d1.set_mission(p8)
