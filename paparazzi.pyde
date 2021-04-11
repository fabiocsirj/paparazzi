from util import ponto
from drone import Drone
from oito import Oito

# Variáveis Globais
d1    = None
p8    = None
windA = 90
windF = 0.5

def setup():                        # Inicializa variáveis globais, frequencia e tamanho da tela
    global d1, p8
    frameRate(30)
    size(1200, 800)
    d1 = Drone()
    p8 = Oito(width/2, height/2, 200)
    d1.set_mission(p8)

def wind_control():
    centro = PVector(27, 27)
    fill(255)
    stroke(0)
    ellipse(centro.x, centro.y, 50, 50)
    fill(0)
    ellipse(centro.x, centro.y, 5, 5)
    p = ponto(25, windA)
    line(centro.x, centro.y, centro.x-p.x, centro.y-p.y);
    textSize(12)
    text("Wind: {}".format(windF), 2, 62)

    wind = p.limit(windF)
    return wind

def draw():
    background(255)       # Fundo branco
    p8.paint()            # Desenha 8 de Paparazzi
    wind = wind_control()
    d1.wind = wind
    d1.execute()          # Executa missao
    print('Velocidade:', PVector.sub(wind, d1.velo).limit(6).mag())
    print('---')

def mouseClicked():
    global p8, windA
    if mouseX > 52 or mouseY > 52:
        p8 = Oito(mouseX, mouseY, 150)
        d1.set_mission(p8)
    else:
        centro = PVector(27, 27)
        click  = PVector(mouseX, mouseY)
        posToCenter = PVector.sub(centro, click)
        ctp = posToCenter.normalize(None).mult(25)
        centerToPerim = PVector(ctp.x, ctp.y)
        theta = atan2(centerToPerim.y, centerToPerim.x)
        windA = theta * (180/PI)

def keyPressed():
    global windF
    if key == '=': windF += 2
    if key == '-': windF -= 0.5
