import cv2
import numpy as np
import pandas as pd 

df = pd.read_csv("Data/Pattern1", index_col = None, usecols =['second_dice', 'first_dice'])

print(df)