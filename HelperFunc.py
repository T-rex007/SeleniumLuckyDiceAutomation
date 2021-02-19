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

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
        print("Action Performed!")
    except TimeoutException:
        print("Loading took too much time!")

