import numpy as np
from renderer.renderer import WireframeRenderer
from PIL import ImageOps

if __name__ == '__main__':
    mode = 'triangle'
    obj = 'bunny'
    inpath = './examples/{}.obj'.format(obj)
    outpath = './images/{}_{}.png'.format(obj, mode)
    wf = WireframeRenderer()
    wf.readfile(inpath)

    im_list = []
    max_w, max_h = -np.inf, -np.inf
    for i in range(72):
        r = 100
        theta = 5 * i
        rad = np.pi * theta / 180
        camera = [r * np.cos(rad), 0, r * np.sin(rad)]
        center = [0, 0, 0]
        up = [0, 1, 0]

        canvas = wf.render(mode, camera, center, up)
        w, h = canvas.size
        max_w = max(w, max_w)
        max_h = max(h, max_h)
        im_list.append(canvas.img)

    im_list = [ImageOps.pad(img, (max_w, max_h), color=(255,255,255)) for img in im_list]
    im_list[0].save('images/{}_render.gif'.format(obj), save_all=True, append_images=im_list[1:], duration=100, loop=0)