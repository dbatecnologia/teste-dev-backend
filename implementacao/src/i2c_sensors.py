import smbus2

class I2cSensor(object):
    def __init__(self, addr, bus_num=100):
        self.__addr = addr
        self.__bus_num = bus_num

    def read(self):
        bus = smbus2.SMBus(self.__bus_num)
        data = bus.read_i2c_block_data(self.__addr, 0x00, 3)
        bus.close()
        if data[0] != self.__addr or not self.__test_checksum(data):
            raise
        return data[1]

    def __test_checksum(self, data):
        if len(data) != 3:
            return False
        if data[2] == ((data[0] + data[1]) & 0xff):
            return True
        return False


class LightSensor(I2cSensor):
    def read(self):
        try:
            data = super().read()
            return data if data < 100 else 100
        except:
            return None


class DistanceSensor(I2cSensor):
    def read(self):
        """
        Get distance in meter.
        """
        try:
            return super().read()/100
        except:
            return None


class BatterySensor(I2cSensor):
    def read(self):
        """
        Get battery voltage.
        """
        try:
            return super().read()/10
        except:
            return None
