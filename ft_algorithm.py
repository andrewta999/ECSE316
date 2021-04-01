import numpy as np 

def FT_1D(img):
    """ Perform the naive Fourier Transform on 1D array
    Paramters
    ---------
    img: 1D numpy array

    Returns
    -------
    1D numpy array
    """
    # Step 1: get image size
    N = img.shape[0]
    result = np.zeros(N, dtype=complex)

    # Step 2: perform DFT
    for k in range(N):
        temp = 0
        for n in range(N):
            temp += img[n] * np.exp(-2j * np.pi * k * n / N)
        result[k] = temp
    
    return result 


def inverse_FT_1D(img):
    """ Perform the naive Inverse Fourier Transform on 1D array
    Paramters
    ---------
    img: 1D numpy array

    Returns
    -------
    1D numpy array
    """
    # Step 1: get image size
    N = img.shape[0]
    result = np.zeros(N, dtype=complex)

    # Step 2: perform IDFT
    for k in range(N):
        temp = 0
        for n in range(N):
            temp += img[n] * np.exp(2j * np.pi * k * n / N)
        result[k] = temp/N
    
    return result 


def FFT_1D(img):
    """ Perform the Fast Fourier Transform on 1D array
    Paramters
    ---------
    img: 1D numpy array

    Returns
    -------
    1D numpy array
    """
    # Step 1: get image size
    N = img.shape[0]
    result = np.zeros(N, dtype=complex)

    # Step 2: perform FFT
    # threshold 
    if N <= 4:
        return FT_1D(img)
    
    # divide image into two equal parts
    # and perform FFT on each part recursively
    even = FFT_1D(img[::2])
    odd = FFT_1D(img[1::2])

    # merge two parts 
    M = N//2
    for k in range(N):
        result[k] = even[k % M] + np.exp(-2j * np.pi * k / N) * odd[k % M]
    return result


def inverse_FFT_1D(img):
    """ Perform the Inverse Fast Fourier Transform on 1D array
    Paramters
    ---------
    img: 1D numpy array

    Returns
    -------
    1D numpy array
    """
    # Step 1: get image size
    N = img.shape[0]
    result = np.zeros(N, dtype=complex)

    # Step 2: perform FFT
    # threshold 
    if N <= 4:
        return inverse_FT_1D(img)
    
    # divide image into two equal parts
    # and perform FFT on each part recursively
    even = inverse_FFT_1D(img[::2])
    odd = inverse_FFT_1D(img[1::2])

    # merge two parts 
    M = N//2
    for k in range(N):
        result[k] = even[k % M] + np.exp(2j * np.pi * k / N) * odd[k % M]
        result[k] /= 2
    return result


def FT_2D(img):
    """ Perform the naive Fourier Transform on 2D array
    Paramters
    ---------
    img: 2D numpy array

    Returns
    -------
    2D numpy array
    """
    N, M = img.shape
    result = np.zeros((N, M), dtype=complex)

    for k in range(N):
        for l in range(M):
            for m in range(M):
                for n in range(N):
                    result[k, l] += img[n, m] * np.exp(-2j * np.pi * ((l * m / M) + (k * n / N)))

    return result 


def inverse_FT_2D(img):
    """ Perform the naive Inverse Fourier Transform on 2D array
    Paramters
    ---------
    img: 2D numpy array

    Returns
    -------
    2D numpy array
    """
    N, M = img.shape
    result = np.zeros((N, M), dtype=complex)

    for k in range(N):
        for l in range(M):
            for m in range(M):
                for n in range(N):
                    result[k, l] += img[n, m] * np.exp(2j * np.pi * ((l * m / M) + (k * n / N)))
            result[k, l] /= M * N

    return result 


def FFT_2D(img):
    """ Perform the Fast Fourier Transform on 2D array
    Paramters
    ---------
    img: 2D numpy array

    Returns
    -------
    2D numpy array
    """
    # Step 1: get row and column
    R, C = img.shape 
    result = np.zeros((R, C), dtype=complex)

    # Step 2: perform Fourier transform on row
    for r in range(R):
        result[r, :] = FFT_1D(img[r, :])

    # Step 3: perform Fourier transform on column
    for c in range(C):
        result[:, c] = FFT_1D(result[:, c])

    return result 


def inverse_FFT_2D(img):
    """ Perform the Inverse Fast Fourier Transform on 2D array
    Paramters
    ---------
    img: 2D numpy array

    Returns
    -------
    2D numpy array
    """
    # Step 1: convert to 2D np-array
    R, C = img.shape
    result = np.zeros((R, C), dtype=complex)

    # Step 2: perform Fourier transform on row
    for r in range(R):
        result[r, :] = inverse_FFT_1D(img[r, :])

    # Step 3: perform Fourier transform on column
    for c in range(C):
        result[:, c] = inverse_FFT_1D(result[:, c])

    return result 