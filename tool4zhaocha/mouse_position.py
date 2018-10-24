import os
import time
import pyautogui as pag
import pythoncom
import pyHook


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
    print("Position:", event.Position)
    return True


def print_mouse_click_pos():
    hm = pyHook.HookManager()
    hm.HookKeyboard()
    hm.MouseAllButtonsDown = on_mouse_event
    hm.MouseAllButtonsUp = on_mouse_event
    hm.HookMouse()
    pythoncom.PumpMessages()


if __name__ == "__main__":
    print_mouse_click_pos()
