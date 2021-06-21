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
import json
import argparse
import getpass
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
        user_numberofwins_raw = input("Please enter number of wins you would like to take a break at  \n>>>")
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
        ############################################################################################
        user_s_bet_amount = input("Please enter the stake amount to use when a pattern is found \n>>>")
        try:
            user_s_bet_amount = int(user_s_bet_amount)
        except:
            print("Please ensure to enter correct data formats")
        assert(user_s_bet_amount>0)
        ######################################### Board type ###################################################
        # board_type = input("Please enter board type \n >>>")
        # assert((board_type== 'hi')| (board_type =='mid')|(board_type=='lo'))
        
        ### Change this value to change user Name 
        username = "Donbull001"

        if (args.mode == 'live'):
            ### Uncomment if you want to take user name as input
            # username = input("Please enter user name: \n>>>")
            password = getpass.getpass("Please enter password: \n>>>")
        else:
            ### Uncomment if you want to take user name as input
            # username = None
            password = None
    else:
        ### Testing mode Developer specified test cases
        recovery_factor = 2
        user_numberofwins = 1
        user_s_amount = 50
        user_s_bet_amount = 300
        sleeptime = 1
        #board_type = 'lo'
    
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
    test_data_dict = {'first_dice':[6,6,2,3,6,3,6,3,3,4,],
                'second_dice': [4,5,5,1,4,2,5,2,6,1],
                'board_type':['hi','hi','mid','lo','hi','lo','hi','lo','hi','lo']}
    board_order = ['mid','hi', 'lo']
    board_index = 0
    board_type  = board_order[board_index]

    # Loadin Board Nums
    with open("data.json", "r") as jreader:
        double_beting_coodinates =json.load(jreader)

    r_stake = (987, 653, 272, 63)
    r1 = (1065, 188, 84, 35)
    r2  = (1160, 189, 86, 33)
    win_size = (1280,947)

    ### Initialize Driver
    if((args.mode == 'demo')| (args.mode == 'test')):
        ### Initialize Diver
        driver = webdriver.Chrome()
        driver.get(DEMO_GAME_URL)
        time.sleep(5)
        driver.set_window_size(1280,947)
        
        print(driver.get_window_size())
        #assert(0)
    elif((args.mode == 'live')|(args.mode =='live-test')):
        ### Initialize Diver
        driver_login = webdriver.Chrome()
        driver_login.get("https://casino.bet9ja.com/casino/category/all")
        ### Enter credentials
        username_element = driver_login.find_element_by_name("username")
        password_element = driver_login.find_element_by_name("password")

        username_element.send_keys(username)
        password_element.send_keys(password, Keys.RETURN)

        logged_in_url = input("Please enter live url \n >>>")
        driver = webdriver.Chrome()
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
    #hf.clickScreen(driver,board_coord[0])

    bal = hf.retrieveBalance(driver, game_image)

    #sys.exit()

    ### Select Amount
    hf.setAmountV2(driver,user_s_amount, amount_dict, board_coord[0])


    count  = 0
    batch = 1
    losses = 0
    countstop = 100
    total_wins = 0
    wins = 0
    pattern_check_start = 0
    amt = user_s_amount 
    match = False
    pattern_found = True
    roll_num_since_sleep = 0
    while(1):
        if (count == countstop):
            df =pd.DataFrame(data_dict)
            df.to_csv("Data/Pattern{}-".format(batch)+str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+ ".csv")
            batch = batch + 1
            count = 0
            losses = 0
            match = False
            roll_num_since_sleep = 0
            board_index = 0
            board_type  = board_order[board_index]
            data_dict= {'first_dice':[],
                        'second_dice': [],
                            'board_type':[]}
            print("Pattern {} Finished".format(batch))
            print("Saving pattern CSV")
            print("Closing Driver.......")
            driver.close()
            
            ### Initialize Driver
            print("Reinitializing driver")
            driver = webdriver.Chrome()
            driver.get("https://logigames.bet9ja.com/games.ls?page=launch&gameid=18000&skin=12&sid=&pff=1&tmp=1611946195")
            driver.set_window_size(1280,947)
            time.sleep(30)
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
            #num_clicks = abs(user_s_amount/50)
            #hf.setAmount(driver, num_clicks, board_coord)
            hf.setAmountV2(driver,amt, amount_dict, board_coord[0])    
        else:
            ### bet
            print("Roll #{}".format(count + 1))
            print("The Number of rolls since last Sleep Time: {}".format(roll_num_since_sleep + 1))
            tmp =  hf.getTemplate("rebet")
            game_image = hf.getGameImage(driver, GAME_CANVAS)
            coord  = hf.detectTemplate(game_image, tmp, False, 3)
            hf.clickScreen(driver,(coord[0][0] + 50, coord[0][1] + 50) )
            time.sleep(20)
            print("Current Stake amount: {}".format(amt))
            time.sleep(20)
            ### Read dice Value
            tmp1,tmp2 = hf.getDiceNum(driver)
            time.sleep(5)
            tmp3,tmp4 = hf.getDiceNum(driver)
            assert((tmp1 ==tmp3) and (tmp2 == tmp4)),"Oooops Something went wrong"
            num1 = tmp3
            num2 = tmp4
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
            
            #r = cv2.selectROI(im)

            #imCrop = im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

            bal = hf.retrieveBalance(driver, game_image)

            #sys.exit()
            print("Balance: ",bal)
            count = count + 1 
            if(count>=5):
                print("Cross referencing patterns")

                ### Searching for patterns
                match_dict =hf.searchPatterns(data_dict = data_dict, start = pattern_check_start)
                pattern_check_start = count
                match, pattern_start = match_dict["check"]
                pattern = match_dict["patterns"]
                
                if(match == True):
                    print("A Pattern was found!")
                    amt = user_s_bet_amount
                    pattern_count = pattern_start
                    match = True
                elif(match == False):
                    match = False
                    print("No Pattern found!")

            
            ### if board type is lo
            if(board_type == 'lo'):
                if(2<=(dice_sum) <=5):
                    wins = wins + 1
                    losses = 0
                    print("Win!")
                    
                    if(match == True):
                        ### If pattern found
                        
                        amt = user_s_bet_amount
                        if(amt>bal):
                            print('Stake Amount has Exceeded your current balance Exiting now')
                            sys.exit()
                        ### Set the next pattern
                        tmp = pattern['board_type']
                        pattern_count +=1
                        tmp = tmp[pattern_count]
                        print("count: ", count )
                        print("Playing Board: ",tmp)
                        board_from_pattern = board_dict[tmp]               
                        time.sleep(5)
                        coord = (double_beting_coodinates["{}".format(dice_sum)][0], double_beting_coodinates["{}".format(dice_sum)][1])
                        hf.clickScreen(driver,coord)
                        #hf.clickScreen(driver,coord[0])
                        hf.setAmountV2(driver,amt, amount_dict, board_from_pattern[0])
                    else:
                        amt = user_s_amount
                        if(amt>bal):
                            print('Stake Amount has Exceeded your current balance Exiting now')
                            sys.exit()    
                        time.sleep(5)
                        hf.setAmountV2(driver,amt, amount_dict, board_coord[0])
                else:
                    losses = losses + 1
                    if(match == True):
                        ### If pattern found
                        print("Loss!")
                        amt = (amt *recovery_factor) + user_s_bet_amount
                        if(amt>bal):
                            print('Stake Amount has Exceeded your current balance Exiting now')
                            sys.exit()
                        ### Set the next pattern
                        pattern_count +=1
                        tmp = pattern['board_type']
                        tmp = tmp[pattern_count]
                        print("count: ", count )
                        print("Playing Board: ",tmp)
                        board_from_pattern = board_dict[tmp]               
                        time.sleep(5)
                        coord = (double_beting_coodinates["{}".format(dice_sum)][0], double_beting_coodinates["{}".format(dice_sum)][1])
                        hf.clickScreen(driver,coord)
                        hf.setAmountV2(driver,amt, amount_dict, board_from_pattern[0])
                    else:   
                        print("Loss!")
                        print("Apply recovery Factor")
                        time.sleep(5)
                        amt = amt *recovery_factor
                        if(amt>bal):
                            print('Stake Amount has Exceeded your current balance Exiting now')
                            sys.exit()
                        hf.setAmountV2(driver,amt, amount_dict, board_coord[0])
            ### If board type is mid
            elif(board_type == 'mid'):
                if(6<=dice_sum<=8):
                    wins = wins + 1
                    losses = 0
                    print("Win!")
                    
                    if(match == True):
                        ### If pattern found
                        
                        amt = user_s_bet_amount
                        if(amt>bal):
                            print('Stake Amount has Exceeded your current balance Exiting now')
                            sys.exit()
                        ### Set the next pattern
                        tmp = pattern['board_type']
                        pattern_count += 1
                        tmp = tmp[pattern_count]
                        print("count: ", count )
                        print("Playing Board: ",tmp)
                        board_from_pattern = board_dict[tmp]               
                        time.sleep(5)
                        coord = (double_beting_coodinates["{}".format(dice_sum)][0], double_beting_coodinates["{}".format(dice_sum)][1])
                        hf.clickScreen(driver, coord)
                        hf.setAmountV2(driver, amt, amount_dict, board_from_pattern[0])
                    else:
                        amt = user_s_amount
                        if(amt>bal):
                            print('Stake Amount has Exceeded your current balance Exiting now')
                            sys.exit()    
                        time.sleep(5)
                        hf.setAmountV2(driver,amt, amount_dict, board_coord[0])
                else:
                    losses = losses + 1
                    if(match == True):
                        ### If pattern found
                        print("Loss!")
                        amt = (amt *recovery_factor) + user_s_bet_amount
                        if(amt>bal):
                            print('Stake Amount has Exceeded your current balance Exiting now')
                            sys.exit()
                        ### Set the next pattern
                        pattern_count += 1
                        tmp = pattern['board_type']
                        tmp = tmp[pattern_count]
                        print("count: ", count )
                        print("Playing Board: ",tmp)
                        board_from_pattern = board_dict[tmp]               
                        time.sleep(5)
                        coord = (double_beting_coodinates["{}".format(dice_sum)][0], double_beting_coodinates["{}".format(dice_sum)][1])
                        hf.clickScreen(driver, coord)
                        hf.setAmountV2(driver, amt, amount_dict, board_from_pattern[0])
                    else:   
                        print("Loss!")
                        print("Apply recovery Factor")
                        time.sleep(5)
                        amt = amt *recovery_factor
                        if(amt>bal):
                            print('Stake Amount has Exceeded your current balance Exiting now')
                            sys.exit()
                        hf.setAmountV2(driver,amt, amount_dict, board_coord[0])
            ### if board is hi   
            elif(board_type == 'hi'):
                if(9<=dice_sum <=12):
                    wins = wins + 1
                    losses = 0
                    print("Win!")
                    
                    if(match == True):
                        ### If pattern found
                        
                        amt = user_s_bet_amount
                        if(amt>bal):
                            print('Stake Amount has Exceeded your current balance Exiting now')
                            sys.exit()
                        ### Set the next pattern
                        pattern_count += 1
                        tmp = pattern['board_type']

                        tmp = tmp[pattern_count]
                        print("count: ", count )
                        print("Playing Board: ",tmp)
                        board_from_pattern = board_dict[tmp]               
                        time.sleep(5)
                        coord = (double_beting_coodinates["{}".format(dice_sum)][0], double_beting_coodinates["{}".format(dice_sum)][1])
                        hf.clickScreen(driver,coord)
                        hf.setAmountV2(driver,amt, amount_dict, board_from_pattern[0])
                    else:
                        amt = user_s_amount
                        if(amt>bal):
                            print('Stake Amount has Exceeded your current balance Exiting now')
                            sys.exit()    
                        time.sleep(5)
                        hf.setAmountV2(driver,amt, amount_dict, board_coord[0])
                else:
                    losses = losses + 1
                    if(match == True):
                        ### If pattern found
                        print("Loss!")
                        amt = (amt *recovery_factor) + user_s_bet_amount
                        if(amt>bal):
                            print('Stake Amount has Exceeded your current balance Exiting now')
                            sys.exit()
                        ### Set the next pattern
                        pattern_count += 1
                        tmp = pattern['board_type']
                        tmp = tmp[pattern_count]
                        print("count: ", count )
                        print("Playing Board: ",tmp)
                        board_from_pattern = board_dict[tmp]               
                        time.sleep(5)
                        coord = (double_beting_coodinates["{}".format(dice_sum)][0], double_beting_coodinates["{}".format(dice_sum)][1])
                        hf.clickScreen(driver,coord)
                        hf.setAmountV2(driver,amt, amount_dict, board_from_pattern[0])
                    else:   
                        print("Loss!")
                        print("Apply recovery Factor")
                        time.sleep(5)
                        amt = amt *recovery_factor
                        if(amt>bal):
                            print('Stake Amount has Exceeded your current balance Exiting now')
                            sys.exit()
                        hf.setAmountV2(driver,amt, amount_dict, board_coord[0])
            else: 
                print(ERROR3_STATEMENT)
            
            time.sleep(2)
            print(num1)
            print(num2)
            print("The Number of Total wins: {}".format(wins))
            print("THe Number of bets: {}".format(count))
            #print("Current Stake amount: {}".format(amt))
            roll_num_since_sleep += 1
            print("Press CTRL + C to close the program")
            if (wins== user_numberofwins):
                print("I have won: {} times".format(wins))
                print("Time to take a nap")
                roll_num_since_sleep = 0
                total_wins = total_wins + wins
                wins = 0
                driver.close()
                time.sleep(60*sleeptime)
                print("Time to wake up")
                ### Initialize Drivers
                if((args.mode == 'demo')| (args.mode == 'test')):
                    ### Initialize Diver
                    driver = webdriver.Chrome()
                    driver.get(DEMO_GAME_URL)
                    time.sleep(5)
                    driver.set_window_size(1280,947)
                    print(driver.get_window_size())

                    #assert(0)
                elif((args.mode == 'live')|(args.mode =='live-test')):
                    ### Initialize Diver            
                    driver = webdriver.Chrome()
                    driver.get(logged_in_url)
                    driver.set_window_size(1280,947)
                time.sleep(60)
                # Update Board type
                board_index += 1
                if(board_index >2):
                    board_index = 0
                board_type = board_order[board_index]

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
                #hf.clickScreen(driver,board_coord[0])

                bal = hf.retrieveBalance(driver, game_image)
                   ### Select Amount
                
                hf.setAmountV2(driver,user_s_amount, amount_dict, board_coord[0])

                ### Select Amount
                hf.setAmountV2(driver,user_s_amount, amount_dict, board_coord[0])
                driver.set_window_size(1280,947)
            print("*****************************************************************")
            print()