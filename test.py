import sys
import pandas as pd
import numpy as np
import os
from tqdm import tqdm
def slidingWindowPatternCheck(pattern, window,stride = 1): 
    """
    Returns whether a pattern match of the pattern in tthe input window 
    in the data.
    """
    assert(isinstance(pattern, list)), "The type given: {}".format(type(pattern))
    assert(isinstance(window, list)), "The type given: {}".format(type(window))
    n = len(pattern)
    num_slides = int((n-len(window))/stride)
    for i in range(0,num_slides + 1, stride):
        if(window == pattern[i:i +len(window)]):
            return (True, i + len(window))  
    return (False, -1)

def searchPatterns(data_dict,start,window_size = 5):
    """
    Returns a dictionary of the format
    dict ={ "check": (Boolean that describes whether or not a pattern is found, the index of the pattern where the pattern ends)
            "pattern": A pandas dataframe containing the pattern found.
    } 
    Args: 
        data_dict: A Dictionary containing the pattern being collected
        window_size: The size of the pattern window   
    """

    file_names = os.listdir("Data")
    for i in tqdm(range(len(file_names))):
        file_name = "Data/{}".format(file_names[i])
        df = pd.read_csv(file_name, index_col = 0)
        first_dice = list(df['first_dice'])
        second_dice = list(df['second_dice'])
        first_dice_check = slidingWindowPatternCheck(first_dice, data_dict['first_dice'][start: window_size+start])
        second_dice_check = slidingWindowPatternCheck(second_dice, data_dict['second_dice'][start: window_size+start])

        if((first_dice_check == second_dice_check) and  second_dice_check[0]):
            print("Pattern Found!")
            print("Pattern Type: Exact Sequential Match")
            print("File name of the pattern found: ",file_name)
            return {"check": second_dice_check, "patterns": df}
    
    print("No Pattern found")
    return {"check":(False,-1), "patterns": df}




if(__name__ == "__main__"):

    data_dict = {'first_dice':[3,3,3,1,1,2,4,5,1,4],
                'second_dice': [1,1,6,5,6,2,4,1,6,4],
                'board_type': ['lo','lo','hi','mid','mid','lo','mid','mid','mid','mid']}


    pattern = [3,3,3,1,1,2,4,5,1,4]
    window = [3,3,1,1,2]
 
    #print(slidingWindowPatternCheck(data_dict['first_dice'], data_dict['first_dice'][-5:]))
    print(searchPatterns(data_dict = data_dict,start =0 , window_size =5))

