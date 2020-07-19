import numpy as np
from renderer.renderer import WireframeRenderer

if __name__ == '__main__':
    mode = 'triangle'
    obj = 'bunny'
    inpath = './examples/{}.obj'.format(obj)
    outpath = './images/{}_{}.png'.format(obj, mode)
    wf = WireframeRenderer()
    wf.readfile(inpath)

    im_list = []
    for i in range(72):
        r = 100
        theta = 5 * i
        rad = np.pi * theta / 180
        camera = [r * np.cos(rad), 0, r * np.sin(rad)]
        center = [0, 0, 0]
        up = [0, 1, 0]

        canvas = wf.render(mode, camera, center, up)
        im_list.append(canvas.img)

    im_list[0].save('images/{}_render.gif'.format(obj), save_all=True, append_images=im_list[1:], duration=100, loop=0)