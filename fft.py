import argparse
import math 
import time
import cv2 
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.colors import LogNorm 

from ft_algorithm import FFT_2D, inverse_FFT_2D, FT_2D


def get_new_size(s):
    p = int(math.log(s, 2)) + 1
    return int(pow(2, p))


def resize_and_FFT(image):
    """ Resize the image to power of 2
    the take the FFT transform
    """
    # Step 1: read the image
    img = plt.imread(image).astype(float)
    # Step 2: get image's sizes and new sizes
    h, w = img.shape 
    dim = (get_new_size(w), get_new_size(h))
    # Step 3: resize the image
    new_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    # Step 4: perform FFT
    new_img2 = FFT_2D(new_img)
    # return the new image
    return img, new_img2 


def plot_mode1(original_img, new_img):
    fig, sub = plt.subplots(1, 2)
    sub[0].imshow(original_img, plt.cm.gray)
    sub[0].set_title('Original image')
    sub[1].imshow(np.abs(new_img), norm=LogNorm())
    sub[1].set_title('FFT on image')
    fig.suptitle(f'Mode 1')
    plt.show()


def plot_mode2(original_img, new_img):
    fig, sub = plt.subplots(1, 2)
    sub[0].imshow(original_img, plt.cm.gray)
    sub[0].set_title('Original image')
    sub[1].imshow(new_img, plt.cm.gray)
    sub[1].set_title('Denoised image')
    fig.suptitle(f'Mode 2')
    plt.show()


def mode1(image):
    """ Mode 1: perform FFT on an image
    and plot both images (original, and FFT)
    Paramters
    ---------
    image : str 
        image's name
    """
    # Step 1: resize image and perform 2d-FFT
    img, new_img = resize_and_FFT(image)

    # Step 2: plot the results
    plot_mode1(img, new_img)
    

def mode2(image):
    """ Mode 1: denoise an image 
    Paramters
    ---------
    image : str 
        image's name
    """
    # Step 1: resize and perform 2D-FFT
    img, new_img = resize_and_FFT(image)

    # Step 3: filter out high frequencies
    # keep ratio
    keep = 0.05
    # get row and column
    r, c = new_img.shape 
    # set to zero all rows with indices between r*keep_fraction and r*(1-keep_fraction):
    new_img[int(r * keep) : int(r * (1 - keep))] = 0   
    new_img[:, int(c * keep) : int(c * (1 - keep))] = 0

    # Step 4: perform inverse FFT to reconstruct the image (keep only the real part for display)
    new_img2 = inverse_FFT_2D(new_img).real 

    # Step 5: plot two images and print results to stdout
    print(f"Fraction of non-zeros: {keep}")
    print(f"Number of non-zerors: ({r*keep}, {c*keep}) out of ({r}, {c})")
    plot_mode2(img, new_img2)
    
    
def mode3(image):
    """ Compress the image
    """ 
    # Step 1: resize and take the FFT
    img, new_img = resize_and_FFT(image)
    


def mode4(image):
    """ Plot the run-time graph of 2D-FFT and naive 2D-FT
    """
    # plot
    fig, ax = plt.subplots()
    ax.set_xlabel('size')
    ax.set_ylabel('runtime (second)')

    methods = [FFT_2D, FT_2D]
    names = ["FFT", "Naive DFT"]
    color = ['green', 'cyan']
    for i in range(2):
        print(f"Algorithm: {names[i]}")
        x_data = []
        y_data = []
        err = []

        size = 2**5
        while size <= 2**12:
            x_data.append(size)
            M = int(math.sqrt(size))
            mock_data = np.random.rand(M, M)

            stats = []
            for j in range(10):
                start = time.time()
                methods[i](mock_data)
                end = time.time()
                stats.append(end - start)

            mean = np.mean(stats)
            sd = np.std(stats)
            err.append(sd)

            print(f"Size {size}: mean {mean}, stdev {sd}")
            y_data.append(mean)

            # multiply problem size by 4
            size *= 4

        plt.errorbar(x_data, y_data, yerr=err, fmt=color[i])
    plt.show()


def parse_cli():
    """
    Parse a command 
    Returns
    -------
    dict: 
        A dictionary of parameters (mode, image)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', action='store', dest='mode',
                        help='Mode: [1] FFT, [2] Denoise, [3] Compress, [4] Plot', type=int, default=1)
    parser.add_argument('-i', action='store', dest='image',
                        help='Input image', type=str, default='moonlanding.png')
    return parser.parse_args()


def main():
    # Parse commands from users
    params = parse_cli()
    # get mode and image
    mode = params.mode
    image = params.image  
    # select mode
    if mode == 1:
        mode1(image)
    elif mode == 2:
        mode2(image)
    elif mode == 3:
        mode3(image)
    elif mode == 4:
        mode4(image)
    else:
        print("Mode must be between 1 and 4")
    

if __name__ == "__main__":
    main() 