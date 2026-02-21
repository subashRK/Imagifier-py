import cv2
import sys
import numpy

# User defined libraries
from utils import truncate_img, compress

# Global variables
input_img_path, target_img_path = None, None

def process_img(input_img, target_img, threshold = 0.3, w = 256, h = 144):
    input_img, target_img = truncate_img(input_img, target_img)
    input_img, target_img = compress(input_img, target_img, w, h)

    cv2.imwrite(f"./output/{input_img_path.split("/")[-1]}", numpy.array(input_img))
    cv2.imwrite(f"./output/{target_img_path.split("/")[-1]}", numpy.array(target_img))

def main(args):
    if len(args) < 2:
        print("Please provide both input and target images paths!")
        exit(1)
    
    global input_img_path, target_img_path
    input_img_path, target_img_path = args[0], args[1]

    input_img = cv2.imread(input_img_path, cv2.IMREAD_COLOR)
    target_img = cv2.imread(target_img_path, cv2.IMREAD_COLOR)

    if input_img is None or target_img is None:
        print("Invalid image path!")
        exit(1)

    # Here converted to python list from np arr, to avoid errors like 'could not broadcast input array from shape' (and also to avoid numpy :\ )
    process_img(list(input_img), list(target_img))

if __name__ == "__main__":
    main(sys.argv[1:])
