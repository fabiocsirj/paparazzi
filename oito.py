from util import ponto

class Oito:
    def __init__(self, x, y, raio):
        self.centro  = PVector(x, y)                                   # CENTRO do 8 de Paparazzi
        self.raio    = raio                                            # RAIO inicial das orbitas
        self.orbita1 = PVector(self.centro.x-self.raio, self.centro.y) # Orbita da esquerda
        self.orbita2 = PVector(self.centro.x+self.raio, self.centro.y) # Orbita da direita
    
    def get_orbitas(self):
        return (self.orbita1, self.orbita2)

    def paint(self):
        fill(255)
        stroke(0)
        ellipse(self.orbita1.x, self.orbita1.y, self.raio*2, self.raio*2)
        ellipse(self.orbita2.x, self.orbita2.y, self.raio*2, self.raio*2)
        inf = ponto(self.raio, -90)
        sup = ponto(self.raio, 90)
        inf1 = PVector(self.orbita1.x-inf.x, self.orbita1.y-inf.y)
        sup1 = PVector(self.orbita1.x-sup.x, self.orbita1.y-sup.y)
        inf2 = PVector(self.orbita2.x-inf.x, self.orbita2.y-inf.y)
        sup2 = PVector(self.orbita2.x-sup.x, self.orbita2.y-sup.y)
        noStroke()
        rect(sup1.x, sup1.y, self.raio*2, self.raio*2+1)
        stroke(0)
        line(inf1.x, inf1.y, sup2.x, sup2.y)
        line(inf2.x, inf2.y, sup1.x, sup1.y)
