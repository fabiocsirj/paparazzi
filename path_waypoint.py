class Path_waypoint:
    def __init__(self):
        self.waypoints = None
        self._center   = None
        self.raio      = 200
        self.rota      = [0, 0] # 0 = reto, 1 = horario, 2 = anti-horario
        self.show      = 1
    
    def setWP(self, center):
        self._center = center
        self.waypoints = []
        self.waypoints.append(PVector(center.x-self.raio, center.y)) # 0 = Esq.
        self.waypoints.append(PVector(center.x+self.raio, center.y)) # 1 = Dir.
        
    def paint(self):
        if self.show:
            fill(255)
            
            stroke(0, 0, 255)
            line(self.waypoints[0].x, self.waypoints[0].y, self.waypoints[1].x, self.waypoints[1].y)
            fill(0)
            ellipse(self.waypoints[0].x, self.waypoints[0].y, 5, 5)
            ellipse(self.waypoints[1].x, self.waypoints[1].y, 5, 5)
