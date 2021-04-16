class Path_stayat:
    def __init__(self):
        self.waypoints = None
        self._center   = None
        self.raio      = 200
        self.rota      = [1, 1] # 0 = reto, 1 = horario, 2 = anti-horario
        self.show      = 1
    
    def setWP(self, center):
        self._center = center
        self.waypoints = []
        self.waypoints.append(PVector(center.x, center.y+self.raio)) # 0 = Inf.
        self.waypoints.append(PVector(center.x, center.y-self.raio)) # 1 = Sup.
        
    def paint(self):
        if self.show:
            fill(255)
            
            stroke(0, 0, 255)
            ellipse(self._center.x, self._center.y, self.raio*2, self.raio*2)
