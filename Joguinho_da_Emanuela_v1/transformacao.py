def transformarcao(self, eixo_x, eixo_y):
    return self.traformarcao_perpectiva(eixo_x, eixo_y)
    #return self.transformarcao_2D(eixo_x, eixo_y)

def transformarcao_2D(self, eixo_x, eixo_y):
    return int(eixo_x), int(eixo_y)

def traformarcao_perpectiva(self, eixo_x, eixo_y):
    linha_eixo_y = eixo_y * self.perpectiva_ponto_y / self.height
    if linha_eixo_y > self.perpectiva_ponto_y:
        linha_eixo_y = self.perpectiva_ponto_y
    
    diferencial_x = eixo_x - self.perpectiva_ponto_x
    diferencial_y = self.perpectiva_ponto_y - linha_eixo_y
    
    #proporção de Y, 1 enquanto diferencial de y == perpectiva_ponto_y ,  0 enquanto diferencial de y
    fator_y = diferencial_y / self.perpectiva_ponto_y
    fator_y = pow(fator_y, 4)

    transformacao_eixo_x = self.perpectiva_ponto_x + diferencial_x * fator_y
    transformacao_eixo_y = self.perpectiva_ponto_y - fator_y * self.perpectiva_ponto_y

    return int(transformacao_eixo_x), int(transformacao_eixo_y)