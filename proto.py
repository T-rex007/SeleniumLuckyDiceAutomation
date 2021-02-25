#!/usr/bin/env python3
"""
Author: Tyrel Cadogan
Email : shaqc777@yahoo.com
Github: https://github.com/T-rex007
"""

from   selenium import webdriver
import pytesseract
import cv2
import time
import HelperFunc as hf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

### User Inputs (to be  programmed)
################################## Betting Amount #########################################################
user_s_amount_raw = input("'live' or 'demo' betting" \n>>>")
try:
    user_s_amount  = int(user_s_amount_raw)
except:
    print("Please ensure to enter correct data formats")
assert((user_s_amount%50)== 0)

################################## Betting Amount #########################################################
user_s_amount_raw = input("Please enter Starting betting amount \n>>>")
try:
    user_s_amount  = int(user_s_amount_raw)
except:
    print("Please ensure to enter correct data formats")
assert((user_s_amount%50)== 0)

######################################## Sleep time ###################################################
sleeptime_raw = input("Please Enter Sleep time \n>>>")
try:
    sleeptime  = abs(int(sleeptime_raw))
except:
    print("Please ensure to enter correct data formats")

########################################### Number of wins ################################################
user_numberofwins_raw = input("Please enter number of wins you woullike to take a break at  \n>>>")
try:
    user_numberofwins = int(user_numberofwins_raw)
except:
    print("Please ensure to enter correct data formats")
assert(user_numberofwins > 0)

########################################## Recover factor #################################################
recovery_factor_raw = input("Please enter Recovery Factor \n>>>")
try:
    recovery_factor = int(recovery_factor_raw)
except:
    print("Please ensure to enter correct data formats")
assert(recovery_factor>0)

######################################### Board type ###################################################
board_type_raw = input("Please enter board type \n >>>")
assert((board_type== 'hi')| (board_type =='mid')|(board_type=='lo'))



amount_list_sorted =  ['50', '250', '1k', '5k', '25k', '250k', '1m']
data_dict= {'first_dice':[],
            'second_dice': []}
amount_dict = {'amt_region':(1098, 478), '50': (915, 484), '250':(800, 485), 
               '1k':(676, 485), '5k':(553, 485), '25k':(434, 484), 
               '250k': (309, 484), '1m': (184, 484)}

r_stake = (987, 653, 272, 63)
r1 = (1065, 188, 84, 35)
r2  = (1160, 189, 86, 33)

### Initialize Driver
driver = webdriver.Firefox()
driver.get("https://logigames.bet9ja.com/games.ls?page=launch&gameid=18000&skin=12&sid=&pff=1&tmp=1611946195")
time.sleep(5)
GAME_CANVAS = "layer2"
game_img = hf.getGameImage(driver, GAME_CANVAS)

### Press Continue
tmp =  hf.getTemplate("continue")
game_image = hf.getGameImage(driver, GAME_CANVAS)
coord  = hf.detectTemplate(game_image, tmp, False, -1)
hf.clickScreen(driver,coord[0])


### Select Board
tmp =  hf.getTemplate(board_type)
game_image = hf.getGameImage(driver, GAME_CANVAS)
board_coord  = hf.detectTemplate(game_image, tmp, False, -1)
hf.clickScreen(driver,board_coord[0])

### Select Amount
num_clicks = abs(user_s_amount/50)
hf.setAmount(driver, num_clicks, board_coord)


count  = 0
batch = 1
losses = 0
countstop = 10
wins = 0
amt = user_s_amount
while(1):
    if (count == countstop):
        df =pd.DataFrame(data_dict)
        df.to_csv("Data/Pattern{}".format(batch))
        batch = batch + 1
        count = 0
        wins = 0
        losses = 0
        data_dict= {'first_dice':[],
                    'second_dice': []}
        print("Pattern {} Finished".format(batch))
        print("Saving pattern CSV")
        print("Closing Driver.......")
        driver.close()
        
        ### Initialize Driver
        print("Reinitializing driver")
        driver = webdriver.Firefox()
        driver.get("https://logigames.bet9ja.com/games.ls?page=launch&gameid=18000&skin=12&sid=&pff=1&tmp=1611946195")
        time.sleep(5)
        GAME_CANVAS = "layer2"
        game_img = hf.getGameImage(driver, GAME_CANVAS)

        ### Press Continue
        tmp =  hf.getTemplate("continue")
        game_image = hf.getGameImage(driver, GAME_CANVAS)
        coord  = hf.detectTemplate(game_image, tmp, False, -1)
        hf.clickScreen(driver,coord[0])
        #balance = hf.retrieveAmount(driver)

        ### Select Board
        tmp =  hf.getTemplate(board_type)
        game_image = hf.getGameImage(driver, GAME_CANVAS)
        board_coord  = hf.detectTemplate(game_image, tmp, False, -1)
        hf.clickScreen(driver,board_coord[0])
        
        ### Select Amount
        num_clicks = abs(user_s_amount/50)
        hf.setAmount(driver, num_clicks, board_coord)
            
    else:
        ### bet
        print("Roll #{}".format(count))
        tmp =  hf.getTemplate("rebet")
        game_image = hf.getGameImage(driver, GAME_CANVAS)
        coord  = hf.detectTemplate(game_image, tmp, False, 3)
        hf.clickScreen(driver,(coord[0][0] + 50, coord[0][1] + 50) )
        time.sleep(10)
        print("Current Stake amount: {}".format(amt))
        
        ### Retrieve images Dice number 
        game_image = hf.getGameImage(driver, GAME_CANVAS)       
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
        
        ### Save Numbers to data dictionary
        data_dict['first_dice'].append(num1)
        data_dict['second_dice'].append(num2)
        count = count + 1

    
        ### if board type is high
        if(board_type == 'lo'):
            if(2<=(num1+ num2) <=5):
                wins = wins + 1
                losses = 0
                print("Win!")
                amt = user_s_amount
                time.sleep(5)
                num_clicks = amt/50 + 1 
                hf.setAmount(driver, num_clicks, board_coord)
            else:
                losses = losses + 1
                wins = 0
                print("Loss!")
                print("Apply a Recovery Factor of {}".format(recovery_factor))
                amt = amt *recovery_factor
                num_clicks = amt/50 + 1
                hf.setAmount(driver, num_clicks, board_coord)
        ### If board type is mid
        elif(board_type == 'mid'):
            if(6<=(num1+ num2) <=8):
                wins = wins + 1
                losses = 0
                print("Win!")
                amt = user_s_amount
                time.sleep(5)
                num_clicks = amt/50 + 1 
                hf.setAmount(driver, num_clicks, board_coord)
            else:
                losses = losses + 1
                wins = 0
                print("Loss!")
                print("Apply a Recovery Factor of {}".format(recovery_factor))
                amt = amt *recovery_factor
                num_clicks = amt/50 + 1
                hf.setAmount(driver, num_clicks, board_coord)
        ### etc    
        elif(board_type == 'hi'):
            if(9<=(num1+ num2) <=12):
                wins = wins + 1
                losses = 0
            else:
                losses = losses + 1
                wins = 0
                print("Loss!")
                print("Apply recovery Factor")
                amt = amt *recovery_factor
                num_clicks = amt/50
                hf.setAmount(driver, num_clicks, board_coord)

        time.sleep(2)
                
        print(num1)
        print(num2)
        print("The Number of consecutive wins: {}".format(wins))
        print("THe Number of bets: {}".format(count))
        #print("Current Stake amount: {}".format(amt))

        if (wins== user_numberofwins):
            print("\t I have won: {} times".format(wins))
            print("\t Time to take a nap")
            time.sleep(60*sleeptime)
            print("Time to wake up")
        print("***********************************************************")
        print()