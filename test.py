from robot_command.rpl import *
#import rospy
#I should probaby learn rospy....
#and I should learn python

import threading

try:
    from pynput import mouse,keyboard
except:

    import sh
    with sh.sudo:
        sh.pip3.install("pynput")
        from pynput import mouse,keyboard

set_units("mm", "deg")

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
mouseListener = mouse.Listener(on_move= on_move, on_click= on_mouse_click)
keyboardListener = keyboard.Listener(on_release= on_release)

def interupt_handler(value):
    if value == True:
        mouseListener.stop()
        keyboardListener.stop()
        quit()

#Program State
movementMode = False
exitProgram = False

pos_x = 0
pos_y = 0

#this is in mm
# x/400 = xPos/1800 -> x = 400*xPos/1800
frame_x_max = 400
frame_y_max = 400

#tormach
def main():
    #start mouse listener
    mouseListener.start()

    #start key listener
    keyboardListener.start()

    #registers stop interupt
    register_interrupt(InterruptSource.Program, 1,  interupt_handler)




    while (True):
        if(exitProgram):
            trigger_interrupt(1, True)
        if movementMode:
            print("yippee")