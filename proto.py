#!/usr/bin/env python3
"""
Author: Tyrel Cadogan
Email : shaqc777@yahoo.com
Github: https://github.com/T-rex007
"""
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


parser = argparse.ArgumentParser()

assertion_statment ="Ooops you may have entered an invalid bot mode\n\tAvailible modes are 'live', 'demo', 'test' and 'live-test"
parser.add_argument("mode", help ="Opening Bot in demo mode", type = str)
args = parser.parse_args()
assert((args.mode == 'demo')|(args.mode =='live')|(args.mode=='test')|(args.mode=='live-test')), assertion_statment

if __name__ == '__main__' :
    print('Running Bot in {} mode'.format(args.mode))
    if ((args.mode == 'demo')| (args.mode =='live')):
        ################################## Betting Amount #########################################################
        user_s_amount_raw = input("Please enter Starting betting amount \n\t>>>")
        try:
            user_s_amount  = int(user_s_amount_raw)
        except:
            print("Please ensure to enter correct data formats")
        assert((user_s_amount%50)== 0)

        ######################################## Sleep time ###################################################
        sleeptime_raw = input("Please Enter Sleep time \n\t>>>")
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
        board_type = input("Please enter board type \n >>>")
        assert((board_type== 'hi')| (board_type =='mid')|(board_type=='lo'))
    else:
        ### Testing mode Developer specified test cases
        recovery_factor = 1
        user_numberofwins = 5
        user_s_amount = 50
        user_s_bet_amount = 300
        sleeptime = 2
        board_type = 'hi'
    
    ###Error StamentS 
    ERROR1_STATEMENT = "Oh No! Something went wrong \n Try not to interfare with the window: Error 1"
    ERROR2_STATEMENT = "Oh No! Something went wrong! Error 2"
    ERROR3_STATEMENT = "Oh No! Something went wrong! Error 3"
    #ERROR4_STATEMENT = "Something Went Wrong! :( Error 4 "

    DEMO_GAME_URL = "https://logigames.bet9ja.com/games.ls?page=launch&gameid=18000&skin=12&sid=&pff=1&tmp=1611946195"
    GAME_CANVAS = "layer2"

    amount_list_sorted =  ['50', '250', '1k', '5k', '25k', '250k', '1m']
    data_dict= {'first_dice':[],
                'second_dice': [],
                'board_type':[]}
    amount_dict = {'amt_region':(1098, 478), '50': (915, 484), '250':(800, 485), 
                '1k':(676, 485), '5k':(553, 485), '25k':(434, 484), 
                '250k': (309, 484), '1m': (184, 484)}
    test_data_dict = {'first_dice':[6,4,5,1,3,6,6,5,5,1],
                'second_dice': [5,4,4,6,2,4,4,2,3,2],
                'board_type':['hi','mid','hi','mid','lo','hi','hi','mid','mid','lo']}



    r_stake = (987, 653, 272, 63)
    r1 = (1065, 188, 84, 35)
    r2  = (1160, 189, 86, 33)
    win_size = (1280,947)

    ### Initialize Driver
    if((args.mode == 'demo')| (args.mode == 'test')):
        ### Initialize Diver
        driver = webdriver.Firefox()
        driver.get("https://logigames.bet9ja.com/games.ls?page=launch&gameid=18000&skin=12&sid=&pff=1&tmp=1611946195")
        time.sleep(5)
        driver.set_window_size(1280,947)
        
        print(driver.get_window_size())
        #assert(0)
    elif((args.mode == 'live')|(args.mode =='live-test')):
        ### Initialize Diver
        driver_login = webdriver.Firefox()
        driver_login.get("https://casino.bet9ja.com/casino/category/all")
        ### Enter credentials
        username_element = driver_login.find_element_by_name("username")
        password_element = driver_login.find_element_by_name("password")

        username_element.send_keys("Donbull001")
        password_element.send_keys("Post20192020", Keys.RETURN)
        # element = driver.find_element_by_xpath("//div[@id='18000']//div[@class='game__info']//button[@class='btn-primary-xxs']")
        # action = webdriver.common.action_chains.ActionChains(driver)
        # action.move_to_element_with_offset(element, 10, 10)
        # action.click()
        # # action.perform()
        logged_in_url = input("Please enter live url \n >>>")
        #driver_login.close()
        driver = webdriver.Firefox()
        driver.get(logged_in_url)
        driver.set_window_size(1280,947)

    print('Wait until the page has loaded before continuing!')
    start = input("Start y or n : ")
    if(start != 'y'):
        ### Stop the programm
        print("Exiting bot.....")
        driver.close()
        sys.exit()  
    
    driver.set_window_size(1280,947)
    
    game_image = hf.getGameImage(driver, GAME_CANVAS)

    ### Press Continue
    tmp =  hf.getTemplate("continue")

    coord  = hf.detectTemplate(game_image, tmp, False, -1)
    hf.clickScreen(driver,coord[0])

    ### Select Board
    board_dict = hf.getAllBoardCoord(driver)
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
    match = False
    pattern_found = True
    while(1):
        if (count == countstop):
            df =pd.DataFrame(data_dict)
            df.to_csv("Data/Pattern-"+str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+ ".csv")
            batch = batch + 1
            count = 0
            wins = 0
            losses = 0
            data_dict= {'first_dice':[],
                        'second_dice': [],
                            'board_type':[]}
            print("Pattern {} Finished".format(batch))
            print("Saving pattern CSV")
            print("Closing Driver.......")
            driver.close()
            
            ### Initialize Driver
            print("Reinitializing driver")
            driver = webdriver.Firefox()
            driver.get("https://logigames.bet9ja.com/games.ls?page=launch&gameid=18000&skin=12&sid=&pff=1&tmp=1611946195")
            time.sleep(20)
            GAME_CANVAS = "layer2"

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
            dice_sum = num1 + num2

            assert(2<=(dice_sum)<= 12), ERROR1_STATEMENT

            ### Save Numbers to data dictionary
            data_dict['first_dice'].append(num1)
            data_dict['second_dice'].append(num2)

            if(dice_sum > 8):
                data_dict['board_type'].append('hi')
            elif(6<=dice_sum<=8):
                data_dict['board_type'].append('mid')
            elif(dice_sum<6):
                data_dict['board_type'].append('lo')
            else:
                print(ERROR2_STATEMENT)

            print("Cross referencing patterns")
            if(count>=2):
                match, pattern = hf.CheckPattern(data_dict)
                print(count)
                if(match == True):
                    print("A Pattern was found!")
                    amt = user_s_bet_amount
                    match = True
                elif(match == False):
                    match = False
                    print("No Pattern found!")
            count = count + 1
            ### if board type is lo
            if(board_type == 'lo'):
                if(2<=(dice_sum) <=5):
                    wins = wins + 1
                    losses = 0
                    print("Win!")
                    
                    if(match == True):
                        ### If pattern found
                        amt = user_s_bet_amount
                        ### Set the next pattern
                        print("Look here")
                        tmp = pattern['board_type']
                        tmp = tmp[count]
                        board_from_pattern = board_dict[tmp]               
                        time.sleep(5)
                        num_clicks = amt/50 + 1 
                        hf.setAmount(driver, num_clicks, board_from_pattern[0])
                    else:
                        amt = user_s_amount    
                        time.sleep(5)
                        num_clicks = amt/50 + 1 
                        hf.setAmount(driver, num_clicks, board_coord[0])
                else:
                    losses = losses + 1
                    wins = 0
                    print("Loss!")
                    print("Apply recovery Factor")
                    if(match == True):
                        ### If pattern found
                        amt = user_s_bet_amount
                        ### Set the next pattern
                        print("Look here")
                        tmp = pattern['board_type']
                        tmp = tmp[count]
                        board_from_pattern = board_dict[tmp]               
                        time.sleep(5)
                        num_clicks = amt/50 + 1 
                        hf.setAmount(driver, num_clicks, board_from_pattern[0])
                    else:   
                        print("Loss!")
                        print("Apply recovery Factor")
                        time.sleep(5)
                        amt = amt *recovery_factor
                        num_clicks = amt/50 +1
                        hf.setAmount(driver, num_clicks, board_coord[0])
            ### If board type is mid
            elif(board_type == 'mid'):
                if(6<=dice_sum<=8):
                    wins = wins + 1
                    losses = 0
                    print("Win!")
                    
                    if(match == True):
                        ### If pattern found
                        amt = user_s_bet_amount
                        ### Set the next pattern
                        print("Look here")
                        tmp = pattern['board_type']
                        tmp = tmp[count]
                        board_from_pattern = board_dict[tmp]               
                        time.sleep(5)
                        num_clicks = amt/50 + 1 
                        hf.setAmount(driver, num_clicks, board_from_pattern[0])
                    else:
                        amt = user_s_amount    
                        time.sleep(5)
                        num_clicks = amt/50 + 1 
                        hf.setAmount(driver, num_clicks, board_coord[0])
                else:
                    losses = losses + 1
                    wins = 0
                    print("Loss!")
                    print("Apply recovery Factor")
                    if(match == True):
                        ### If pattern found
                        amt = user_s_bet_amount
                        ### Set the next pattern
                        print("Look here")
                        tmp = pattern['board_type']
                        tmp = tmp[count]
                        board_from_pattern = board_dict[tmp]               
                        time.sleep(5)
                        num_clicks = amt/50 + 1 
                        hf.setAmount(driver, num_clicks, board_from_pattern[0])
                    else:   
                        print("Loss!")
                        print("Apply recovery Factor")
                        time.sleep(5)
                        amt = amt *recovery_factor
                        num_clicks = amt/50 +1
                        hf.setAmount(driver, num_clicks, board_coord[0])
            ### if board is hi   
            elif(board_type == 'hi'):
                if(9<=dice_sum <=12):
                    wins = wins + 1
                    losses = 0
                    print("Win!")
                    
                    if(match == True):
                        ### If pattern found
                        amt = user_s_bet_amount
                        ### Set the next pattern
                        print("Look here")
                        tmp = pattern['board_type']
                        tmp = tmp[count]
                        board_from_pattern = board_dict[tmp]               
                        time.sleep(5)
                        num_clicks = amt/50 + 1 
                        hf.setAmount(driver, num_clicks, board_from_pattern[0])
                    else:
                        amt = user_s_amount    
                        time.sleep(5)
                        num_clicks = amt/50 + 1 
                        hf.setAmount(driver, num_clicks, board_coord[0])
                else:
                    losses = losses + 1
                    wins = 0
                    print("Loss!")
                    print("Apply recovery Factor")
                    if(match == True):
                        ### If pattern found
                        amt = user_s_bet_amount
                        ### Set the next pattern
                        print("Look here")
                        tmp = pattern['board_type']
                        tmp = tmp[count]
                        board_from_pattern = board_dict[tmp]               
                        time.sleep(5)
                        num_clicks = amt/50 + 1 
                        hf.setAmount(driver, num_clicks, board_from_pattern[0])
                    else:   
                        print("Loss!")
                        print("Apply recovery Factor")
                        time.sleep(5)
                        amt = amt *recovery_factor
                        num_clicks = amt/50 +1
                        hf.setAmount(driver, num_clicks, board_coord[0])
            else: 
                print(ERROR3_STATEMENT)

            
            time.sleep(2)
            print(num1)
            print(num2)
            print("The Number of consecutive wins: {}".format(wins))
            print("THe Number of bets: {}".format(count))
            #print("Current Stake amount: {}".format(amt))
            
            print("Press CTRL + C to close the program")
            if (wins== user_numberofwins):
                print("\tI have won: {} times".format(wins))
                print("\tTime to take a nap")
                time.sleep(60*sleeptime)
                print("Time to wake up")
            print("*****************************************************************")
            print()