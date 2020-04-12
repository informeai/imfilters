#
# Python script for applying filters to images
# Thanks to the pillow library team
#
# Copyright (c) 2020 by Wellington Gadelha. All Rights reserved.
#


import math
import os
from random import randint, random

from PIL import Image, ImageFilter, ImageGrab, ImageDraw

class IMBrightness:
    '''
    Class responsible for applying the brightness adjustment filter.
    : param image: Image to be applied to the filter.
    : param adjust: Adjustment level.
    '''
    def __init__(self, image:str, adjust:int=5):
        self.image = image
        self.adjust = adjust

        adj = math.floor(255 * (self.adjust / 100))

        self.img = Image.open(self.image)

        width, height = self.img.size

        self.new_image = Image.new('RGB', self.img.size)

        for x in range(width):
            for y in range(height):
                px = self.img.getpixel((x,y))

                r = px[0] + adj
                g = px[1] + adj
                b = px[2] + adj

                self.new_image.putpixel((x,y),(r, g, b))

    def save(self, path:str):
        '''
        Method responsible for saving image.
        : param path: Name of the file to be saved.
        '''
        self.new_image.save(path)

    def show(self):
        '''
        Method responsible for viewing the image.
        '''
        self.new_image.show()

class IMContrast:
    '''
    Class responsible for applying the contrast adjustment filter.
    : param image: Image to be applied to the filter.
    : param adjust: Adjustment level.
    '''

    def __init__(self, image:str, adjust:int=0):
        self.image = image
        self.adjust = adjust

        self.img = Image.open(self.image)

        width, height = self.img.size

        adj = pow((self.adjust + 100) / 100, 2)

        self.new_img = Image.new('RGB',self.img.size)

        for x in range(width):
            for y in range(height):
                
                px = self.img.getpixel((x,y))

                red = px[0]
                green = px[1]
                blue = px[2]

                red /= 255
                red -= 0.5
                red *= adj
                red += 0.5
                red *= 255

                green /= 255
                green -= 0.5
                green *= adj
                green += 0.5
                green *= 255

                blue /= 255
                blue -= 0.5
                blue *= adj
                blue += 0.5
                blue *= 255

                r = int(red)
                g = int(green)
                b = int(blue)

                self.new_img.putpixel((x,y), (r, g, b))

    def save(self, path:str):
        '''
        Method responsible for saving image.
        : param path: Name of the file to be saved.
        '''
        self.new_img.save(path)

    def show(self):
        '''
        Method responsible for viewing the image.
        '''
        self.new_img.show()


class IMSaturation:
    '''
    Class responsible for applying the saturation adjustment filter.
    : param image: Image to be applied to the filter.
    : param adjust: Adjustment level.
    '''

    def __init__(self, image:str, adjust:int=10):
        self.image = image
        self.adjust = adjust

        adj = self.adjust * -0.01

        self.img = Image.open(self.image)

        width, height = self.img.size

        self.new_img = Image.new('RGB', self.img.size)

        for x in range(width):
            for y in range(height):

                px = self.img.getpixel((x,y))

                red = px[0]
                green = px[1]
                blue = px[2]

                maximo = max(red, green, blue)

                if red != maximo:
                    red = red + (maximo - red) * adj
                if green != maximo:
                    green = green + (maximo - green) * adj
                if blue != maximo:
                    blue = blue + (maximo - blue) * adj

                r = int(red)
                g = int(green)
                b = int(blue)
                
                self.new_img.putpixel((x,y), (r,g,b))
    
    def save(self, path:str):
        '''
        Method responsible for saving image.
        : param path: Name of the file to be saved.
        '''
        self.new_img.save(path)

    def show(self):
        '''
        Method responsible for viewing the image.
        '''
        self.new_img.show()

