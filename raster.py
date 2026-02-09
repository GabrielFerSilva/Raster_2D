import argparse
import importlib
from itertools import product
import time
import aliasing as al

import numpy as np

from tqdm import tqdm
import matplotlib.pyplot as plt

def main(args):
    xmin, xmax, ymin, ymax = args.window
    width, height = args.resolution
    samples_per_pixel = args.samples_per_pixel

    # create tensor for image: RGB
    image = np.zeros((height, width, 3))

    # Find coordinates for each pixel
    x_coords = [xmin + (xmax - xmin) * (i + 0.5) / width for i in range(width)]
    y_coords = [ymin + (ymax - ymin) * (j + 0.5) / height for j in range(height)]

    # load scene from file args.scene
    scene = importlib.import_module(args.scene).Scene()

    # for each pixel, determine if it is inside any primitive in the scene
    # use cartesian product for efficiency
    for j, i in tqdm(product(range(height), range(width)), total=height*width):
        point = (x_coords[i], y_coords[j])

        N = args.samples_per_pixel

        # generate points
        generated_points = al.aliasing_filter(args.aliasing,args.sigma,N)

        # set background color
        bg_color = list(scene.background.as_list())
        image[j, i] = bg_color

        #create summation array
        pixel_color = np.array([0.0, 0.0, 0.0])

        for x,y in generated_points:
            new_point = (point[0] + x, point[1] + y)

            sample_color = None

            # if point is inside any primitive, set pixel color to that primitive's color
            for primitive, color in scene:
                inside = primitive.in_out(new_point)
                if inside:
                    # Simple shading: use the red channel as intensity
                    sample_color = [color.r, color.g, color.b]
                    break
                
            if sample_color is None:
                sample_color = bg_color

            pixel_color += sample_color

        pixel_color[0] /= N
        pixel_color[1] /= N
        pixel_color[2] /= N
        
        image[j, i] = pixel_color

    # stability guarantee
    image = np.clip(image, 0, 1)

    # save image as png using matplotlib
    plt.imsave(args.output, image, vmin=0, vmax=1, origin='lower')


if __name__ == "__main__":
    raster_scene = 'lion_scene'
    aliasing_type = 'hat'
    # lion scene window = [-200, 400, -30, 420]
    # output_{raster_scene}_{resolution[0]}x{resolution[1]}_{aliasing_type}

    resolutions = [(256,144)]
    inicio = time.time()
    for resolution in resolutions:
        parser = argparse.ArgumentParser(description="Raster module main function")
        parser.add_argument('-s', '--scene', type=str, help='Scene name', default=raster_scene)
        parser.add_argument('-w', '--window', type=float, nargs=4, help='Window: xmin xmax ymin ymax', default=[-200, 400, -30, 420])
        parser.add_argument('-r', '--resolution', type=int, nargs=2, help='Resolution: width height', default=[resolution[0], resolution[1]])
        parser.add_argument('-a', '--aliasing', type=str, help='Anti Aliasing Filter', default=aliasing_type)
        parser.add_argument('-p', '--samples_per_pixel', type=int, help='Samples per Pixel', default='100')
        parser.add_argument('-q', '--sigma', type=float, help='Sigma for point distributions', default='1')
        parser.add_argument('-o', '--output', type=str, help='Output file name', default=f'output/tarefa 3/hat/tigrinho_hat.png')
        args = parser.parse_args()
        main(args)
    final = time.time() - inicio
    print(f'Tempo : {final:.2f} segundos')
