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
import json
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

# with open("amount_ditc.json",'w') as jwriter:
#     json.dump(amount_dict,jwriter)


if(__name__ =="__main__"):

    driver = webdriver.Firefox()
    driver.get("https://logigames.bet9ja.com/games.ls?page=launch&gameid=18000&skin=12&sid=&pff=1&tmp=1611946195")
    time.sleep(5)
    GAME_CANVAS = 'layer2'
    driver.set_window_size(1280,947)
    game_image = hf.getGameImage(driver, GAME_CANVAS)
    
    data = dict()
    ### Press Continue
    tmp =  hf.getTemplate("continue")

    coord  = hf.detectTemplate(game_image, tmp, False, -1)
    hf.clickScreen(driver,coord[0])
    game_image = hf.getGameImage(driver, GAME_CANVAS)

    with open("data.json", "r") as jreader:
            d =json.load(jreader)

    coord = (d["2"][0], d["2"][1])
    hf.clickScreen(driver,coord)
    game_image = hf.getGameImage(driver, GAME_CANVAS)

    # for i in range(2,13):
    #     r = cv2.selectROI(game_image)
    #     # Crop image
    #     def cropRegion(r, img):
    #         return img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    #     img = cropRegion(r,game_image)
    #     data["{}".format(i)] = r
    #     print(r)
    #     plt.imsave("imgs/borad_num/{}.jpg".format(i), img)

    # with open("data.json", "w") as jwriter1:
    #     json.dump(data, jwriter1)
    # driver.close()
    # print(r)

    # with open("data.json", "r") as jreader:
    #     d =json.load(jreader)
    
    # print(d)