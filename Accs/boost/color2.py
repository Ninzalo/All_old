import win32gui
import os
import time
import pyautogui as pg


while 1:
	def pixel_color_at(x,y):
		hdc = win32gui.GetWindowDC(win32gui.GetDesktopWindow())
		c = int(win32gui.GetPixel(hdc, x, y))
		return (c & 0xff), ((c >> 8) & 0xff), ((c >> 16) & 0xff)
	pix = pixel_color_at(*win32gui.GetCursorPos())
	print(pix)
	print(win32gui.GetCursorPos())
	time.sleep(0.5)
	os.system('cls||clear')

