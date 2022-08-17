import pyautogui as pg

x, y = pg.position()
pix = pg.pixel(x,y)
print(pix)