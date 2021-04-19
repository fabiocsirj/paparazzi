class Path_eight:
    def __init__(self):
        self.waypoints = None
        self._center   = None
        self.raio      = 200
        self.rota      = [1, 0, 2, 0] # 0 = reto, 1 = horario, 2 = anti-horario
        self.show      = 1
    
    def setWP(self, center):
        self._center = center
        self.waypoints = []
        self.waypoints.append(PVector(center.x-self.raio, center.y+self.raio)) # 0 = Esq. Inf.
        self.waypoints.append(PVector(center.x-self.raio, center.y-self.raio)) # 1 = Esq. Sup.
        self.waypoints.append(PVector(center.x+self.raio, center.y+self.raio)) # 2 = Dir. Inf.
        self.waypoints.append(PVector(center.x+self.raio, center.y-self.raio)) # 3 = Dir. Sup.
        
    def paint(self):
        if self.show:
            fill(255)
            
            stroke(0, 0, 255)
            ellipse(self._center.x-self.raio, self._center.y, self.raio*2, self.raio*2)
            noStroke()
            rect(self.waypoints[1].x, self.waypoints[1].y, self.raio+1, self.raio*2+1)
            
            stroke(0, 0, 255)
            ellipse(self._center.x+self.raio, self._center.y, self.raio*2, self.raio*2)
            noStroke()
            rect(self.waypoints[3].x-self.raio, self.waypoints[3].y, self.raio, self.raio*2+1)
            
            stroke(0, 0, 255)
            line(self.waypoints[1].x, self.waypoints[1].y, self.waypoints[2].x, self.waypoints[2].y)
            line(self.waypoints[3].x, self.waypoints[3].y, self.waypoints[0].x, self.waypoints[0].y)
            
