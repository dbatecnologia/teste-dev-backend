import devices

def main():
    devs = devices.Devices()
    try:
        devs.run()
    except KeyboardInterrupt:
        print('stopping...')

if __name__ == "__main__":
    main()
