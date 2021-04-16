from drone import Drone
from path_eight import Path_eight
from path_oval import Path_oval
from path_stayat import Path_stayat
from path_waypoint import Path_waypoint
from path_scan import Path_scan

# Variáveis Globais
f      = 0
drones = []
path   = []
p      = 0
labels = ['Paparazzi Eight', 'Paparazzi Oval', 'Paparazzi Stay At', 'Paparazzi Waypoint', 'Paparazzi Scan']
center = None
windA  = 90
windF  = 0.5
obs    = []
obsOn  = 0

def setup():                        # Inicializa variáveis globais, frequencia e tamanho da tela
    global center
    frameRate(10)
    size(1200, 800)
    path.append(Path_eight())
    path.append(Path_oval())
    path.append(Path_stayat())
    path.append(Path_waypoint())
    path.append(Path_scan())
    
    d = Drone(1)
    center = PVector(width/2, height/2)
    path[p].setWP(center)
    d.set_mission(path[p])
    drones.append(d)

def wind_control():
    centro = PVector(27, 27)
    fill(255)
    stroke(0)
    ellipse(centro.x, centro.y, 50, 50)
    fill(0)
    ellipse(centro.x, centro.y, 5, 5)
    p = PVector(25*cos(windA/(180/PI)), 25*sin(windA/(180/PI)))
    line(centro.x, centro.y, centro.x-p.x, centro.y-p.y);
    textSize(12)
    text("Wind: {}".format(windF), 2, 62)
    text('[+/-] change force ', 2, 74)

    wind = p.limit(windF)
    return wind

def draw():
    global f
    background(255)       # Fundo branco
    fill(0)
    if obsOn: text('Set Obstacle', 500, 12)
    else: text(labels[p], 500, 20)
    text('Press: [d] add drone | [r] on/off radar mode | [p] change mission', 2, 778)
    text('Press: [o] add obstacle or set center mission with mouse click', 2, 790)
    
    f += 1
    f = f % len(drones)
    path[p].paint()
    
    if obsOn:
        fill(0)
        for o in obs:
            ellipse(o.x, o.y, 20, 20)
            
    wind = wind_control()
    for i in range(len(drones)):
        drones[(i+f) % len(drones)].wind = wind
        drones[(i+f) % len(drones)].execute()
    print('---')

def mouseClicked():
    global center, windA
    click  = PVector(mouseX, mouseY)
    if mouseX > 52 or mouseY > 52:
        if obsOn:
            obs.append(click)
        else:
            center = click
            set_mission()
    else:
        centro = PVector(27, 27)
        posToCenter = PVector.sub(centro, click)
        ctp = posToCenter.normalize(None).mult(25)
        centerToPerim = PVector(ctp.x, ctp.y)
        theta = atan2(centerToPerim.y, centerToPerim.x)
        windA = theta * (180/PI)

def set_mission():
    path[p].setWP(center)
    for i in range(len(drones)):
        drones[i].set_mission(path[p])

def keyPressed():
    global windF
    if key == '=': windF += 1.5
    if key == '-': windF -= 0.5
    
    if key == 'd':
        d = Drone(len(drones)+1)
        d.set_mission(path[p])
        drones.append(d)
        
    if key == 'r':
        path[p].show = (path[p].show+1)%2
        for i in range(len(drones)):
            drones[i].radarOn = (drones[i].radarOn+1) % 2
    
    if key == 'p':
        global p
        p = (p+1) % len(path)
        set_mission()
    
    if key == 'o':
        global obsOn
        obsOn = (obsOn+1)%2
