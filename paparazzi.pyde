from util import ponto
from drone import Drone
from oito import Oito

# Variáveis Globais
f      = 0
drones = []
p8     = None
windA  = 90
windF  = 0.5

def setup():                        # Inicializa variáveis globais, frequencia e tamanho da tela
    global p8
    frameRate(10)
    size(1200, 800)
    d = Drone(1)    
    p8 = Oito(width/2, height/2, 200)
    d.set_mission(p8)
    drones.append(d)

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
    global f
    background(255)       # Fundo branco
    fill(0)
    # ellipse(width/2, height/2, 10, 10)
    f += 1
    f = f % len(drones)
    p8.paint()
    wind = wind_control()
    
    for i in range(len(drones)):
        drones[(i+f) % len(drones)].wind = wind
        drones[(i+f) % len(drones)].execute()
    
    print('---')

def mouseClicked():
    global p8, windA
    if mouseX > 52 or mouseY > 52:
        p8 = Oito(mouseX, mouseY, 150)
        for i in range(len(drones)):
            drones[i].set_mission(p8)
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
    if key == 'd':
        d = Drone(len(drones)+1)
        d.set_mission(p8)
        drones.append(d)
    if key == 'r':
        p8.show = (p8.show+1)%2
        for i in range(len(drones)):
            drones[i].radarOn = (drones[i].radarOn+1) % 2
