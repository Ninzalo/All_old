import pyautogui as pg
import os
import time

connection = 0

#pg.pixelMatchesColor(x, y, (r, g, b))
if not pg.pixelMatchesColor(364,215, (30, 31, 31)):                             
	connection += 1 

if not pg.pixelMatchesColor(713,215, (31, 32, 32)):                             
	connection += 1  

#if connection >= 2:
	#connection = 11
print(connection)