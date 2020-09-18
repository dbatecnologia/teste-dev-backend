#!/usr/bin/env python3

import time
import devices

def main():
    devs = devices.Devices()
    try:
        while True:
            print(devs.read())
            time.sleep(1)
    except KeyboardInterrupt:
        print('stopping...')

if __name__ == "__main__":
    main()
