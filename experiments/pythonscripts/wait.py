#!/usr/bin/env python3
"""
Author: Tyrel Cadogan
Email : shaqc777@yahoo.com
Github: https://github.com/T-rex007
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


if __name__=='__main__':
    DEMO_GAME_URL = "https://logigames.bet9ja.com/games.ls?page=launch&gameid=18000&skin=12&sid=&pff=1&tmp=1611946195"
    GAME_CANVAS = "layer2"
    driver = webdriver.Firefox()
    driver.get(DEMO_GAME_URL)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "GAME_CANVAS"))
        )
    finally:
        print("Done")
        driver.close()
        
    #print(help(By))
