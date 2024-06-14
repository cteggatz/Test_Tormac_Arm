from robot_command.rpl import *
import rospy

try:
    from pynput import mouse,keyboard
except:

    import sh
    with sh.sudo:
        sh.pip3.install("pynput")
        from pynput import keyboard

pressed_keys = set()

set_units("mm", "deg")


def on_key_press(key):
    global exitProgram
    
    try:
        if(key.char):
            pressed_keys.add(key.char)
            #rospy.logwarn(f'key {key.char} was pressed')
    except AttributeError:
        if(key == keyboard.Key.esc):
            #rospy.logwarn(f'killing program!')
            trigger_interrupt(1, 0)
            return False
        pressed_keys.add(key)

def on_key_lift(key):
    try:
        if(key.char):
            pressed_keys.discard(key.char)
            #rospy.logwarn(f'key {key.char} was pressed')
    except AttributeError:
        pressed_keys.discard(key)
        return False

keyboardListener = keyboard.Listener(
    on_press= on_key_press,
    on_release= on_key_lift
)

#bounds
max_x = 400
max_y = 400

## checks if the coordinates provided are within the constraints set in max_x & max_y
##
def checkBounds(coord, bound):
    if(coord >= bound):
        rospy.logwarn("movement more then max bounds - restrictin movement")
        return bound
    elif (coord <= 0):
        rospy.logwarn("movement less then min bounds - restrictin movement")
        return 0
    else:
        return coord

def interrupt_handler(value):
    if value == 0:
        keyboardListener.stop()
        exit()


# --- init ----

keyboardListener.start()
moveDist = 10

set_user_frame("WASD_Test", p[400, -200, 500, 0,0,0])
change_user_frame("WASD_Test")
set_tool_frame("tool_frame1", orientation=p[0,0,0,180,0,0])
change_tool_frame("tool_frame1")  # We make sure we are using it

#poses
home = Pose()
next_move = get_pose().to_list()
#tormac stuff
register_interrupt(InterruptSource.Program, 1, interrupt_handler)
movej(home)


def main():
    global next_move





    if("w" in pressed_keys):
        next_move[0] = checkBounds(next_move[0] - moveDist, max_x)
    if("s" in pressed_keys):
        next_move[0] = checkBounds(next_move[0] + moveDist, max_x)
    if("a" in pressed_keys):
        next_move[1] = checkBounds(next_move[1] - moveDist, max_y)
    if("d" in pressed_keys):
        next_move[1] = checkBounds(next_move[1] + moveDist, max_y)
        
    movej(p[next_move[0],next_move[1],next_move[2],next_move[3],next_move[4],next_move[5]])    