import argparse
import importlib
from itertools import product
import time

import numpy as np

from tqdm import tqdm
import matplotlib.pyplot as plt

def main(args):
    xmin, xmax, ymin, ymax = args.window
    width, height = args.resolution
    aliasing_filter = args.aliasing
    samples_per_pixel = args.samples_per_pixel

    # create tensor for image: RGB
    image = np.zeros((height, width, 3))

    # Find coordinates for each pixel
    x_coords = [xmin + (xmax - xmin) * (i + 0.5) / width for i in range(width)]
    y_coords = [ymin + (ymax - ymin) * (j + 0.5) / height for j in range(height)]

    # load scene from file args.scene
    scene = importlib.import_module(args.scene).Scene()

    # uniforme pra pegar os pontos

    #b-a/N somatorio das f's


    # for each pixel, determine if it is inside any primitive in the scene
    # use cartesian product for efficiency
    for j, i in tqdm(product(range(height), range(width)), total=height*width):
        point = (x_coords[i], y_coords[j])
        # set background color
        image[j, i] = list(scene.background.as_list())
        # if point is inside any primitive, set pixel color to that primitive's color
        for primitive, color in scene:
            inside = primitive.in_out(point)
            if inside:
                # Simple shading: use the red channel as intensity
                image[j, i] = [color.r, color.g, color.b]
                break  # Stop at the first primitive that contains the point

    # save image as png using matplotlib
    plt.imsave(args.output, image, vmin=0, vmax=1, origin='lower')

# implementar gradiente?

if __name__ == "__main__":
    raster_scene = 'implicit_scene'

    # lion scene window = [-200, 400, -30, 420]

    resolutions = [(256,144),(426,240),(480,360),(640,480),(1280,720),(1920,1080),(2560,1440),(3840,2560)]
    inicio = time.time()
    for resolution in resolutions:
        parser = argparse.ArgumentParser(description="Raster module main function")
        parser.add_argument('-s', '--scene', type=str, help='Scene name', default=raster_scene)
        parser.add_argument('-w', '--window', type=float, nargs=4, help='Window: xmin xmax ymin ymax', default=[-3, 3, -3, 3])
        parser.add_argument('-r', '--resolution', type=int, nargs=2, help='Resolution: width height', default=[resolution[0], resolution[1]])
        parser.add_argument('-a', '--aliasing', type=str, help='Anti Aliasing Filter', default='escrever algo aqui')
        parser.add_argument('-p', '--samples_per_pixel', type=int, help='Samples per Pixel', default='escrever algo aqui')
        parser.add_argument('-o', '--output', type=str, help='Output file name', default=f'output/output_{raster_scene}_{resolution[0]}x{resolution[1]}.png')
        args = parser.parse_args()
        main(args)
    final = time.time() - inicio
    print(f'Tempo : {final:.2f} segundos')