class IMVibrance:
    '''
    Class responsible for applying the vibrance filter.
    : param image: Image to be applied to the filter.
    : param adjust: Adjustment level.
    '''

    def __init__(self, image:str, adjust:int=50):
        self.image = image
        self.adjust = adjust

        self.img = Image.open(self.image)

        width, height = self.img.size

        self.new_img = Image.new('RGB',self.img.size)

        adj = self.adjust * -1

        for x in range(width):
            for y in range(height):

                px = self.img.getpixel((x,y))

                red = px[0]
                green = px[1]
                blue = px[2]

                mx = max(red, green, blue)
                avg = (red + green + blue) / 3
                amt = ((abs(mx - avg) * 2 / 255) * adj) / 100

                if red != mx:
                    red = red + (mx - red) * amt
                if green != mx:
                    green = green + (mx - green) * amt
                if blue != mx:
                    blue = blue + (mx - blue) * amt

                r = int(red)
                g = int(green)
                b = int(blue)

                self.new_img.putpixel((x,y), (r, g, b))

    def save(self, path:str):
        '''
        Method responsible for saving image.
        : param path: Name of the file to be saved.
        '''
        self.new_img.save(path)

    def show(self):
        '''
        Method responsible for viewing the image.
        '''
        self.new_img.show()



