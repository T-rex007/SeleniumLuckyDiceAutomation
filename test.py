import sys
import pandas as pd
import numpy as np
import os

def slidingWindowPatternCheck(pattern, window,stride = 1): 
    """
    Returns whether a pattern match of the pattern in tthe input window 
    in the data.
    """
    
    assert(isinstance(pattern, list)), "The type given: {}".format(type(pattern))
    assert(isinstance(window, list)), "The type given: {}".format(type(window))
    n = len(pattern)
    num_slides = int((n-len(window))/stride)
    for i in range(0,num_slides, stride):
        if(window == pattern[i:i +len(window)]):
            return (True, i + len(window))  
    return (False, -1)


def searchPatterns(data_dict,window_size):


    #print(slidingWindowPatternCheck(pattern,window))

    file_names = os.listdir("Data")
    for i in range(len(file_names)):
        file_name = "Data/{}".format(file_names[i])
        df = pd.read_csv(file_name)
        first_dice = list(df[df.columns[1]])
        second_dice = list(df[df.columns[2]])
        boards = list(df[df.columns[3]])
        dice_sum = list(np.array(first_dice) + np.array(second_dice))

        current_dice_sum = list(np.array(data_dict['first_dice'][-window_size:]) + np.array(data_dict['second_dice'][-window_size:]))

        first_dice_check = slidingWindowPatternCheck(first_dice, data_dict['first_dice'][-window_size:])
        second_dice_check = slidingWindowPatternCheck(second_dice, data_dict['second_dice'][-window_size:])
        dice_sum_check  = slidingWindowPatternCheck(dice_sum, current_dice_sum)
        boards_check  = slidingWindowPatternCheck(boards, data_dict['board_type'][-window_size:])

        if(first_dice_check[0]):
            print(first_dice_check)
            print(file_name)
            return {"check": first_dice_check, "patterns": df}

        elif(second_dice_check[0]):
            print(second_dice_check)
            print(file_name)
            return {"check": boards_check, "patterns": df}

        elif(dice_sum_check[0]):
            print(dice_sum_check)
            print(file_name)
            return {"check": boards_check, "patterns": df}

        elif(boards_check[0]):
            print(file_name)
            return {"check": boards_check, "patterns": df}


    return None




if(__name__ == "__main__"):

    data_dict = {'first_dice':[6,6,2,3,6,3,6,3,3,4,],
                'second_dice': [4,5,5,1,4,2,5,2,6,1],
                'board_type':['hi','hi','mid','lo','hi','lo','hi','lo','hi','lo']}
    pattern = [1,23,4,3,22,34,35,5,43,45,35,34,34,53]
    window = [22,34,5,35]

    print(slidingWindowPatternCheck(pattern,window))

    file_names = os.listdir("Data")
    window_size = 5
    for i in range(len(file_names)):
        file_name = "Data/{}".format(file_names[i])
        df = pd.read_csv(file_name)
        first_dice = list(df[df.columns[1]])
        second_dice = list(df[df.columns[2]])
        boards = list(df[df.columns[3]])
        dice_sum = list(np.array(first_dice) + np.array(second_dice))

        current_dice_sum = list(np.array(data_dict['first_dice'][-window_size:]) + np.array(data_dict['second_dice'][-window_size:]))

        first_dice_check = slidingWindowPatternCheck(first_dice, data_dict['first_dice'][-window_size:])
        second_dice_check = slidingWindowPatternCheck(second_dice, data_dict['second_dice'][-window_size:])
        dice_sum_check  = slidingWindowPatternCheck(dice_sum, current_dice_sum)
        boards_check  = slidingWindowPatternCheck(boards, data_dict['board_type'][-window_size:])

        if(first_dice_check[0]):
            print(first_dice_check)
            print(file_name)
            sys.exit("Pattern found")

        elif(second_dice_check[0]):
            print(second_dice_check)
            print(file_name)
            sys.exit("Pattern found")

        elif(dice_sum_check[0]):
            print(dice_sum_check)
            print(file_name)
            sys.exit("Pattern found")

        elif(boards_check[0]):
            print(boards_check)
            print(file_name)
            sys.exit("Pattern found")

    print("No paterns found")


    
    # pattern = [1,23,4,3,22,34,35,5,43,45,35,34,34,53]
    # window = [22,34,5,35]
    # n = len(pattern)
    # stride = 1
    # num_slides = int((n-len(window))/stride)
    # for i in range(0,num_slides, stride):
    #     if(window == pattern[i:i +len(window)]):
    #         outputs = (True, i + len(window))
    #         print(outputs)
    #         sys.exit("Pattern found")
    
    
    # outputs = (False, -1)
    # print(outputs)



    

