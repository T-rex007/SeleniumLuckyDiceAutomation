"""
Author: Tyrel Cadogan
Email: shaqc777@yahoo.com
Github:  
Decription: 
"""
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import base64
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def getTemplate(TEMPLATE_NAME):
    return cv2.imread('imgs/templates/{}.png'.format(TEMPLATE_NAME),0)

def getGameImage(driver, el_class_name = None):
    """Returns gray scale Image of the canvas """
    
    c1_element = driver.find_element_by_id(el_class_name)
    canvas = c1_element.screenshot_as_base64
    cap = base64.b64decode(canvas)
    image = cv2.imdecode(np.frombuffer(cap, np.uint8), 1)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def detectTemplate(image, template, visualize = False, method_num = -1):
    img2 = image
    w, h = template.shape[::-1]
    # All the 6 methods for comparison in a list
    methods = [['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED'][method_num]]
    # methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
    #             'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    for meth in methods:
        img = img2.copy()
        method = eval(meth)
        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        ### Visualize the Detection?
        if(visualize == True):
            cv2.rectangle(img,top_left, bottom_right, 255,20)
            plt.subplot(121),plt.imshow(res,cmap = 'gray')
            plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            plt.subplot(122),plt.imshow(img,cmap = 'gray')
            plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            plt.suptitle(meth)
            plt.show()
    return (top_left, bottom_right, res)

def clickScreen(driver, top_left):
    try:
        #myElem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CLASS_NAME, 'game')))
        game_element = driver.find_element_by_class_name("game")
        myElem = game_element
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(myElem, top_left[0] + 50, top_left[1] + 50)
        action.click()
        action.perform()
        #print("Action Performed!")
    except TimeoutException:
        print("Loading took too much time!")

def decodeString(input_string):
    num_dict = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5,'Six': 6}
    for key,value in num_dict.items():
        if(key == input_string):
            return value
    return 0


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((2,2),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

def cropRegion(r, img):
    return img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]


def colorThreshold(img, rbg_threshold = (60,60,60)):
    """
    Return Binary Image which is thresholded by thr rbg pixel vales 
    given in rbg_threshold i.e. If pixel is > thres assign 1
    and if pixel is < thres assing 0
    args:
          img - img to be thresholded
          rbg_threshold - (r,g,b)
    """
    temp = np.zeros(img.shape)
    rflags_h = img[:,:]>rbg_threshold[0]

    temp[:,:][rflags_h] = 1
    
    return temp

def retrieveAmount(driver, game_image):
    """
    Return current Amount (int) the player currently has.
    args: Created Selenium webdriver
    """
    bal_region = (987, 653, 272, 63)
    game_img = getGameImage(driver, "layer2")
    # Crop image
    imCrop = game_image[int(bal_region[1]):int(bal_region[1]+bal_region[3]), 
                        int(bal_region[0]):int(bal_region[0]+bal_region[2])]
    im1 = thresholding(imCrop)
    plt.imshow(imCrop)
    img1 = np.abs(im1.astype( int) - 255)
    img1 = np.array(img1).astype('uint8')
    custom_config = r'--oem 3 --psm 6'
    string_balance = pytesseract.image_to_string(img1, config=custom_config)
    print("OCR String")
    print(string_balance)
    tmp = int(string_balance.split('\n')[0][:-2].replace(',', '').replace(';', '').replace('.','').replace(':', ''))
    return tmp

def setAmount(driver,num_clicks, board_coord):
    for i in range(int(num_clicks -1)):
        game_image = getGameImage(driver, "layer2")
        clickScreen(driver,board_coord[0])
