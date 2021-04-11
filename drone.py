from util import ponto
from oito import Oito

class Drone:
    def __init__(self):
        self.pos      = PVector(random(width), random(height)) # Posicao inicial aleatoria
        self.velo     = PVector(0, 0)                          # Velociade inicial
        self.maxSpeed = 0.2                                    # Define a velocidade maxima inicial
        self.mission  = None                                   # Configura a missao
        self.alvo     = PVector(0, 0)                          # Alvo inicial
        self.wind     = PVector(0, 0)                          # Vento inicial
        
        # Variaveis auxiliares para _seek_p8
        self._c    = PVector(0, 0)
        self._path = False
        self._orb  = False                          

    def set_mission(self, m):
        self.mission = m
        self.alvo    = PVector(0, 0)
        self._c      = PVector(0, 0)
        self._path   = False
        self._orb    = False

    def _paint(self):                                      # Desenha um Drone ajustando o angulo do setor anterior para simular direcao
        if self.velo.mag() > 0: angulo = self.velo.heading() + PI/2
        else: angulo = 0
        pushMatrix()
        translate(self.pos.x, self.pos.y)
        rotate(angulo)
        img = loadImage("drone4.png")
        image(img, -37, 0)
        popMatrix()

    def execute(self):
        if self.mission != None:
            if isinstance(self.mission, Oito): self._seek_p8(self.mission)
            
            # DEFINE A DIRECAO
            direcao = PVector.sub(self.alvo, self.pos)          # Direcao e a diferenca entre o alvo e a posicao atual
            distancia = direcao.mag()                           # Define a Distancia
            # print('Distancia:',distancia)
            self.maxSpeed = min(6, self.maxSpeed+0.2)           # Aceleracao gradual
            if not self._path and distancia < 70: 
                self.maxSpeed = map(distancia, 0, 70, 0.1, 6)   # Desaceleracao gradual

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
            #####################
            
            # ATUALIZA POSICAO
            self.pos.add(self.velo)                             # Atualiza a posicao adicionando a velocidade a posicao atual
            ##################

            # Pertubacao do vento
            self.pos.sub(self.wind)
            #####################
    
            # DESEHA O DRONE NA TELA
            self._paint()
            ##########################

    def _esquina_p8(self, p8, theta, orbita1, i):        # Dupla funcao: i = 1  define esquina mais proxima...
        orbitas = p8.get_orbitas()                       # ...           i = -1 transicao entre orbitas
        ang = theta * (180/PI)                                
        if orbita1:                                      # Se for a orbita esquerda...
            if ang > 90: p = ponto(p8.raio, 90*i)        #  -> Na funcao i=1 : Se angulo > 90, vai para esquina superior (90*1) da orbita esquerda
            if ang < -90: p = ponto(p8.raio, -90*i)      #  -> Na funcao i=-1: Se angulo > 90, vai para esquina inferior (90*-1) da orbita direita  
            if ang > 90 or ang < -90:                    # Linha acima mesmo raciocinio para angulo < -90 e aqui testa as duas condicoes...
                self.alvo.x = orbitas[(2+i)%3].x - p.x   #  -> Atualiza o alvo na orbita da esquerda (orbitas[0]), se i=1... 
                self.alvo.y = orbitas[(2+i)%3].y - p.y   # ... ou na orbita da direita (orbitas[1]), se i=-1
                if i == -1:                              # Se for transicao de orbitas...
                    self._c = orbitas[(2+i)%3]           #  -> Atualiza o self._c para orbita oposta
                    self._orb = False                    #  -> Sinaliza que nao esta mais em uma orbita
        else:                                            # Mesmo raciocinio de cima, porem para a orbita da direita
            if ang < 90 and ang >= 0: p = ponto(p8.raio, 90*i)
            if ang > -90 and ang <= 0: p = ponto(p8.raio, -90*1)
            if (ang < 90 and ang >= 0) or (ang > -90 and ang <= 0): 
                self.alvo.x = orbitas[abs(i-2)%3].x - p.x
                self.alvo.y = orbitas[abs(i-2)%3].y - p.y
                if i == -1: 
                    self._c = orbitas[abs(i-2)%3]
                    self._orb = False

    def _seek_p8(self, p8):                                             # PROCURA O CAMINHO
        if not self._path:                                              # NAO ESTA NO CAMINHO
            if self.pos.x-p8.orbita1.x < p8.orbita2.x-self.pos.x:       # Define orbita mais proxima...
                self._c = p8.orbita1.copy()                             #  -> self._c = centro da orbita esquerda
            else:
                self._c = p8.orbita2.copy()                             #  -> self._c = centro da orbita direita
            posToCenter = PVector.sub(self._c, self.pos)                # Define o vetor da posicao atual ate o centro desta orbita
            ctp = posToCenter.normalize(None).mult(p8.raio)
            centerToPerim = PVector(ctp.x, ctp.y)                       # Define o vetor deste centro ate o perimetro
            posToPerim = PVector.sub(posToCenter, centerToPerim)        # Define o caminho da posicao atual ate o perimetro (diferenca vetores acima)
            self.alvo.x = self.pos.x+posToPerim.x                       # Atualiza o alvo somando a posicao atual com o caminho ate o perimetro
            self.alvo.y = self.pos.y+posToPerim.y
            theta = atan2(self._c.y-self.alvo.y, self._c.x-self.alvo.x)
            self._esquina_p8(p8, theta, self._c==p8.orbita1, 1)         # Se o alvo for no perimetro interno das orbitas, atualiza para uma esquina
            if PVector.sub(self.alvo, self.pos).mag() < 15: 
                self._path = True

        else:                                                           # Se esta no caminho...
            if self._orb:                                               # Verifica se esta numa orbita
                posToCenter = PVector.sub(self._c, self.pos)            # -|
                ctp = posToCenter.normalize(None).mult(p8.raio)         #  | -> Explicado acima
                centerToPerim = PVector(ctp.x, ctp.y)                   # -|
                orbita1 = self._c==p8.orbita1
                theta = atan2(centerToPerim.y, centerToPerim.x)         # Calcula os radianos
                if orbita1: theta += 0.4                                # Velocidade Angular para esquerda
                else: theta -= 0.4                                      # Velocidade Angular para direita
                self.alvo.x = self._c.x - (p8.raio * cos(theta))        # Atualiza o alvo de acordo com qual centro e novo radiano
                self.alvo.y = self._c.y - (p8.raio * sin(theta))
                self._esquina_p8(p8, theta, orbita1, -1)                # Verifica limite da orbita (para fazer a transicao)...
                                                                        # ...da sup. esq. para inf. dir. e da sup. dir. para inf. esq.
            elif PVector.sub(self.alvo, self.pos).mag() < 15: self._orb = True
        
        # Marca o alvo
        fill(255,0,0)
        ellipse(self.alvo.x, self.alvo.y, 6, 6)
        stroke(0,0,255);
        line(self.pos.x, self.pos.y, self.alvo.x, self.alvo.y);
        ##############
