import numpy as np
import cv2

# Find the biggest contour
def biggest_contour(contours):
    biggest = np.array([])
    max_area = 0
    # look for all found contours, limit their number to 10, and calculate the contour area
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:                 #filter out small contours by area
            #search for contours with only four corners
            peri = cv2.arcLength(i, True)       #define a curve and if the shape is closed
            approx = cv2.approxPolyDP(i, 0.015 * peri, True)        #approximate the contour to another shape; ( define the curve, approximation accuracy, true-> if the curve is closed)
            if area > max_area and len(approx) == 4:                #search for  a max area and only if the contour has four corners
                biggest = approx
                max_area = area
    return biggest


#detect edges
def detect_edge(img):
    # Convert image to grayscale, apply bilateral filtering, and perform Canny edge detection. 
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply bilateral filter to remove noise while keeping edges sharp
    gray = cv2.bilateralFilter(gray, 20, 30, 30)
    
    # Perform Canny edge detection
    edged = cv2.Canny(gray, 10, 20)

    return edged

#align image
def align_image(edged, img, img_original):
    
    #step1: detect contour of the document
    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    #detect contours in hierarchy
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]             #sort contours
    biggest = biggest_contour(contours)                                             #search for the biggest contours with four corners
    
    # draw the biggest contour
    cv2.drawContours(img, [biggest], -1, (0, 255, 0), 3)                            
    
    #step2: reorder and find the right contours
    # Pixel values in the original image
    points = biggest.reshape(4, 2)                                  #reshape contour points to have four lists with two places in a list
    input_points = np.zeros((4, 2), dtype="float32")                #storage of contra corner point coordinates in the correct order
    
    #sum and differences of coordinates to identify corners
    #note that the top-left and the bottom-right will have the smallest and largest sum respectively.
    #sum x and y coordinates together by specifying an axis equal to one
    points_sum = points.sum(axis=1)     
    input_points[0] = points[np.argmin(points_sum)]     #top-left
    input_points[3] = points[np.argmax(points_sum)]     #bottom-right

    # the top right and bottom left points -> smallest and largest difference, at this point we'll have all corner points
    points_diff = np.diff(points, axis=1)
    input_points[1] = points[np.argmin(points_diff)]        #top-right
    input_points[2] = points[np.argmax(points_diff)]        #bottom-left


    #step3: calculate the new dimensions
    #calculate the dimensions of our new image-> calculate the distance between points coordinates
    (top_left, top_right, bottom_right, bottom_left) = input_points     #unpack the corner points
    #calculate the bottom width of the image by computing the distance between the x coordinates of bottom right and the bottom left points
    bottom_width = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))   
    # for top width, calculate the distance top right and left coordinates
    top_width = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))
    right_height = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))
    left_height = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))

    # Define the output image size, 
    # use the maximum width and height, so use the max function and convert our input to int 
    max_width = max(int(bottom_width), int(top_width))
    # max_height = max(int(right_height), int(left_height))
    max_height = int(max_width * 1.414)  # for A4
    
    #perspective transformation
    converted_points = np.float32([
        [0, 0], 
        [max_width, 0], 
        [0, max_height], 
        [max_width, max_height]
        ])
    matrix = cv2.getPerspectiveTransform(input_points, converted_points)
    img_output = cv2.warpPerspective(img_original, matrix, (max_width, max_height))
    
    return img_output
    
#reduce noise for the image
def reduce_noise(img):  
    blurred = cv2.GaussianBlur(img, (5, 5), 0)  
    return blurred

#enhance contrast (CLAHE)
def enhance_contrast(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    #converted to grayscale
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))  
    enhanced = clahe.apply(img_gray)  
    return enhanced