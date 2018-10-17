import win32gui, win32con, win32api


def _MyCallback(hwnd, extra):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        windows = extra
        temp = []
        temp.append(hex(hwnd))
        temp.append(win32gui.GetClassName(hwnd))
        temp.append(win32gui.GetWindowText(hwnd))
        windows[hwnd] = temp


def TestEnumWindows():
    windows = {}
    win32gui.EnumWindows(_MyCallback, windows)
    print("Enumerated a total of  windows with %d classes".format(len(windows)))
    print('------------------------------')
    # print classes
    for item in windows:
        print(windows[item])
    print('-------------------------------')


print("Enumerating all windows...")
h = win32gui.FindWindow(None, '\xba\xec\xce\xe5')
print(hex(h))
TestEnumWindows()
print("All tests done!")
