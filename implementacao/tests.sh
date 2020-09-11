#!/bin/bash

echo "> Test FakeSerial"
python3 -m unittest tests.fake_devices.fake_interfaces.fake_serial
