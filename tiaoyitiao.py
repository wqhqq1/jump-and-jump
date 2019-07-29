import os
from PIL import Image
import numpy
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
import time
need_update = True
def get_screen_image():
    os.system('adb shell screencap -p /sdcard/screen.png')
    os.system('adb pull /sdcard/screen.png')
    return numpy.array(Image.open('screen.png'))
def jump_to_next(point1, point2):
    x1, y1 = point1;x2, y2 = point2
    distance = ((x2-x1)**2 + (y2-y1)**2)**0.5
    os.system('adb shell input touchscreen swipe 330 410 330 410 {}'.format(int(distance*1.35)))
    global  need_update
    need_update = True
def on_calck(event,coor=[]):
    coor.append((event.xdata, event.ydata))
    if len(coor) == 2:
        jump_to_next(coor.pop(), coor.pop())
    global need_update
    need_update = True
def update_screen(frame):
    global need_update
    if need_update:
        time.sleep(1)
        axes_image.set_array(get_screen_image())
        need_update = False
    return axes_image,
def main():
    figure = pyplot.figure()
    axes_image = pyplot.imshow(get_screen_image(), animated=True)
    figure.canvas.mpl_connect('button_press_event', on_calck)
    ani = FuncAnimation(figure, update_screen, interval=50, blit=True)
    pyplot.show()
if __name__ == '__main__':
    main()