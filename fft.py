import argparse
import math 
import time
import cv2 
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.colors import LogNorm 

from ft_algorithm import FFT_2D, inverse_FFT_2D, FT_2D


def get_new_size(s):
    """ Compute the nearest power of 2 of a number
    Parameters
    ----------
    s : int 

    Returns
    -------
    int
    """
    p = int(math.log(s, 2)) + 1
    return int(pow(2, p))


def resize_and_FFT(image):
    """ Resize the image to size of power of 2, then take the FFT transform
    Parameters
    ----------
    image : 2D numpy array

    Returns
    -------
    2D numpy array
    """
    # Step 1: read the image
    img = plt.imread(image).astype(float)

    # Step 2: get image's sizes and new sizes
    h, w = img.shape 
    dim = (get_new_size(w), get_new_size(h))

    # Step 3: resize the image
    new_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    # Step 4: perform FFT
    # new_img2 = FFT_2D(new_img)
    new_img2 = np.fft.fft2(new_img)

    # return the new image
    return img, new_img2 


def mode1(image):
    """ Mode 1: perform FFT on an image, and plot both images (original, and FFT)
    Paramters
    ---------
    image : str 
        image's name
    """
    # Step 1: resize image and perform 2d-FFT
    img, new_img = resize_and_FFT(image)

    # Step 2: plot the results
    plot, sub_plot = plt.subplots(1, 2)
    sub_plot[0].imshow(original_img, plt.cm.gray)
    sub_plot[0].set_title('Original image')
    sub_plot[1].imshow(np.abs(new_img), norm=LogNorm())
    sub_plot[1].set_title('FFT on image')
    plot.suptitle(f'Mode 1')
    plt.show()
    

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
    # set to zero all rows and columns with fractions between keep_fraction and (1-keep_fraction):
    new_img[int(r * keep) : int(r * (1 - keep))] = 0   
    new_img[:, int(c * keep) : int(c * (1 - keep))] = 0

    # Step 4: perform inverse FFT to reconstruct the image (keep only the real part for display)
    new_img2 = inverse_FFT_2D(new_img).real 

    # Step 5: plot two images and print results to stdout
    print(f"Fraction of non-zeros: {keep}")
    print(f"Number of non-zerors: ({r*keep}, {c*keep}) out of ({r}, {c})")
    plot, sub_plot = plt.subplots(1, 2)
    sub_plot[0].imshow(original_img, plt.cm.gray)
    sub_plot[0].set_title('Original image')
    sub_plot[1].imshow(new_img, plt.cm.gray)
    sub_plot[1].set_title('Denoised image')
    plot.suptitle(f'Mode 2')
    plt.show()
    

def compress1(img, level):
    """ Compress method 1
    Keep all very low frequencies and a fraction of high frequencies
    Parameters
    ----------
    img : 2D numpy array
    level : int
        compresion level    

    Returns 
    -------
    2D numpy array
    """
    # get keep lower and upper bound for filtering
    keep = 100 - level
    lower = np.percentile(img, keep//2)
    upper = np.percentile(img, 100 - keep//2)

    # filter the image wit lower and upper bounds
    compressed_img = img * np.logical_or(img <= lower, img >= upper)

    # perform the inverse FFT and return 
    return np.fft.ifft2(compressed_img)


def compress2(img, level):
    """ Compress method 2
    Threshold the coefficients' magnitude and take only the largest percentile of them
    Parameters
    ----------
    img : 2D numpy array
    level : int
        compresion level    

    Returns 
    -------
    2D numpy array
    """
    # get the dimension of the image
    dim = img.shape 

    # get the magnitude
    temp = np.abs(img)

    # get the indices of 'level' number of smallest magnitudes
    index = np.argpartition(temp, level, axis=None)

    # flatten the image and set 'level' smallest magnitudes to 0
    img_temp = img.flatten()
    for i in range(level):
        img_temp[index[i]] = 0

    # rebuild the image
    compressed_img = np.reshape(img_temp, dim)

    # perform IFFT and return 
    return np.fft.ifft2(compressed_img)


def mode3(image):
    """ Compress the image
    Parameters
    ----------
    img : 2D numpy array
    """ 
    # Step 1: resize and take the FFT
    img, new_img = resize_and_FFT(image)
    R, C = new_img.shape 

    # Step 2: compress the image and save compressed images
    compression = [[0, 15, 30], [50, 75, 95]]
    plot, ax = plt.subplots(2, 3)
    plot.suptitle('Mode 3')
    for i in range(2):
        for j in range(3):
            level = compression[i][j]
            # print to stdout
            print(f"Compression level {level}:")
            print(f"\tSize: {R*C}")
            print(f"\tNumber of non-rezos: {R*C*(100-level)//100}")

            # compress the image and add to plot
            compressed_img = compress1(new_img, level)
            ax[i, j].imshow(compressed_img.real, plt.cm.gray)
            ax[i, j].set_title(f"Compression level: {level}")

            # save the image
            np.savetxt(f"compression_level_{level}.txt", compressed_img)

    plt.show()



     
def mode4(image):
    """ Plot the run-time graph of 2D-FFT and naive 2D-FT
    Parameters
    ----------
    img : 2D numpy array
    """
    # initialize a plot
    plot, ax = plt.subplots()
    ax.set_xlabel('size')
    ax.set_ylabel('runtime (second)')

    # define some lists
    methods = [FFT_2D, FT_2D]
    names = ["FFT", "Naive DFT"]
    color = ['green', 'cyan']

    # iteratively experiment with 2 algorithms
    for i in range(2):
        print(f"Algorithm: {names[i]}")
        
        # list to store data
        x_data = [] # data for x axis
        y_data = [] # data for y axis
        err = []    # data for standard deviation

        size = 2**5 # problem size
        while size <= 2**12:
            # append size to x_data
            x_data.append(size)

            # create mock data 
            M = int(math.sqrt(size))
            mock_data = np.random.rand(M, M)

            # list to store results of 10 trials
            record = []
            # run 10 trials
            for j in range(10):
                # record the measurements
                start = time.time()
                methods[i](mock_data)
                end = time.time()
                record.append(end - start)

            # compute the mean and stdev of the measurements
            mean = np.mean(record)
            sd = np.std(record)
            err.append(sd)

            # print to stdout
            print(f"Size {size}: mean {mean}, stdev {sd}")

            # append data to y_data
            y_data.append(mean)

            # update problem size
            size *= 4

        # plot the results
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
    parser.add_argument('-m', action='store', dest='mode', help="Mode (1-4)", type=int, default=1)
    parser.add_argument('-i', action='store', dest='image', help="Image name", type=str, default='moonlanding.png')
    return parser.parse_args()


def main():
    """ Main function
    """
    # parse the command
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