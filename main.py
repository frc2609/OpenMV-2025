# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# AprilTags Example
#
# This example shows the power of the OpenMV Cam to detect April Tags
# on the OpenMV Cam M7. The M4 versions cannot detect April Tags.

import sensor
import time
from machine import PWM, Pin

pwmX = PWM(Pin("P7", Pin.OUT), freq=50, duty_u16=0) # 50Hz 20ms 0% duty
pwmZ = PWM(Pin("P9", Pin.OUT), freq=50, duty_u16=0)
screenW = 160 # QQVGA width to normalize center x
tagMaxW = 120 # maximum expected size of april tag

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

# Note! Unlike find_qrcodes the find_apriltags method does not need lens correction on the image to work.

# Please use the TAG36H11 tag family for this script - it's the recommended tag family to use.

while True:
    clock.tick()
    img = sensor.snapshot()

    tags = img.find_apriltags()

    if len(tags):
        pwmX.duty_u16(int(2**16*(tags[0].cxf/screenW))-1) # set duty (50% = centered)
        pwmZ.duty_u16(int(2**16*(tags[0].w/tagMaxW))-1)
        # print(tags[0].cxf/screenW, tags[0].w/tagMaxW)
    else:
        pwmX.duty_u16(0)
        pwmZ.duty_u16(0)