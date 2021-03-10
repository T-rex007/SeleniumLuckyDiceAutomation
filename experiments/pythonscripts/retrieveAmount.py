#!/usr/bin/env python3
"""
Author: Tyrel Cadogan
Email : shaqc777@yahoo.com
Github: https://github.com/T-rex007
"""
import HelperFunc as hf
import numpy as np
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


amount_dict = {'amt_region':(1098, 478), '50': (915, 484), '250':(800, 485), 
                '1k':(676, 485), '5k':(553, 485), '25k':(434, 484), 
                '250k': (309, 484), '1m': (184, 484)}
amt_val_dict  = { '50': 50, '250':250, 
                '1k':1000, '5k':5000, '25k':25000, 
                '250k': 250000, '1m': 1000000}


def optimizeAmtClick(amt):
    """
    Returns a optimized list of the amounts to click in the game to minimize 
    """
    
    amt_val_lst  = [50,250,1000, 5000,25000,250000,1000000]
    amt_key_lst  = ['50','250','1k','5k','25k','250k','1m']
    key_lst = []
    while(amt != 0):
        if(np.max(amt_val_lst)<=amt):
            key_lst.append(amt_key_lst[np.argmax(amt_val_lst)])
            amt = amt- np.max(amt_val_lst)
        else:
            amt_val_lst.pop()
    return key_lst

def setAmountV2(amt, amount_dict, board_dict):
    """
    Performs the optimal clicks for the given amt
    args:
        amt - Stake
        amount_dict - Dictionary of coordinates for amount selections
        board_dict - Dictionary of coordinates for board selection
    """
    key_lst =optimizeAmtClick(amt);
    for k in key_lst:
        hf.clickScreen(driver,amount_dict['amt_region'])
        hf.clickScreen(driver,amount_dict[k])
        hf.clickScreen(driver,board_dict[board_type][0])

def retrieveBalance(driver, game_image):
    """
    Return current Amount (int) the player currently has.
    args: Created Selenium webdriver
    """
    bal_region = (1058, 8, 194, 37)
    game_img = hf.getGameImage(driver, "layer2")
    # Crop image
    imCrop = game_image[int(bal_region[1]):int(bal_region[1]+bal_region[3]), 
                        int(bal_region[0]):int(bal_region[0]+bal_region[2])]
    im1 = hf.thresholding(imCrop)
    plt.imshow(imCrop)
    img1 = np.abs(im1.astype( int) - 255)
    img1 = np.array(img1).astype('uint8')
    custom_config = r'--oem 3 --psm 6'
    string_balance = pytesseract.image_to_string(img1, config=custom_config)
    print("OCR String")
    print(string_balance)
    try:
        tmp = int(string_balance.split('\n')[0][:-2].replace(',', '').replace(';','').replace('.','').replace(':',''))
    except:
        print("Oh No something went wrong with the OCR for the amount balance")
    return tmp
    

if(__name__ =="__main__"):

    driver = webdriver.Firefox()
    driver.get("https://logigames.bet9ja.com/games.ls?page=launch&gameid=18000&skin=12&sid=&pff=1&tmp=1611946195")
    time.sleep(5)
    GAME_CANVAS = 'layer2'
    driver.set_window_size(1280,947)
    game_image = hf.getGameImage(driver, GAME_CANVAS)
    board_type = 'mid'

    ### Press Continue
    tmp =  hf.getTemplate("continue")

    coord  = hf.detectTemplate(game_image, tmp, False, -1)
    hf.clickScreen(driver,coord[0])

    ### Select Board
    board_dict = hf.getAllBoardCoord(driver)
    tmp =  hf.getTemplate(board_type)
    game_image = hf.getGameImage(driver, GAME_CANVAS)
    board_coord  = hf.detectTemplate(game_image, tmp, False, -1)
    #hf.clickScreen(driver,board_coord[0])
    setAmountV2(26750, amount_dict, board_dict)
    game_image = hf.getGameImage(driver, GAME_CANVAS)
    #r = cv2.selectROI(game_image)
    #imCrop = game_image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    #plt.imshow(imCrop)
    #plt.show()
    #print(r)
   
    #tmp = hf.retrieveAmount(driver, game_image)
    #print(tmp)
    bal = retrieveBalance(driver, game_image)
    print(bal)


