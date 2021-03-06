import os
import time
import pyautogui as pag
import pythoncom
import pyHook

old_x, old_y = 0, 0
new_x, new_y = 0, 0
hm = None


def print_mouse_position():
    try:
        while True:
            print("Press Ctrl-C to end")
            x, y = pag.position()  # 返回鼠标的坐标
            pos_str = "Position:" + str(x).rjust(4) + ',' + str(y).rjust(4)
            print(pos_str)  # 打印坐标
            time.sleep(0.2)
            os.system('cls')  # 清楚屏幕
    except KeyboardInterrupt:
        print('end....')


def on_mouse_event(event):
    global old_x, old_y, new_x, new_y, hm
    print('event.MessageName: %s' % event.MessageName)
    if event.MessageName == "mouse left down":
        old_x, old_y = event.Position
        print('click down: %d, %d' % (old_x, old_y))
    if event.MessageName == "mouse left up":
        new_x, new_y = event.Position
        print('click up: %d, %d' % (new_x, new_y))
        hm.UnhookMouse()
        hm.UnhookKeyboard()
        hm = None
    return True


def start_get_mouse_click_pos():
    global hm
    hm = pyHook.HookManager()
    hm.SubscribeMouseAllButtons(on_mouse_event)
    hm.HookMouse()
    hm.HookKeyboard()
    pythoncom.PumpMessages()


def get_grab_pos():
    global old_x, old_y, new_x, new_y
    return old_x, old_y, new_x, new_y


if __name__ == "__main__":
    print('please click:')
    start_get_mouse_click_pos()
