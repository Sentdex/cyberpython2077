from framegrabber import FrameGrabber
import cv2
import numpy as np
import time
import keys as k 
from getkeys import key_check
from collections import deque


keys = k.Keys()
screens = deque(maxlen=2)
movements = deque(maxlen=10)

YELLOW_PATH = np.array([75,150,150]), np.array([150,255,255])
BLUE_PATH = np.array([0,150,150]), np.array([50,255,255])

def pathing(minimap, color):
    lower, upper = color

    hsv = cv2.cvtColor(minimap, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    matches = np.argwhere(mask==255)
    mean_y = np.mean(matches[:,1])
    target = minimap.shape[1]/2

    error = target - mean_y

    move_size = 1
    full_range = int(abs(error*1.5))
    
    for i in range(full_range):

        keys.directMouse(-1*int(error/abs(error))*move_size*2, 0)  # doing this to retain the sign. iono.  works. 
        time.sleep(0.000001)

        if i < full_range / 2:
            move_size += 1
        else:
            move_size -= 1
    
    cv2.imshow("cv2screen", mask)
    cv2.waitKey(10)


for i in range(5):
    print(i)
    time.sleep(1)

# Initialize screen grabber
fg = FrameGrabber(0, 0, 2560, 1440, "Cyberpunk 2077 (C) 2020 by CD Projekt RED")

keys.directKey("w")
# run for just 100 frames.

paused_status = False
while True:

    pressed = key_check()
    if 'Y' in pressed: 
        paused_status = not(paused_status)

    if paused_status: 
        print("Paused... (y)")
        time.sleep(1)

    else:
        screen = fg.grab()
        screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2RGB) # because default will be BGR
        minimap = screen[81:377, 2181:2469]
        miniminimap = screen[185:215, 2290:2358]

        screen = cv2.resize(screen, (960,540))
        screens.append(screen)

        if len(screens) == 2:

            diff=cv2.absdiff(screens[1],screens[0])
            gray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
            blurred =cv2.GaussianBlur(gray,(5,5),0)
            _,thresh=cv2.threshold(blurred, 50, 255,cv2.THRESH_BINARY)
            movement_count = len(np.argwhere(thresh==255))
            #print(movement_count) 
            movements.append(movement_count)

            movement_avg = np.mean(movements)

            print('Move avg:',np.mean(movements))
            cv2.imshow("movement_detection", thresh)
            #cv2.waitKey(10)

            if movement_avg < 10000:
                keys.directKey("space")
                keys.directKey("space", keys.key_release)

        try:
            try:
                pathing(miniminimap, color=BLUE_PATH)
            except Exception as e:
                print("falling back to yellow path for now.", str(e))
                pathing(miniminimap, color=YELLOW_PATH)
        except:
            print("Full map zoom out.")
            try:
                pathing(minimap, color=BLUE_PATH)
            except Exception as e:
                print("falling back to yellow path for now.", str(e))
                pathing(minimap, color=YELLOW_PATH)
        #screen = cv2.resize(screen, (960,540))
        #cv2.imshow("cv2screen", screen)
        #cv2.waitKey(10)


keys.directKey("w", keys.key_release)
cv2.destroyAllWindows()
