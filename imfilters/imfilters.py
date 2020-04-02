from PIL import Image


class IMGray:
    '''
    Classe responsavel por aplicar filtro de escala de cinza.
    :param image: Caminho do arquivo a ser aberto
    :param mode: Modo de saida do arquivo. Ex: '0.25' -> 25%, '0.5' -> 50%, '0.75' -> 75%, 'optimize' -> Optimized.
    '''

    def __init__(self, image, mode=None):
        self.image = image
        self.mode = mode
        self.img = Image.open(self.image, 'r')
        self.width, self.height = self.img.size

    def save(self, path):
        '''
        Método responsável por salvar imagem.
        :param path: Nome do arquivo a ser salvo.
        '''
        self.new_img = Image.new('RGB', self.img.size)

        for x in range(self.width):
            for y in range(self.height):
                px = self.img.getpixel((x,y))
                mean_color = (px[0] + px[1] + px[2])//3
                if self.mode == 'optimize':
                    self.new_img.putpixel((x,y), self._optimized(px))
                elif self.mode == '0.25':
                    self.new_img.putpixel((x,y), self._25(px))
                elif self.mode == '0.5':
                    self.new_img.putpixel((x,y), self._50(px))
                elif self.mode == '0.75':
                    self.new_img.putpixel((x,y), self._75(px))
                else:
                    self.new_img.putpixel((x,y),(mean_color, mean_color, mean_color))
        self.new_img.save(path)
    
    def _optimized(self, pixel):
        p_R = pixel[0]
        p_G = pixel[1]
        p_B = pixel[2]

        color = int((p_R * 0.21) + int(p_G * 0.71) + int(p_B * 0.8)//3)
        return (color, color, color)
    
    def _25(self, pixel):
        p_R = pixel[0]
        p_G = pixel[1]
        p_B = pixel[2]

        c = (p_R + p_G + p_B)//3
        cor = int(c + ((255 - c) * 0.25))

        return (cor, cor, cor)

    def _50(self, pixel):
        p_R = pixel[0]
        p_G = pixel[1]
        p_B = pixel[2]

        c = (p_R + p_G + p_B)//3
        cor = int(c + ((255 - c) * 0.5))

        return (cor, cor, cor)

    def _75(self, pixel):
        p_R = pixel[0]
        p_G = pixel[1]
        p_B = pixel[2]

        c = (p_R + p_G + p_B)//3
        cor = int(c - ((255 - c) * 0.25))

        return (cor, cor, cor)
    



if __name__ == '__main__':
    img = IMGray('dev.jpg', mode='optimize')
    img.save('dev_optimize.png')
