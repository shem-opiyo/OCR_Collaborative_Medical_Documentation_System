import cv2
import numpy as np

def preprocess_image(image_path):
    image = cv2.imread(image_path)

    # 1. Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. CLAHE for contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    contrast = clahe.apply(blurred)

    # 4. Edge detection
    edges = cv2.Canny(contrast, 100, 200)

    # 5. Thresholding
    _, thresh = cv2.threshold(contrast, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh
