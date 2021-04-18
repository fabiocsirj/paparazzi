class Drone:
    def __init__(self, id):
        self.id       = id
        self.pos      = PVector(random(width), random(height)) # Posicao inicial aleatoria
        self.velo     = PVector(0, 0)                          # Velociade inicial
        self.maxSpeed = 0.2                                    # Define a velocidade maxima inicial
        self.mission  = None                                   # Configura a missao
        self.alvo     = None                                   # Alvo inicial
        self.wind     = PVector(0, 0)                          # Vento inicial
        self.radarOn  = 0
        
        # Variaveis auxiliares de colisao
        self._obstacles = []
        self.printObs   = 0
        self.timeRadar  = 0
        
        # Variaveis auxiliares para o seek
        self._wp     = 0
        self._path   = False
        self._orbita = None

    def set_mission(self, m):
        self.mission = m
        self.alvo    = None
        self._wp     = 0
        self._path   = False
        self._orbita = None

    def _paint(self):                                      # Desenha um Drone ajustando o angulo do setor anterior para simular direcao
        if self.velo.mag() > 0: angulo = self.velo.heading() + PI/2
        else: angulo = 0
        pushMatrix()
        translate(self.pos.x, self.pos.y)
        rotate(angulo)
        img = loadImage("drone4.png")
        if self.printObs:
            fill(255, 0, 255) 
            ellipse(0, 20, 5, 5)
        image(img, -37, 0)
        fill(255)
        text("{}".format(self.id), -5, 37)
        popMatrix()

    def execute(self):
        if self.mission != None:
            self._seek()

            # DEFINE A DIRECAO
            direcao = PVector.sub(self.alvo, self.pos)          # Direcao = a diferenca entre o alvo e a posicao atual
            distancia = direcao.mag()                           # Define a Distancia
            # print('Distancia:',distancia)
            
            self.maxSpeed = min(6, self.maxSpeed+0.2)           # Aceleracao gradual
            if not self._path and distancia < 70: 
                self.maxSpeed = map(distancia, 0, 70, 0.1, 6)   # Desaceleracao gradual para entrar no path

            # print('max speed:', self.maxSpeed)
            direcao.limit(self.maxSpeed)                        # Limita o salto de direcao pela velocidade estabelecida acima
            ##################

            # DEFINE A ACELERACAO
            acelera = PVector.sub(direcao, self.velo)           # Aceleracao e a diferenca entre a direcao e a velocidade atual
            acelera.limit(0.32)                                 # Suaviza Transicao
            # print('Aceleracao:', acelera)
            #####################

            # DEFINE A VELOCIDADE
            self.velo.add(acelera)                              # Adiciona a aceleracao a velocidade atual
            self.velo.limit(self.maxSpeed)                      # Limita a velocidade a maxima permitida
            print("V {}: {}".format(self.id, self.velo.mag()))
            #####################
            
            # ATUALIZA POSICAO
            self.pos.add(self.velo)                             # Atualiza a posicao adicionando a velocidade a posicao atual
            ##################

            # Obstaculos
            if len(self._obstacles):
                self.timeRadar = (self.timeRadar+1) % 100
                for o in self._obstacles:
                    if self.printObs:
                        fill(255,0,255)
                        ellipse(o.x, o.y, 10, 10)
                    d = PVector.sub(o, self.pos)
                    d.limit(map(PVector.dist(o, self.pos), 0, 100, 3, 0))
                    self.pos.sub(d)
                    if PVector.dist(o, self.pos) > 100: self._obstacles.remove(o)
                    elif self._obstacles.index(o) == self.timeRadar: self._obstacles.remove(o)
            ############

            # Pertubacao do vento
            self.pos.sub(self.wind)
            #####################
            
            # DESEHA O DRONE NA TELA
            self._paint()
            ##########################
            
            # Radar
            if self.radarOn: self.radar()
            else: self._targuet()
            #######

    def _seek(self):
        if not self._path:                              # Se nao esta no path
            if not self.alvo:                           # Se nao temn alvo, define-o para o waypoint mais proximo
                perto = self.mission.waypoints[0]
                dis_p = PVector.dist(perto, self.pos)
                for wp in self.mission.waypoints:
                    d = PVector.dist(wp, self.pos) 
                    if d < dis_p:
                        perto = wp
                        dis_p = d
                self.alvo = perto
                self._wp  = self.mission.waypoints.index(perto)
            elif PVector.dist(self.alvo, self.pos) < 15: 
                self._path = True
                self.alvo = self.mission.waypoints[(self._wp+1) % len(self.mission.waypoints)]
        
        else: # Esta no path
            next_wp = (self._wp+1) % len(self.mission.waypoints)
            if PVector.dist(self.mission.waypoints[next_wp], self.pos) < 15: 
                self._nextTarguet()
                next_wp = (self._wp+1) % len(self.mission.waypoints)

            if self.mission.rota[self._wp] > 0:
                if not self._orbita:
                    dif_x = abs(self.mission.waypoints[self._wp].x - self.mission.waypoints[next_wp].x)
                    dif_y = abs(self.mission.waypoints[self._wp].y - self.mission.waypoints[next_wp].y)
                    if self.mission.waypoints[self._wp].x < self.mission.waypoints[next_wp].x: 
                        x = self.mission.waypoints[self._wp].x + (dif_x/2)
                    else: 
                        x = self.mission.waypoints[self._wp].x - (dif_x/2)
                    if self.mission.waypoints[self._wp].y < self.mission.waypoints[next_wp].y: 
                        y = self.mission.waypoints[self._wp].y + (dif_y/2)
                    else: 
                        y = self.mission.waypoints[self._wp].y - (dif_y/2)
                    self._orbita = PVector(x, y)
                
                posToCenter = PVector.sub(self._orbita, self.pos)
                ctp = posToCenter.normalize(None).mult(self.mission.raio)
                centerToPerim = PVector(ctp.x, ctp.y)
                theta = atan2(centerToPerim.y, centerToPerim.x)
                if self.mission.rota[self._wp] == 1: theta += 0.4
                else: theta -= 0.4
                
                x = self._orbita.x - (self.mission.raio * cos(theta))
                y = self._orbita.y - (self.mission.raio * sin(theta))
                self.alvo = PVector(x, y)
                
                if PVector.dist(self.mission.waypoints[next_wp], self.alvo) < 5: 
                    self._nextTarguet()

    def _nextTarguet(self):
        self._wp     = (self._wp+1) % len(self.mission.waypoints)
        next_wp      = (self._wp+1) % len(self.mission.waypoints)
        self.alvo    = self.mission.waypoints[next_wp]
        self._orbita = None

    def _targuet(self):
        fill(255,0,0)
        stroke(255,0,0)
        ellipse(self.alvo.x, self.alvo.y, 6, 6)
        line(self.pos.x, self.pos.y, self.alvo.x, self.alvo.y);

    def radar(self):
        colide = False
        
        saveFrame("radar{}.jpg".format(self.id))
        imgRadar = loadImage("radar{}.jpg".format(self.id))
        loadPixels()
        
        h9 = self.velo.heading() - PI/2
        for i in range(5, 14):
            if colide: break
            hx = h9 + (PI * (i/20.0)) 
            borda  = PVector(self.pos.x + (75*cos(hx)), self.pos.y + (75*sin(hx)))
            for i in range(10, 100, 10):
                fp = PVector.sub(borda, self.pos).normalize(None).mult(i) # Posicao futura
                # point(self.pos.x+fp.x, self.pos.y+fp.y)
                pix = pixels[int(self.pos.y+fp.y)*1200+int(self.pos.x+fp.x)]
                pixels[int(self.pos.y+fp.y)*1200+int(self.pos.x+fp.x)] = -16777200
                if pix != -1:
                    print('Detectou')
                    x = int(self.pos.x+fp.x)
                    y = int(self.pos.y+fp.y)
                    print('X:', x)
                    print('Y:', y)
                    obstaculo = PVector(x, y)
                    
                    next_wp = (self._wp+1) % len(self.mission.waypoints)
                    if PVector.dist(obstaculo, self.mission.waypoints[next_wp]) < 15: self._nextTarguet()
                    
                    if len(self._obstacles) == 0: 
                        self._obstacles.append(obstaculo)
                    elif abs(x-self._obstacles[-1].x) > 5 or abs(y-self._obstacles[-1].y) > 5: 
                        self._obstacles.append(obstaculo)

                    colide = True
                    break
        updatePixels()
        
