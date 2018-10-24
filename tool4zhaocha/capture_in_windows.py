import pyHook
import pythoncom
from PIL import ImageGrab

# from win32api import GetSystemMetrics as gsm

# 提前绑定鼠标位置事件
old_x, old_y = 0, 0
new_x, new_y = 0, 0
full = False
hm = None


def hotkey(key=None):
    """绑定热键，开始进行划屏截图操作"""
    pass


def on_mouse_event(event):
    global old_x, old_y, new_x, new_y, full, hm
    print('event.MessageName: %s' % event.MessageName)
    if event.MessageName == "mouse left down":
        old_x, old_y = event.Position
        print('click down: %d, %d' % (old_x, old_y))
    if event.MessageName == "mouse left up":
        new_x, new_y = event.Position
        print('click up: %d, %d' % (new_x, new_y))
        # 解除事件绑定
        hm.UnhookMouse()
        hm.UnhookKeyboard()
        hm = None
        capture()
    return True


def capture():
    global old_x, old_y, new_x, new_y, full
    print('begin capture')
    if full:
        image = ImageGrab.grab()
    else:
        image = ImageGrab.grab((old_x, old_y, new_x, new_y))
    image.show()


def begin_hook_mouse():
    global hm
    hm = pyHook.HookManager()
    hm.SubscribeMouseAllButtons(on_mouse_event)
    hm.HookMouse()
    hm.HookKeyboard()
    pythoncom.PumpMessages()


if __name__ == "__main__":
    begin_hook_mouse()
