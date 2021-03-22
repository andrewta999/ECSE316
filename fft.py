import argparse
import math 
import cv2 
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.colors import LogNorm 

from ft_algorithm import FFT_2D, inverse_FFT_2D


def get_new_size(s):
    p = int(math.log(s, 2)) + 1
    return int(pow(2, p))


def resize_image(image):
    # resize the image to power of 2
    # Step 1: read the image
    img = plt.imread(image).astype(float)
    # Step 2: get image's sizes and new sizes
    h, w = img.shape 
    dim = (get_new_size(w), get_new_size(h))
    # Step 3: resize the image
    new_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    print("Original size: ", img.shape)
    print("New size: ", new_img.shape)

    # return resized image
    return new_img 


def mode1(image):
    # Mode 1
    # Step 1: resize image
    img = resize_image(image)

    # Step 2: perform 2D-FFT
    new_img = FFT_2D(img)
    # new_img1 = np.fft.fft2(img)

    # Step 3: plot the results
    fig, sub = plt.subplots(1, 2)
    sub[0].imshow(img, plt.cm.gray)
    sub[0].set_title('Original image')
    # sub[0].imshow(np.abs(new_img1), norm=LogNorm())
    # sub[0].set_title('FFT2')
    sub[1].imshow(np.abs(new_img), norm=LogNorm())
    sub[1].set_title('FFT on image')
    fig.suptitle('Mode 1')
    plt.show()

def mode2(image):
    pass 

def mode3(image):
    pass 

def mode4(image):
    pass 


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