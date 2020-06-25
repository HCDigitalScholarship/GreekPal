import cv2 as cv2
import numpy as np
import math

OUTPUT_IMAGE_SIZE = 400

"""
Python script that preprocess one image at a time
Main function to be called to preprocess the image is get_preprocessed_image(image)

get_preprocessed_image(image) reads from path, it takes the already read in 
image as a parameter and returns preprocessed grayscale image 

"""


def get_contrasted_image(image):
  new_image = np.zeros(image.shape, image.dtype)
  alpha = 2.2
  beta = 0
  new_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
  cv2.waitKey()
  return new_image

def get_outlined_image(image):
  # Otsu's thresholding after Gaussian filtering
  blur = cv2.GaussianBlur(image,(5,5),0)
  ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

  kernel = np.ones((3,3), np.uint8) 
#   closing = cv2.morphologyEx(th3, cv2.MORPH_CLOSE, kernel)
  return th3

def get_resized_image(test_image):
  input_width = test_image.shape[1]
  input_height = test_image.shape[0]

  scale_factor = OUTPUT_IMAGE_SIZE / max(input_height, input_width)

  needed_width = int(input_width * scale_factor)
  needed_height = int(input_height * scale_factor) 
  dim = (needed_width, needed_height)

  # resize image
  test_image = cv2.resize(test_image, dim, interpolation = cv2.INTER_AREA)

  blank_image = 255 * np.ones(shape=[OUTPUT_IMAGE_SIZE, OUTPUT_IMAGE_SIZE, 3], dtype=np.uint8)
  blank_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)

  x_offset = int((OUTPUT_IMAGE_SIZE - test_image.shape[1])/2)
  y_offset = int((OUTPUT_IMAGE_SIZE - test_image.shape[0])/2)

  blank_image[ y_offset:y_offset+test_image.shape[0], x_offset:x_offset+test_image.shape[1]] = test_image
  return blank_image


def get_preprocessed_image(path):
    image = cv2.imread(path,0)
    # first convert to grayscale if it's not already
    if len(image.shape)>2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # contrast the image for better thresholding results
    contrasted_image = get_contrasted_image(image)

    # outline symbols using Otsu's thresholding
    outlined_image = get_outlined_image(contrasted_image)

    # resize image
    resized_image = get_resized_image(outlined_image)
    cv2.imwrite(path.replace('original','cleaned'),resized_image)

def resize_image(path):
    image = cv2.imread(path,0)
    # first convert to grayscale if it's not already
  
    # resize image
    resized_image = get_resized_image(image)
    cv2.imwrite(path,resized_image)

    
