#!/usr/bin/env python3
"""
Author: Tyrel Cadogan
Email : shaqc777@yahoo.com
Github: https://github.com/T-rex007
"""
import 
import numpy as np

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


if(__name__ =="__main__"):
    print(optimizeAmtClick(120650))
    




