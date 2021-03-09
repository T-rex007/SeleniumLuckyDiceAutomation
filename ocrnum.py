import HelperFunc as hf
import pytesseract
import cv2
import time
import numpy as np
import pandas as pd
import base64
import sys
import argparse
import matplotlib.pyplot as plt

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime

def getDiceNum(driver):
    """
    Returns a tuple of integers representing the dice numbers 
    """
    game_image = hf.getGameImage(driver, 'layer2')       
    r1 = (1065, 188, 84, 35)
    r2  = (1160, 189, 86, 33)
    imCrop1 = game_image[int(r1[1]):int(r1[1]+r1[3]), int(r1[0]):int(r1[0]+r1[2])]
    imCrop2 = game_image[int(r2[1]):int(r2[1]+r2[3]), int(r2[0]):int(r2[0]+r2[2])]
    ### Preprocess Image
    thresh_image1 = hf.thresholding(imCrop1)
    thresh_image2 = hf.thresholding(imCrop2)
    img1 = np.abs(thresh_image1.astype( int) - 255)
    img2 = np.abs(thresh_image2.astype( int) - 255)
    img1 = np.array(img1).astype('uint8')
    img2 = np.array(img2).astype('uint8')
    ### Perform OCR to retreive dice roll
    custom_config = r'--oem 3 --psm 6'
    str1 = pytesseract.image_to_string(img1, config=custom_config)
    str2 = pytesseract.image_to_string(img2, config=custom_config)
    num1 = hf.decodeString(str1.split('\n')[0])
    num2 = hf.decodeString(str2.split('\n')[0])
    return (num1, num2)
if __name__ == '__main__':
    ### Initialize Diver
    driver = webdriver.Firefox()
    driver.get("https://logigames.bet9ja.com/games.ls?page=launch&gameid=18000&skin=12&sid=&pff=1&tmp=1611946195")
    time.sleep(5)
    driver.set_window_size(1280,947)
    k = input("Enter: ")
    print(driver.get_window_size())
    k = 'n'
    while(k =='n'):
        print(getDiceNum(driver))
        k = input("Enter: ")
    driver.close()
