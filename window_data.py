import cv2
import os
import subprocess

os.chdir('/home/ypelec2022/Desktop/pano')
add_image = cv2.imread('/home/ypelec2022/image2.png', cv2.IMREAD_COLOR)

gotopath = 'cd ~/Desktop/pano'

program = '/home/ypelec2022/Desktop/pano/PANORAMA/pano_exe_showFull /home/ypelec2022/Desktop/pano/pano_param.yaml'

#subprocess.run(gotopath,shell=True)
subprocess.run(program,shell=True)

#cv2.imwrite()
cv2.imshow('original images',add_image)
cv2.waitKey()
cv2.destroyAllWindow()