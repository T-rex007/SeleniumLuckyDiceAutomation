#!/usr/bin/env python3
"""
Author: Tyrel Cadogan
Email : shaqc777@yahoo.com
Github: https://github.com/T-rex007
"""
import cv2
import numpy as np
import pandas as pd 
import os 
import HelperFunc as hf
import time

from datetime import datetime 
from tqdm import tqdm
from selenium import webdriver


### print(df)
### print(datafile)

l1 = [2,5,1,3,1,5,4,6,5,6,3,2,1,3,4,1,5,6,5,3,1,3]
l2 = [1,2,3,5,6,4,5,1,3,6,5,1,6,5,1,3,1,1,4,6,5,4]
data_dict = {"second_dice": l1,"first_dice":l2}

def CheckPattern(data_dict):
    """
    Returns if there is any matching pattern
    args: Current pattern
    """
    match = True
    datafile = os.listdir('Data')
    print("Checking pattern.....")
    for i in tqdm(range(len(datafile))):
        df = pd.read_csv("Data/{}".format(datafile[i]), index_col = None, usecols =['second_dice', 'first_dice', 'board_type'])
        tmp1 = df['first_dice']
        tmp2 = df['second_dice']
        
        for i2 in range(len(data_dict["first_dice"])):
            if((tmp1[i2] !=data_dict["first_dice"][i2]) and (tmp2[i2] !=data_dict["second_dice"][i2])):
                match = False
                break
        if(match == True):
            return (match, df)
    return (match,None)

def getAllBoardCoord(driver):
    """
    Return a dictionary of Courdinates of different board locations
    args:
        driver - Selenium webdriver
    """
    board_list = ['hi', 'mid', 'lo']
    board_dict = {}
    for b in board_list: 
        tmp =  hf.getTemplate(b)
        game_image = hf.getGameImage(driver, 'layer2')
        board_coord  = hf.detectTemplate(game_image, tmp, False, -1)
        board_dict[b] = board_coord
    return board_dict

if(__name__=="__main__"):
    logged_in_url = "https://logigames.bet9ja.com/games.ls?page=launch&gameid=18000&skin=12&sid=&pff=1&tmp=1611946195"
    driver = webdriver.Firefox()
    driver.get(logged_in_url)
    driver.set_window_size(1280,947)
    time.sleep(15)
    GAME_CANVAS = "layer2"
    game_image = hf.getGameImage(driver, 'layer2')

    ### Press Continue
    tmp =  hf.getTemplate("continue")
    coord  = hf.detectTemplate(game_image, tmp, False, -1)
    hf.clickScreen(driver,coord[0])
    df = pd.read_csv('Data/Pattern-2021-03-02-18-35-50', index_col=None,usecols =['second_dice', 'first_dice','board_type'])
    #print(df['board_type'])
    #print(getAllBoardCoord(driver))

    driver.close()