class IMGray:
    '''
    Class responsible for applying gray scale filter.
    : param image: Path of the file to be opened
    : param mode: File output mode. Ex: 'normal' -> Balanced gray scale, - 'optimize' -> Optimized gray scale.
    '''

    def __init__(self, image:str, mode:str=None):
        self.image = image
        self.mode = mode
        self.img = Image.open(self.image, 'r')
        self.width, self.height = self.img.size


        self.new_img = Image.new('RGB', self.img.size)

        for x in range(self.width):
            for y in range(self.height):
                px = self.img.getpixel((x,y))

                lum = IMLuminance(rgb=px).lumin

                if self.mode == 'optimize':
                    self.new_img.putpixel((x,y), self._optimized(px))
                else:
                    self.new_img.putpixel((x,y), (lum, lum, lum))

    def save(self, path):
        '''
        Method responsible for saving image.
        : param path: Name of the file to be saved.
        '''
        self.new_img.save(path)

    def show(self):
        '''
        Method responsible for viewing the image.
        '''
        self.new_img.show()
    
    def _optimized(self, pixel):
        p_R = pixel[0]
        p_G = pixel[1]
        p_B = pixel[2]

        color = int((p_R * 0.21) + int(p_G * 0.71) + int(p_B * 0.8)//3)
        return (color, color, color)
    
class IMBoxBlur:
    '''
    Class responsible for applying blur filter in box.
    : param image: Image to be applied to the filter.
    : param bl: Size of the blur box. Ex: bl = 5 -> box: 5X5.
    '''

    def __init__(self, image:str, bl:int=None):
        self.image = image
        im = Image.open(self.image)
        if bl and isinstance(bl, int):
            self.im_final = im.filter(ImageFilter.BoxBlur(bl))
        else:
            self.im_final = im.filter(ImageFilter.BoxBlur(1))

    def save(self, path:str):
        '''
        Method responsible for saving image.
        : param path: Name of the file to be saved.
        '''
        self.im_final.save(path)

    def show(self):
        '''
        Method responsible for viewing the image.
        '''
        self.im_final.show()


class IMGaussBlur:
    '''
    Class responsible for applying Gaussian filter.
    :param image: Image to be applied to the filter.
    :param radius: Blur radius.
    '''

    def __init__(self, image:str, radius:int=2):
        self.image = image
        self.radius = radius
        img = Image.open(self.image)

        if self.radius and isinstance(self.radius, int):
            self.im_final = img.filter(ImageFilter.GaussianBlur(radius=self.radius))
        
        self.im_final = img.filter(ImageFilter.GaussianBlur(radius=2))

    def save(self, path:str):
        '''
        Method responsible for saving image.
        : param path: Name of the file to be saved.
        '''
        self.im_final.save(path)

    def show(self):
        '''
        Method responsible for viewing the image.
        '''
        self.im_final.show()

class IMUnsharpMask:
    '''
    Class responsible for applying sharpness mask filter.
    :param image: Image to be applied to the filter.
    :param radius: Radius of the maskara.
    :param percent: Sharpness percentage.
    :param limit: Brightness limit.
    '''

    def __init__(self, image:str, radius=2, percent=50, limit=3):
        self.image = image
        self.radius = radius
        self.percent = percent
        self.limit = limit

        img = Image.open(self.image)
        self.im_final = img.filter(ImageFilter.UnsharpMask(radius=self.radius, percent=self.percent, threshold=self.limit))

    def save(self, path:str):
        '''
        Method responsible for saving image.
        : param path: Name of the file to be saved.
        '''
        self.im_final.save(path)

    def show(self):
        '''
        Method responsible for viewing the image.
        '''
        self.im_final.show()

class IMRFilters:
    '''
    Base class that provides quick filters.
    :param image: Image to be applied to the filter.
    '''

    def __init__(self, image:str):
        self.image = image
        im = Image.open(self.image)
        self.BLUR = self._blur(im)
        self.CONTOUR = self._contour(im)
        self.DETAIL = self._detail(im)
        self.EDGE_ENHANCE = self._edge_enhance(im)
        self.EDGE_ENHANCE_MORE = self._edge_enhance_more(im)
        self.EMBOSS = self._emboss(im)
        self.FIND_EDGES = self._find_edges(im)
        self.SHARPEN = self._sharpen(im)
        self.SMOOTH = self._smooth(im)
        self.SMOOTH_MORE = self._smooth_more(im)

    def _contour(self, img):
        return img.filter(ImageFilter.CONTOUR)

    def _edge_enhance(self, img):
        return img.filter(ImageFilter.EDGE_ENHANCE)
    
    def _blur(self, img):
        return img.filter(ImageFilter.BLUR)
    
    def _detail(self, img):
        return img.filter(ImageFilter.DETAIL)
    
    def _edge_enhance_more(self, img):
        return img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    def _emboss(self, img):
        return img.filter(ImageFilter.EMBOSS)
    
    def _find_edges(self, img):
        return img.filter(ImageFilter.FIND_EDGES)
    
    def _sharpen(self, img):
        return img.filter(ImageFilter.SHARPEN)

    def _smooth(self, img):
        return img.filter(ImageFilter.SMOOTH)

    def _smooth_more(self, img):
        return img.filter(ImageFilter.SMOOTH_MORE)

    
class IMLuminance:
    '''
    Class responsible for return luminance.
    '''

    def __init__(self, rgb:tuple):
        self.rgb = rgb
        self.lumin = int((0.299 * self.rgb[0]) + (0.587 * self.rgb[1]) + (0.114 * self.rgb[2]))
    

class IMRgbToHsv:
    '''
    Class responsible for convert rgb to hsv.
    '''

    def __init__(self, rgb:tuple):
        self.rgb = rgb

        r = self.rgb[0]
        g = self.rgb[1]
        b = self.rgb[2]

        maximo = max(r, g, b)
        minimo = min(r, g, b)

        v = maximo
        d = maximo - minimo

        s = 0 if maximo == 0 else d / maximo

        if maximo == minimo:
            h = 0
        else:
            if maximo == r:
                if g < b:
                    e = 6
                else:
                    e = 0
                h = (g - b) / d + e
            elif maximo == g:
                h = (b - r) / d + 2
            elif maximo == b:
                h = (r - g) / d + 4
        h /= 6
        self.hsv = (h, s, v)

class IMRgbToHsl:
    '''
    Class responsible for convert rgb to hsl.
    '''

    def __init__(self, rgb:tuple):
        self.rgb = rgb

        r = self.rgb[0]
        g = self.rgb[1]
        b = self.rgb[2]

        r /= 255
        g /= 255
        b /= 255

        maximo = max(r, g, b)
        minimo = min(r, g, b)

        l = (maximo + minimo) / 2

        if maximo == minimo:
            h = 0
            s = 0
        else:
            d = maximo - minimo

            if l > 0.5:
                s = d / (2 - maximo - minimo)
            else:
                s = d / (maximo - minimo)
            
            # Calculo do h
            if maximo == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif maximo == g:
                h = (b - r) / d + 2
            elif maximo == b:
                h = (r - g) / d + 4

            h /= 6

        self.hsl = (h, s, l)


class IMHsvToRgb:
    '''
    Class responsible for convert hsv to rgb.
    '''

    def __init__(self, hsv:tuple):
        h = hsv[0]
        s = hsv[1]
        v = hsv[2]

        i = math.floor(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        if i % 6 == 0:
            r = v
            g = t
            b = p
        elif i % 6 == 1:
            r = q
            g = v
            b = p
        elif i % 6 == 2:
            r = p
            g = v
            b = t
        elif i % 6 == 3:
            r = p
            g = q
            b = v
        elif i % 6 == 4:
            r = t
            g = p
            b = v
        elif i % 6 == 5:
            r = v
            g = p
            b = q

        red = math.floor(r * 255)
        green = math.floor(g * 255)
        blue = math.floor(b * 255)

        self.rgb = (red, green, blue)



class IMSepia:
    '''
    Class responsible for applying the sepia filter.
    : param image: Image to be applied to the filter.
    : param adjust: Adjustment level.
    '''

    def __init__(self, image:str, adjust:int=100):
        self.image = image
        self.adjust = adjust
        
        self.adjust /= 100



        im = Image.open(self.image)

        w, h = im.size

        self.im_final = Image.new('RGB', size=im.size)

        for x in range(w):
            for y in range(h):

                px = im.getpixel((x,y))

                r = int(min(255, (px[0] * (1 - (0.607 * self.adjust))) + (px[1] * (0.769 * self.adjust)) + (px[2] * (0.189 * self.adjust))))
                g = int(min(255, (px[0] * (0.349 * self.adjust)) + (px[1] * (1 - (0.314 * self.adjust))) + (px[2] * (0.168 * self.adjust))))
                b = int(min(255, (px[0] * (0.272 * self.adjust)) + (px[1] * (0.534 * self.adjust)) + (px[2] * (1 - (0.869 * self.adjust)))))
                
                self.im_final.putpixel((x,y),(r, g, b))
        

    def save(self, path:str):
        '''
        Method responsible for saving image.
        : param path: Name of the file to be saved.
        '''
        return self.im_final.save(path)

    def show(self):
        '''
        Method responsible for viewing the image.
        '''
        return self.im_final.show()

class IMInvert:
    '''
    Class responsible for applying the invert filter.
    : param image: Image to be applied to the filter.
    : param adjust: Adjustment level.
    '''

    def __init__(self, image:str):
        self.image = image

        im = Image.open(self.image)

        w, h = im.size

        self.im_final = Image.new('RGB', size=im.size)

        for x in range(w):
            for y in range(h):
                
                px = im.getpixel((x,y))

                r = 255 - px[0]
                g = 255 - px[1]
                b = 255 - px[2]
                

                self.im_final.putpixel((x,y), (r, g, b))

    def save(self, path:str):
        '''
        Method responsible for saving image.
        :param path: Name of the file to be saved.
        '''
        self.im_final.save(path)

    def show(self):
        '''
        Method responsible for viewing the image.
        '''
        self.im_final.show()

class IMNoise:
    '''
    Class responsible for applying the noise filter.
    :param image: Image to be applied to the filter.
    :param adjust: Adjustment level.
    '''

    def __init__(self, image:str, adjust:int=10):
        self.image = image
        self.adjust = adjust

        self.img = Image.open(self.image)

        width, height = self.img.size

        self.new_img = Image.new('RGB', self.img.size)

        adj = abs(self.adjust) * 2.55

        minimo = adj * -1
        maximo = adj
        for x in range(width):
            for y in range(height):
                
                rand = round(minimo + (random() * (maximo - minimo)))
                px = self.img.getpixel((x,y))
                red = px[0]
                green = px[1]
                blue = px[2]

                r = int(red + rand)
                g = int(green + rand)
                b = int(blue + rand)

                self.new_img.putpixel((x,y), (r, g, b))

    def save(self, path:str):
        '''
        Method responsible for saving image.
        : param path: Name of the file to be saved.
        '''
        self.new_img.save(path)

    def show(self):
        '''
        Method responsible for viewing the image.
        '''
        self.new_img.show()

class IMGamma:
    '''
    Class responsible for applying the gamma filter.
    :param image: Image to be applied to the filter.
    :param adjust: Adjustment level.
    '''

    def __init__(self, image:str, adjust:int=2):
        self.image = image
        self.adjust = adjust

        self.img = Image.open(self.image)

        self.new_img = Image.new('RGB', self.img.size)

        width, height = self.img.size

        for x in range(width):
            for y in range(height):

                px = self.img.getpixel((x,y))

                red = px[0]
                green = px[1]
                blue = px[2]

                r = int(pow(red / 255, self.adjust) * 255)
                g = int(pow(green / 255, self.adjust) * 255)
                b = int(pow(blue / 255, self.adjust) * 255)

                self.new_img.putpixel((x,y), (r, g, b))

    def save(self, path:str):
        '''
        Method responsible for saving image.
        :param path: Name of the file to be saved.
        '''
        self.new_img.save(path)

    def show(self):
        '''
        Method responsible for viewing the image.
        '''
        self.new_img.show()

class IMClip:
    '''
    Class responsible for applying the clip filter.
    :param image: Image to be applied to the filter.
    :param adjust: Adjustment level.
    '''

    def __init__(self, image:str, adjust:int=15):
        self.image = image
        self.adjust = adjust

        self.img = Image.open(self.image)

        width, height = self.img.size

        self.new_img = Image.new('RGB', self.img.size)

        adj = abs(self.adjust) * 2.55

        for x in range(width):
            for y in range(height):

                px = self.img.getpixel((x,y))

                red = px[0]
                green = px[1]
                blue = px[2]

                if (red > 255 - adj):
                    red = 255
                elif (red < adj):
                    red = 0

                if (green > 255 - adj):
                    green = 255
                elif (green < adj):
                    green = 0
                
                if (blue > 255 - adj):
                    blue = 255
                elif (blue < adj):
                    blue = 0
                
                r = int(red)
                g = int(green)
                b = int(blue)

                self.new_img.putpixel((x,y), (r, g, b))

    def save(self, path:str):
        '''
        Method responsible for saving image.
        :param path: Name of the file to be saved.
        '''
        self.new_img.save(path)

    def show(self):
        '''
        Method responsible for viewing the image.
        '''
        self.new_img.show()

class IMThreshold:
    '''
    Class responsible for applying the threshold filter.
    :param image: Image to be applied to the filter.
    :param limiar: Adjustment limiar.
    '''

    def __init__(self, image:str, limiar:int=127):
        self.image = image
        name , _ = os.path.splitext(self.image)

        self.limiar = limiar


        self.gray = IMGray(self.image)
        self.gray.save(name+'.png')

        self.img = Image.open(name+'.png')

        self.new_img = Image.new('RGB', self.img.size)

        width, height = self.img.size

        for x in range(width):
            for y in range(height):

                px = self.img.getpixel((x,y))

                red = px[0]
                green = px[1]
                blue = px[2]

                m = self.limiar


                if red > m:
                    r = 255
                elif red < m:
                    r = 0

                if green > m:
                    g = 255
                elif green < m:
                    g = 0
                
                if blue > m:
                    b = 255
                elif blue < m:
                    b = 0

                self.new_img.putpixel((x,y), (r, g, b))
        os.remove(name+'.png')

    def save(self, path:str):
        '''
        Method responsible for saving image.
        :param path: Name of the file to be saved.
        '''
        self.new_img.save(path)


    def show(self):
        '''
        Method responsible for viewing the image.
        '''
        self.new_img.show()

class IMSoftSat:
    '''
    Class responsible for applying the soft saturation filter.
    :param image: Image to be applied to the filter.
    '''

    def __init__(self, image:str):
        self.image = image

    def save(self, path:str):
        '''
        Método responsável por salvar imagem.
        :param path: Nome do arquivo a ser salvo.
        '''
        self.img_br = IMBrightness(self.image, 10)
        self.img_br.save(path)
        self.img_cont = IMContrast(path,30)
        self.img_cont.save(path)
        self.img_sepia = IMSepia(path, 60)
        self.img_sepia.save(path)
        self.img_satu = IMSaturation(path, -30)
        self.img_satu.save(path)



class IMSolarize:
    '''
    Class responsible for applying the solarize filter.
    :param image: Image to be applied to the filter.
    :param limit: Adjustment nivel de exposition.
    '''

    def __init__(self, image:str, limit:int=128):
        self.image = image
        self.limit = limit

        self.img = Image.open(self.image)

        self.new_img = Image.new('RGB', self.img.size)

        width, height = self.img.size

        for x in range(width):
            for y in range(height):

                px = self.img.getpixel((x,y))

                red = px[0]
                green = px[1]
                blue = px[2]

                if red > self.limit:
                    r = 255 - red
                else:
                    r = red

                if green > self.limit:
                    g = 255 - green
                else:
                    g = green
                
                if blue > self.limit:
                    b = 255 - blue
                else:
                    b = blue

                self.new_img.putpixel((x,y), (r, g, b))

    def save(self, path:str):
        '''
        Method responsible for saving image.
        :param path: Name of the file to be saved.
        '''
        self.new_img.save(path)

    def show(self):
        '''
        Method responsible for viewing the image.
        '''
        self.new_img.show()

class IMSharpen:
    '''
    Class responsible for applying the sharpen filter.
    :param image: Image to be applied to the filter.
    '''

    def __init__(self, image:str):
        self.image = image

        img = Image.open(self.image)
        self.new_img = img.filter(ImageFilter.Kernel((3,3), (0, -1, 0, -1, 8, -1, 0, -1, 0)))

    def save(self, path:str):
        '''
        Method responsible for saving image.
        :param path: Name of the file to be saved.
        '''
        self.new_img.save(path)

    def show(self):
        '''
        Method responsible for viewing the image.
        '''
        self.new_img.show()

class IMLumios:
    '''
    Class responsible for applying lumens filters.
    : param image: Image to be applied to the filter.
    : param color: Color to be applied. Options -> red, blue, green.
    : param percent: Quantity of color percentage.
    '''

    def __init__(self, image:str, color:str='blue', percent:float=0.1):
        self.image = image

        im = Image.open(self.image)

        self.new_img = Image.new('RGB',im.size)

        width, height = im.size

        percent *=10
        if percent > 10:
            l = 10
        elif percent < 0:
            l = 0
        else:
            l = percent

        for x in range(width):
            for y in range(height):

                px = im.getpixel((x,y))

                red = px[0]
                green = px[1]
                blue = px[2]

                med = (red + green + blue) // 3
                
                if color == 'blue':
                    r = med
                    g = med
                    b = blue + ((255 - blue) // 10) * int(l)
                elif color == 'red':
                    r = red + ((255 - red) // 10) * int(l)
                    g = med
                    b = med
                elif color == 'green':
                    r = med 
                    g = green + ((255 - green) // 10) * int(l)
                    b = med
                else:
                    print(f'Color -> {color} not applicable.')
                    exit(0)
                self.new_img.putpixel((x,y), (r, g, b))

    def save(self, path:str):
        '''
        Method responsible for saving the image with filter.
        '''
        self.new_img.save(path)

    def show(self):
        '''
        Method responsible for showing the image with filter.
        '''
        self.new_img.show()

class IMPixelated:
    '''
    Class responsible for applying pixelated filters.
    : param image: Image to be applied to the filter.
    : param scale: Scale of pixel diameter.
    '''

    def __init__(self, image:str, scale:int=3):
        self.image = image
        self.scale = scale

        im = Image.open(self.image)
        im = im.convert('RGBA')

        new_img = Image.new('RGBA',im.size, (0,0,0,0))

        draw = ImageDraw.Draw(new_img)

        width, height = im.size

        self.scale = 10

        if self.scale > 10:
            self.scale = 10
        elif self.scale < 3:
            self.scale = 3


        for x in range(width):
            for y in range(height):

                px = im.getpixel((x,y))


                red = px[0] 
                green = px[1] 
                blue = px[2] 

                r = int(red)
                g = int(green)
                b = int(blue)

                if x % self.scale == 0:
                    draw.rectangle(((x + 5,y + 5),(x + 10, y + 10)), fill=(r, g, b, 500))

        im = Image.alpha_composite(im,new_img)

        self.new_im = im.convert('RGB')

    def save(self, path:str):
        '''
        Method responsible for saving the image with filter.
        '''
        self.new_im.save(path)

    def show(self):
        '''
        Method responsible for showing the image with filter.
        '''
        self.new_im.show()

class IMRectangle:
    '''
    Class responsible for applying rectangle filters.
    :param image: Image to be applied to the filter.
    :param color: Color of RGBA format for aply in rectangle.
    :param scale: Scale for rectangles.
    :param rand: Apply random color.
    :param dist: Distance of rectangles.
    '''

    def __init__(self, image:str, color:tuple=(0,0,0,1), scale:int=3, rand:bool=False, dist:int=20):
        self.image = image
        self.color = color
        self.scale = scale
        self.rand = rand
        self.dist = dist

        self.im = Image.open(self.image)
        self.im = self.im.convert('RGBA')

        self.new_img = Image.new('RGBA',self.im.size, (0,0,0,0))

        draw = ImageDraw.Draw(self.new_img)

        width, height = self.im.size

        r = self.color[0]
        g = self.color[1]
        b = self.color[2]
        a = self.color[3]
        if a > 1:
            a = 1
        elif a < 0:
            a = 0
        else:
            a = int(a * 1000)
        self.rgba = (r, g, b, a)

        for x in range(0,width, randint(2,self.dist//2)):
            for y in range(0, height, randint(self.dist//2,self.dist * 2)):

                r = randint(1,3)

                if self.rand:
                    draw.rectangle(((x,y),(x + self.scale * r, y + self.scale )), (randint(0,255), randint(0,255), randint(0,255), randint(100,1000))) 
                else:
                    draw.rectangle(((x,y),(x + self.scale * r, y + self.scale )), self.rgba)    

                


        self.im = Image.alpha_composite(self.im,self.new_img)
        self.new_img = self.im.convert('RGB')

    def save(self,path:str):
        '''
        Method responsible for saving the image with filter.
        '''
        self.new_img.save(path)

    def show(self):
        '''
        Method responsible for showing the image with filter.
        '''
        self.new_img.show()

class IMPredominance:
    '''
    Class responsible for applying predominance filter of color.
    :param image: Image to be applied to the filter.
    :param color: Color for predominance. Ex: red, blue, green, yellow, orange, purple, ciano, pink.
    '''

    def __init__(self, image:str, color:str='red'):
        self.image = image
        self.color = color
        self.im = Image.open(self.image)

        self.new_im = Image.new('RGB', self.im.size)

        width, height = self.im.size

        for x in range(width):
            for y in range(height):

                px = self.im.getpixel((x,y))

                red = px[0]
                green = px[1]
                blue = px[2]

                med = (red + green + blue) // 3

                if self.color == 'red':
                    if red > green and red > blue:
                        r = red
                        g = green
                        b = blue
                    else:
                        r = med
                        g = med
                        b = med
                elif self.color == 'blue':
                    if blue > green and blue > red:
                        r = red
                        g = green
                        b = blue
                    else:
                        r = med
                        g = med
                        b = med
                elif self.color == 'green':
                    if green > red and green > blue:
                        r = red
                        g = green
                        b = blue
                    else:
                        r = med
                        g = med
                        b = med
                elif self.color == 'yellow':
                    if red > blue and green > blue and green > 200:
                        r = red
                        g = green
                        b = blue
                    else:
                        r = med
                        g = med
                        b = med
                elif self.color == 'ciano':
                    if blue > red and green > blue:
                        r = red
                        g = green
                        b = blue
                    else:
                        r = med
                        g = med
                        b = med
                elif self.color == 'purple':
                    if blue > red and blue > green and red > 100 and red < 200:
                        r = red
                        g = green
                        b = blue
                    else:
                        r = med
                        g = med
                        b = med
                elif self.color == 'pink':
                    if red > green and red > blue and blue > green and blue > 100:
                        r = red
                        g = green
                        b = blue
                    else:
                        r = med
                        g = med
                        b = med
                elif self.color == 'orange':
                    if red > green and red > blue and green > blue and green > 50 and green < 150:
                        r = red
                        g = green
                        b = blue
                    else:
                        r = med
                        g = med
                        b = med

                self.new_im.putpixel((x,y), (r, g, b))

    def save(self, path:str):
        '''
        Method responsible for saving the image with filter.
        '''
        self.new_im.save(path)

    def show(self):
        '''
        Method responsible for showing the image with filter.
        '''
        self.new_im.show()