from pynput import mouse,keyboard
import threading
from robot_command.rpl import *

## when a key is pressed 
def on_release(key):
    global movementMode, exitProgram

    if(key == keyboard.Key.esc):
        exitProgram = True
    
    try:
        if(key.char == 'i'):
            if(movementMode == False):
                print("entering movement mode")
                movementMode = True
            else:
                print("exiting movement mode")
                movementMode = False
    except AttributeError:
        pass

## this is when mouse moves
def on_move(x,y):
    global movementMode, pos_x, pos_y

    if(movementMode == True):
        print('Pointer moved to {0}'.format((x,y)))
        
## when mouse is clicked
def on_mouse_click(x,y,button, pressed):
    global movementMode

    if(movementMode):
        print('{0} at {1} with {2}'.format(
        "Pressed" if pressed else "No Pressed",
        (x,y),
        button
        ))

#threading lock for concurancy
lock = threading.Lock()

#Program State
movementMode = False
exitProgram = False

pos_x = 0
pos_y = 0

#this is in mm
# x/400 = xPos/1800 -> x = 400*xPos/1800
frame_x_max = 400
frame_y_max = 400


set_units("mm", "deg")

#tormach
def main():
    print("starting mouse listener")
    mouseListener = mouse.Listener(on_move= on_move, on_click= on_mouse_click)
    mouseListener.start()

    print("starting key listener")
    keyboardListener = keyboard.Listener(on_release= on_release)
    keyboardListener.start()

    #while (not exitProgram):
        #if movementMode:
            #movel()
    
    keyboardListener.stop()
    mouseListener.stop()
    quit()


    
