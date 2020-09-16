#!/bin/bash

RED='\e[31m'
GREEN='\e[32m'
NC='\e[0m' # No Color

function echo_red {
    echo -e "$RED$@$NC"
}

function echo_green {
    echo -e "$GREEN$@$NC"
}

function unittest {
    local title=$1
    local file=$2

    echo_green "\n*************************************************************"
    echo_green "Test $title"

    python3 -m unittest $file

    if [ $? -ne 0 ]; then
        echo_red "\nTest $title failed. Exiting..."
        exit
    fi
}

unittest FakeSerial tests.fake_devices.fake_interfaces.fake_serial
unittest FakeI2c tests.fake_devices.fake_interfaces.fake_i2c
unittest FakeI2cSensor tests.fake_devices.fake_i2c_sensor
unittest FakeGpsSensor tests.fake_devices.fake_gps_sensor
unittest FakeGprs tests.fake_devices.fake_gprs
