from PIL import Image, ImageDraw, ImageOps

class WireframeCanvas:
    def __init__(self, imsize, fg_color, bg_color):

        self.imsize = imsize
        self.fg_color = fg_color
        self.bg_color = bg_color

        self.img = Image.new('RGB', self.imsize, self.bg_color)
        self.draw = ImageDraw.Draw(self.img)
    
    def drawline(self, c1, c2):
        self.draw.line([c1, c2], fill=self.fg_color)
    
    def drawpoly(self, coors, fill):
        self.draw.polygon(coors, fill=fill)
    
    def verticalFlip(self):
        self.img = ImageOps.flip(self.img)

    def show(self):
        self.img.show()
    
    def save(self, path):
        self.img.save(path)
    
    def close(self):
        self.img.close()
    
    @property
    def size(self):
        return self.img.size

def test():
    wf = WireframeCanvas()
    wf.drawline((100, 350), (150, 300))
    wf.show()

if __name__ == '__main__':
    test()