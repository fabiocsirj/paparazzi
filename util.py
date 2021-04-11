def ponto(raio, graus): # Retorna coordenadas de um ponto no perimetro de um circulo de acordo com o angulo (em graus)
    return PVector(raio*cos(graus/(180/PI)), raio*sin(graus/(180/PI)))
