from android_tools.utils import tap_delay
from android_tools.utils import tap_cycle

delay = 0.01


def main():
    print('begin tap')
    while True:
        # tap_delay(500, 1000, delay, 5)
        tap_cycle(500, 1000)


if __name__ == '__main__':
    main()
