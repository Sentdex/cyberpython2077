from grabscreen import grab_screen
import cv2
import numpy as np
import time
import keys as k 


keys = k.Keys()


def pathing(minimap):
    lower = np.array([75,150,150])
    upper = np.array([150,255,255])

    hsv = cv2.cvtColor(minimap, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    matches = np.argwhere(mask==255)
    mean_y = np.mean(matches[:,1])
    target = minimap.shape[1]/2

    error = target - mean_y

    print(error)
    keys.directMouse(-1*int(error*3), 0)
    
    cv2.imshow("cv2screen", mask)
    cv2.waitKey(10)


for i in range(5):
    print(i)
    time.sleep(1)


keys.directKey("w")
# run for just 100 frames.
for i in range(100):
    screen = grab_screen(region=(1280, 0, 3840, 1440))  # region will vary depending on game resolution and monitor resolution
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB) # because default will be BGR
    minimap = screen[81:377, 2181:2469]
    miniminimap = screen[185:215, 2290:2358]

    pathing(miniminimap)
    #screen = cv2.resize(screen, (960,540))
    #cv2.imshow("cv2screen", screen)
    #cv2.waitKey(10)
keys.directKey("w", keys.key_release)
cv2.destroyAllWindows()
