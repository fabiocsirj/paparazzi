class Path_scan:
    def __init__(self):
        self.waypoints = None
        self._center   = None
        self.raio      = 50
        self.rota      = [0, 1, 0, 2, 0, 1, 0, 2, 0, 0] # 0 = reto, 1 = horario, 2 = anti-horario
        self.show      = 1
    
    def setWP(self, center):
        self._center = center
        self.waypoints = []
        self.waypoints.append(PVector(center.x-(self.raio*4), center.y-(self.raio*4)))
        self.waypoints.append(PVector(center.x+(self.raio*4), center.y-(self.raio*4)))
        self.waypoints.append(PVector(center.x+(self.raio*4), center.y-(self.raio*2)))
        self.waypoints.append(PVector(center.x-(self.raio*4), center.y-(self.raio*2)))
        self.waypoints.append(PVector(center.x-(self.raio*4), center.y))
        self.waypoints.append(PVector(center.x+(self.raio*4), center.y))
        self.waypoints.append(PVector(center.x+(self.raio*4), center.y+(self.raio*2)))
        self.waypoints.append(PVector(center.x-(self.raio*4), center.y+(self.raio*2)))
        self.waypoints.append(PVector(center.x-(self.raio*4), center.y+(self.raio*4)))
        self.waypoints.append(PVector(center.x+(self.raio*4), center.y+(self.raio*4)))

    def paint(self):
        if self.show:
            fill(0)
            stroke(0, 0, 255)
            ellipse(self.waypoints[0].x, self.waypoints[0].y, 5, 5)
            fill(255)
            
            ellipse(self.waypoints[1].x, self.waypoints[1].y+self.raio, self.raio*2, self.raio*2)
            noStroke()
            rect(self.waypoints[1].x-self.raio, self.waypoints[1].y, self.raio, self.raio*2+1)
            
            stroke(0, 0, 255)
            ellipse(self.waypoints[3].x, self.waypoints[3].y+self.raio, self.raio*2, self.raio*2)
            noStroke()
            rect(self.waypoints[3].x, self.waypoints[3].y, self.raio+1, self.raio*2+1)
            
            stroke(0, 0, 255)
            ellipse(self.waypoints[5].x, self.waypoints[5].y+self.raio, self.raio*2, self.raio*2)
            noStroke()
            rect(self.waypoints[5].x-self.raio, self.waypoints[5].y, self.raio, self.raio*2+1)
            
            stroke(0, 0, 255)
            ellipse(self.waypoints[7].x, self.waypoints[7].y+self.raio, self.raio*2, self.raio*2)
            noStroke()
            rect(self.waypoints[7].x, self.waypoints[7].y, self.raio+1, self.raio*2+1)
            
            stroke(0, 0, 255)
            line(self.waypoints[8].x, self.waypoints[8].y, self.waypoints[9].x, self.waypoints[9].y)
            line(self.waypoints[6].x, self.waypoints[6].y, self.waypoints[7].x, self.waypoints[7].y)
            line(self.waypoints[4].x, self.waypoints[4].y, self.waypoints[5].x, self.waypoints[5].y)
            line(self.waypoints[2].x, self.waypoints[2].y, self.waypoints[3].x, self.waypoints[3].y)
            line(self.waypoints[0].x, self.waypoints[0].y, self.waypoints[1].x, self.waypoints[1].y)
            
            fill(0)
            ellipse(self.waypoints[9].x, self.waypoints[9].y, 5, 5)
            
            
